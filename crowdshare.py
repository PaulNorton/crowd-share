#
# crowdshare
# Paul Norton
#

### Imports ###
from tkinter import *
from PIL import ImageTk, Image
import io
import json
from modules.rootTk import RootTk
from modules.twitter import Twitter
from modules.instagram import Instagram
from modules.aws import Aws

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
       
        # Constants
        self.HASHTAG = config['hashtag']
 
        # Twitter
        self.twitter = Twitter(config['app_key'], config['app_secret'], config['oauth_token'], config['oauth_token_secret'])

        # Instagram
        self.instagram = Instagram(config['access_token'])
        
        # Amazon Web Service
        self.aws = Aws(config['aws_access_key_id'], config['aws_secret_access_key'], self.HASHTAG)

        # Set up other attributes
        self.x = 0
        self.pics = []
        self.text = ''
        
        # Start callback cycle
        self.id = self.after(3000, self.callback)

    # callback: main event, gets called every three seconds
    def callback(self):
        # Call various social media APIs
        self.search_media()
        
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
            
            # Retrieve picture from AWS
            bytes = self.aws.retrieve_from_aws(post.file_name)
            self.original = Image.open(io.BytesIO(bytes))
            
            # Set image and text and call resize
            self.image = ImageTk.PhotoImage(self.original)
            self.text = post.message
            self.resize(self.display.winfo_width(), self.display.winfo_height())
            
            # Increment counter
            self.x += 1

    # search_twitter: get tweets with event hashtag
    def search_media(self):
        posts = self.twitter.get_posts(self.HASHTAG) + self.twitter.get_dms(self.HASHTAG) + self.instagram.get_posts(self.HASHTAG)
        for post in posts:
            # Check if we've already processed the image
            if not any(x.id == post.id for x in self.pics):
                # Update Post object and save
                post.file_name = str(len(self.pics))+'.jpg'
                self.save_image(post)
                self.pics.append(post)
    
    # save_image: save image to AWS or to local storage        
    def save_image(self, post):
        # Get image bytes (use twitter client for direct message authentication)
        r = self.twitter.client.get(post.url)
        
        # Save to AWS
        self.aws.post_to_aws(post.file_name, r.content)

### Initialization ###
root = RootTk()
crowdshare = CrowdShare(root)
crowdshare.mainloop()
