from tkinter import *
from twitter import *
from PIL import ImageTk
import os
import shutil
import json
import boto3
import botocore
import requests
from datetime import datetime

class MyTk(Tk):
    def __init__(self, master=None):
        Tk.__init__(self, master)
        
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

        self.panel = Label(self)
        self.panel.pack(side = 'bottom', fill = 'both', expand = 'yes')

        self.id = self.after(3000, self.callback)

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
            img = ImageTk.PhotoImage(data=bytes)
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
root.attributes('-fullscreen', True)

root.mainloop()
