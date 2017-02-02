from tkinter import *
from twitter import *
from urllib.request import urlretrieve
from PIL import ImageTk, Image
import os
import shutil

class MyTk(Tk):
    def __init__(self, master=None):
        Tk.__init__(self, master)
        
        file = open('bearer_token.txt', 'r')
        self.BEARER_TOKEN = file.read()
        file.close()
        
        self.HASHTAG = 'crowdsharethesisproject'

        self.twitter = Twitter(auth=OAuth2(bearer_token=self.BEARER_TOKEN))

        self.x = 1
        self.pics = []

        self.panel = Label(self)
        self.panel.pack(side = 'bottom', fill = 'both', expand = 'yes')

        self.id = self.after(3000, self.callback)

    def callback(self):
        self.search_twitter()
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

if os.path.isdir('img'):
    shutil.rmtree('img')
os.makedirs('img')

root = MyTk()
root.attributes('-fullscreen', True)

root.mainloop()
