#
# CrowdShare
# Paul Norton
#

### Imports ###
from tkinter import *
from twython import *
from PIL import ImageTk, Image
import io
import json
import boto3
import requests
from datetime import datetime

### MyTk - Tk Class Extension ###
# Gives Tkinter window ability to enter or exit full screen when user presses 'f' or 'esc'
class RootTk(Tk):
    def __init__(self, master=None):
        Tk.__init__(self, master)

        # Bind key events to fullscreen
        self.bind('<f>', self.enter_fullscreen)
        self.bind('<Escape>', self.exit_fullscreen)
    
    # enter_fullscreen: go to fullscreen
    def enter_fullscreen(self, e):
        self.attributes('-fullscreen', True)
    
    # exit_fullscreen: go back to previous size
    def exit_fullscreen(self, e):
        self.attributes('-fullscreen', False)

### CrowdShare - Frame Class Extension ###
# Handles all the main functionality of the CrowdShare app
class CrowdShare(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, bg='black')
        
        # Configure initial display
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)
        self.original = Image.open('media/logo.jpg')
        self.image = ImageTk.PhotoImage(self.original)
        self.display = Canvas(self, bd=0, highlightthickness=0, bg='black', width=800, height=600)
        self.display.create_image(0, 0, image=self.image, anchor=CENTER, tags='IMG')
        self.display.grid(row=0, sticky=W+E+N+S)
        self.pack(fill=BOTH, expand=1)
        
        # Binds window resizing to CrowdShare.resize_event
        self.bind('<Configure>', self.resize_event)
        
        # Import configuration created by setup.py
        file = open('config.json', 'r')
        config = json.loads(file.read())
        file.close()
       
        # Event hashtag
        self.HASHTAG = config['hashtag']
 
        # Twitter
        self.APP_KEY = config['app_key']
        self.APP_SECRET = config['app_secret']
        self.OAUTH_TOKEN = config['oauth_token']
        self.OAUTH_TOKEN_SECRET = config['oauth_token_secret']
        self.twitter = Twython(self.APP_KEY, self.APP_SECRET, self.OAUTH_TOKEN, self.OAUTH_TOKEN_SECRET)

        # Instagram
        self.ACCESS_TOKEN = config['access_token']        
        
        # Amazon Web Service
        self.AWS = config['aws']
        if self.AWS:
            self.s3 = boto3.resource('s3')
            self.bucket_name = self.build_bucket_name(self.HASHTAG, datetime.now())            
            self.bucket = self.s3.create_bucket(Bucket=self.bucket_name)

        # Set up other attributes
        self.x = 0
        self.pics = []
        self.text = ''
        
        # Start callback cycle
        self.id = self.after(3000, self.callback)

    # callback: main event, gets called every three seconds
    def callback(self):
        # Call various social media APIs
        self.search_twitter()
        self.get_twitter_dms()
        self.search_instagram()
        
        # Rotate image
        self.set_image()
        
        # Continue callback cycle
        self.id = self.after(3000, self.callback)

    # resize_event: called when window is resized
    def resize_event(self, event):
        # Pass values to resize method
        self.resize(event.width, event.height)

    # resize: changes image size to match size of window
    def resize(self, width, height):
        # Adjust for window margins
        width -= 40
        height -= 120
        
        # Calculate maximum size at the original aspect ratio
        if height/width > self.original.height/self.original.width:
            size = (width, int(width*self.original.height/self.original.width))
        else:
            size = (int(height*self.original.width/self.original.height), height)
            
        # Resize image and set up image and caption label
        resized = self.original.resize(size,Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(resized)
        self.display.delete('IMG')
        self.display.delete('TEXT')
        self.display.create_image(width/2+20, height/2+20, image=self.image, anchor=CENTER, tags='IMG')
        self.display.create_text(width/2+20, height+100, anchor=S, text=self.text, tags='TEXT', fill='white', font=("Purisa", 18), width=width, justify=CENTER)
    
    # set_image: Rotate image on the window
    def set_image(self):
        # Make sure we have pictures
        if len(self.pics) > 0:
            # Reset counter if necessary
            if self.x == len(self.pics):
                self.x = 0
            
            # Get next post
            post = self.pics[self.x]
            
            # Retrieve picture from AWS or local storage
            if self.AWS:
                bytes = self.retrieve_from_aws(post.file_name)
                self.original = Image.open(io.BytesIO(bytes))
            else:
                self.original = Image.open(post.file_name)
            
            # Set image and text and call resize
            self.image = ImageTk.PhotoImage(self.original)
            self.text = post.message
            self.resize(self.display.winfo_width(), self.display.winfo_height())
            
            # Increment counter
            self.x += 1

    # search_twitter: get tweets with event hashtag
    def search_twitter(self):
        # Call twitter API
        tweets = self.twitter.search(q='#'+self.HASHTAG)
        
        # Cycle through tweets
        for status in tweets['statuses']:
            # Check if there are media attached
            try:
                media = status['extended_entities']['media']
            except:
                continue
            
            # Cycle through media and get photos
            for item in media:
                if item['type'] == 'photo':
                    # Check if we've already processed the image
                    if not any(x.id == item['id'] for x in self.pics):
                        # Create Post object and save
                        post = Post(id=item['id'], user_name=status['user']['screen_name'], platform='twitter', file_name=str(len(self.pics))+'.jpg', url=item['media_url_https'], text=status['text'])
                        self.save_image(post)
                        self.pics.append(post)

    # get_twitter_dms: get direct messages sent to account
    def get_twitter_dms(self):
        # Call twitter API
        dms = self.twitter.get_direct_messages()
        
        # Cycle through messages
        for dm in dms:
            # Check if there are media attached
            try:
                media = dm['entities']['media']
            except:
                continue
            
            # Cycle through media and get photos
            for item in media:
                if item['type'] == 'photo':
                    # Check if we've already processed the image
                    if not any(x.id == item['id'] for x in self.pics):
                        # Create Post object and save
                        post = Post(id=item['id'], user_name=dm['sender']['screen_name'], platform='twitter', file_name=str(len(self.pics))+'.jpg', url=item['media_url_https'], text=dm['text'])
                        self.save_image(post)
                        self.pics.append(post)

    # search_instagram: get instagram posts with event hashtag
    def search_instagram(self):
        # Call instagram API
        r = requests.get('https://api.instagram.com/v1/tags/' + self.HASHTAG + '/media/recent?access_token=' + self.ACCESS_TOKEN)
        json_data = json.loads(r.content.decode())
        posts = json_data['data']
        
        # Cycle through posts
        for post in posts:
            # Check if we've already processed the image
            if not any(x.id == post['id'] for x in self.pics):
                # Create Post object and save
                post = Post(id=post['id'], user_name=post['user']['username'], platform='instagram', file_name=str(len(self.pics))+'.jpg', url=post['images']['standard_resolution']['url'], text=post['caption']['text'])
                self.save_image(post)
                self.pics.append(post)
    
    # save_image: save image to AWS or to local storage        
    def save_image(self, post):
        # Get image bytes (use twitter client for direct message authentication)
        r = self.twitter.client.get(post.url)
        
        # Save to AWS or to local storage
        if self.AWS:
            r = requests.get(post.url)
            self.bucket.put_object(Key=post.file_name, Body=r.content)
        else:
            file = open(post.file_name, 'wb')
            file.write(r.content)
            file.close()
    
    # retrieve_from_aws: get image from AWS
    def retrieve_from_aws(self, key):
        object = self.s3.Object(self.bucket_name,key)
        return object.get()['Body'].read()
    
    # build_bucket_name: helper method to create name for S3 bucket
    def build_bucket_name(self, hashtag, date):
        date_str = str(date).replace(' ', '-').replace(':', '-').split('.')[0]
        return hashtag + '-' + date_str

### Post - Custom Class ###
# Contains all information about an image
class Post:
    def __init__(self, id, user_name, platform, file_name, url, text):
        self.id = id
        self.user_name = user_name
        self.platform = platform
        self.file_name = file_name
        self.url = url
        
        # Remove potentially bad characters (emojis, etc.)
        text = text.encode('ascii', 'ignore').decode().strip()
        self.text = (text[:75] + '...') if len(text) > 75 else text
        
        # Build message for image caption
        self.message = '"' + self.text + '" - ' + self.user_name + ' via ' + self.platform

### Initialization ###
root = RootTk()
crowdshare = CrowdShare(root)
crowdshare.mainloop()
