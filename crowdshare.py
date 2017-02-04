from tkinter import *
from twitter import *
from PIL import ImageTk, Image
import io
import json
import boto3
import requests
from datetime import datetime

class MyTk(Tk):
    def __init__(self, master=None):
        Tk.__init__(self, master)

        self.bind('<f>', self.fullscreen)
        self.bind('<Escape>', self.exit_fullscreen)

    def fullscreen(self, e):
        self.attributes('-fullscreen', True)
    def exit_fullscreen(self, e):
        self.attributes('-fullscreen', False)

class App(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)
        self.original = Image.open('logo.jpg')
        self.image = ImageTk.PhotoImage(self.original)
        self.display = Canvas(self, bd=0, highlightthickness=0)
        self.display.create_image(self.display.winfo_width()/2, self.display.winfo_height()/2, image=self.image, anchor=CENTER, tags="IMG")
        self.display.grid(row=0, sticky=W+E+N+S)
        self.pack(fill=BOTH, expand=1)
        self.bind("<Configure>", self.resize_event)
        
        file = open('config.json', 'r')
        config = json.loads(file.read())
        file.close()
        
        self.BEARER_TOKEN = config['bearer_token']
        self.ACCESS_TOKEN = config['access_token']        
        self.HASHTAG = config['hashtag']

        self.twitter = Twitter(auth=OAuth2(bearer_token=self.BEARER_TOKEN))
        
        self.s3 = boto3.resource('s3')
        self.bucket_name = self.build_bucket_name(self.HASHTAG, datetime.now())            
        self.bucket = self.s3.create_bucket(Bucket=self.bucket_name)

        self.x = 1
        self.pics = []

        self.id = self.after(3000, self.callback)

    def resize_event(self, event):
        self.resize(event.width, event.height)

    def resize(self, width, height):
        if height/width > self.original.height/self.original.width:
            size = (width, int(width*self.original.height/self.original.width))
        else:
            size = (int(height*self.original.width/self.original.height), height)
        resized = self.original.resize(size,Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(resized)
        self.display.delete("IMG")
        self.display.create_image(width/2, height/2, image=self.image, anchor=CENTER, tags="IMG")        

    def callback(self):
        self.search_twitter()
        self.search_instagram()
        self.set_image()
        
        self.id = self.after(3000, self.callback)
        
    def set_image(self):
        if len(self.pics) > 0:
            if self.x > len(self.pics):
                self.x = 1
            bytes = self.retrieve_from_aws(str(self.x) + '.jpg')
            self.original = Image.open(io.BytesIO(bytes))
            self.image = ImageTk.PhotoImage(self.original)
            self.resize(self.display.winfo_width(), self.display.winfo_height())

            self.x += 1

    def search_twitter(self):
        tweets = self.twitter.search.tweets(q='#'+self.HASHTAG)
        for status in tweets['statuses']:
            try:
                media = status['extended_entities']['media']
            except:
                continue
            for item in media:
                if item['type'] == 'photo':
                    url = item['media_url_https']
                    if url not in self.pics:
                        self.pics.append(url)
                        self.save_to_aws(url)
    
    def search_instagram(self):
        r = requests.get('https://api.instagram.com/v1/tags/' + self.HASHTAG + '/media/recent?access_token=' + self.ACCESS_TOKEN)
        json_data = json.loads(r.content.decode())
        posts = json_data['data']
        for post in posts:
            url = post['images']['standard_resolution']['url']
            if url not in self.pics:
                self.pics.append(url)
                self.save_to_aws(url)
                
    def save_to_aws(self, url):
        r = requests.get(url)
        self.bucket.put_object(Key=str(len(self.pics)) + '.jpg', Body=r.content)
        
    def retrieve_from_aws(self, key):
        object = self.s3.Object(self.bucket_name,key)
        return object.get()['Body'].read()
    
    def build_bucket_name(self, hashtag, date):
        date_str = str(date).replace(' ', '-').replace(':', '-').split('.')[0]
        return hashtag + '-' + date_str

root = MyTk()
app = App(root)
app.mainloop()
