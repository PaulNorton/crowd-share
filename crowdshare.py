from tkinter import *
from twitter import *
from PIL import ImageTk, Image
import io
import json
import boto3
import requests
from datetime import datetime
from urllib.request import urlretrieve

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
        Frame.__init__(self, master, bg='black')
                
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)
        self.original = Image.open('media/logo.jpg')
        self.image = ImageTk.PhotoImage(self.original)
        self.display = Canvas(self, bd=0, highlightthickness=0, bg='black', width=800, height=600)
        self.display.create_image(0, 0, image=self.image, anchor=CENTER, tags='IMG')
        self.display.grid(row=0, sticky=W+E+N+S)
        self.pack(fill=BOTH, expand=1)
        
        self.bind('<Configure>', self.resize_event)
        
        file = open('config.json', 'r')
        config = json.loads(file.read())
        file.close()
        
        self.BEARER_TOKEN = config['bearer_token']
        self.ACCESS_TOKEN = config['access_token']        
        self.HASHTAG = config['hashtag']
        self.AWS = config['aws'];

        self.twitter = Twitter(auth=OAuth2(bearer_token=self.BEARER_TOKEN))
        
        if self.AWS:
            self.s3 = boto3.resource('s3')
            self.bucket_name = self.build_bucket_name(self.HASHTAG, datetime.now())            
            self.bucket = self.s3.create_bucket(Bucket=self.bucket_name)

        self.x = 0
        self.pics = []
        self.text = ''

        self.id = self.after(3000, self.callback)

    def resize_event(self, event):
        self.resize(event.width, event.height)

    def resize(self, width, height):
        width -= 40
        height -= 120
        if height/width > self.original.height/self.original.width:
            size = (width, int(width*self.original.height/self.original.width))
        else:
            size = (int(height*self.original.width/self.original.height), height)
        resized = self.original.resize(size,Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(resized)
        self.display.delete('IMG')
        self.display.delete('TEXT')
        self.display.create_image(width/2+20, height/2+20, image=self.image, anchor=CENTER, tags='IMG')
        self.display.create_text(width/2+20, height+100, anchor=S, text=self.text, tags='TEXT', fill='white', font=("Purisa", 18), width=width, justify=CENTER)

    def callback(self):
        self.search_twitter()
        self.search_instagram()
        self.set_image()
        
        self.id = self.after(3000, self.callback)
        
    def set_image(self):
        if len(self.pics) > 0:
            if self.x == len(self.pics):
                self.x = 0
                
            post = self.pics[self.x]
            
            if self.AWS:
                bytes = self.retrieve_from_aws(post.file_name)
                self.original = Image.open(io.BytesIO(bytes))
            else:
                self.original = Image.open(post.file_name)
            
            self.image = ImageTk.PhotoImage(self.original)
            self.text = post.message
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
                    if not any(x.id == item['id'] for x in self.pics):
                        post = Post(id=item['id'], user_name=status['user']['screen_name'], platform='twitter', file_name=str(len(self.pics))+'.jpg', url=url, text=status['text'])
                        self.save_to_aws(post)
                        self.pics.append(post)
    
    def search_instagram(self):
        r = requests.get('https://api.instagram.com/v1/tags/' + self.HASHTAG + '/media/recent?access_token=' + self.ACCESS_TOKEN)
        json_data = json.loads(r.content.decode())
        posts = json_data['data']
        for post in posts:
            url = post['images']['standard_resolution']['url']
            if not any(x.id == post['id'] for x in self.pics):
                post = Post(id=post['id'], user_name=post['user']['username'], platform='instagram', file_name=str(len(self.pics))+'.jpg', url=url, text=post['caption']['text'])
                self.save_to_aws(post)
                self.pics.append(post)
                
    def save_to_aws(self, post):
        if self.AWS:
            r = requests.get(post.url)
            self.bucket.put_object(Key=post.file_name, Body=r.content)
        else:
            urlretrieve(post.url, post.file_name)
            
    def retrieve_from_aws(self, key):
        object = self.s3.Object(self.bucket_name,key)
        return object.get()['Body'].read()
    
    def build_bucket_name(self, hashtag, date):
        date_str = str(date).replace(' ', '-').replace(':', '-').split('.')[0]
        return hashtag + '-' + date_str

class Post:
    def __init__(self, id, user_name, platform, file_name, url, text):
        self.id = id
        self.user_name = user_name
        self.platform = platform
        self.file_name = file_name
        self.url = url
        
        text = text.encode('ascii', 'ignore').decode().strip()
        self.text = (text[:75] + '...') if len(text) > 75 else text
        
        self.message = '"' + self.text + '" - ' + self.user_name + ' via ' + self.platform

root = MyTk()
app = App(root)
app.mainloop()
