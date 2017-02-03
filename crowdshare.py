from tkinter import *
from twitter import *
from urllib.request import urlretrieve, urlopen
from PIL import ImageTk, Image
import os
import shutil
import json

class MyTk(Tk):
    def __init__(self, master=None):
        Tk.__init__(self, master)
        
        file = open('.config', 'r')
        config = json.loads(file.read())
        file.close()
        
        self.BEARER_TOKEN = config['bearer_token']
        self.ACCESS_TOKEN = config['access_token']        
        self.HASHTAG = config['hashtag']

        self.twitter = Twitter(auth=OAuth2(bearer_token=self.BEARER_TOKEN))

        self.x = 1
        self.pics = []

        self.panel = Label(self)
        self.panel.pack(side = 'bottom', fill = 'both', expand = 'yes')

        self.id = self.after(3000, self.callback)

    def callback(self):
        self.search_twitter()
        self.search_instagram()
        self.set_image()
        
        #You can cancel the call by doing "self.after_cancel(self.id)"
        self.id = self.after(3000, self.callback)
        
    def set_image(self):
        if len(self.pics) > 0:
            if self.x > len(self.pics):
                self.x = 1
            img = ImageTk.PhotoImage(Image.open('img/' + str(self.x) + '.jpg'))
            self.panel.configure(image = img)
            self.panel.image = img
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
                        urlretrieve(url, 'img/' + str(len(self.pics)) + '.jpg')
    
    def search_instagram(self):
        response = urlopen('https://api.instagram.com/v1/tags/' + self.HASHTAG + '/media/recent?access_token=' + self.ACCESS_TOKEN)
        json_data = json.load(response)
        posts = json_data['data']
        for post in posts:
            url = post['images']['standard_resolution']['url']
            if url not in self.pics:
                self.pics.append(url)
                urlretrieve(url, 'img/' + str(len(self.pics)) + '.jpg')

if os.path.isdir('img'):
    shutil.rmtree('img')
os.makedirs('img')

root = MyTk()
root.attributes('-fullscreen', True)

root.mainloop()
