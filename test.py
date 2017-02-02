from tkinter import *
from twitter import *
from PIL import ImageTk, Image
import time

class MyTk(Tk):
    def __init__(self, master=None):
        Tk.__init__(self, master)
        
        file = open("bearer_token.txt", "r")
        self.BEARER_TOKEN = file.read()
        file.close()
        
        self.HASHTAG = "crowdsharethesisproject"

        self.twitter = Twitter(auth=OAuth2(bearer_token=self.BEARER_TOKEN))

        self.x = 1
        self.pics = []

        self.panel = Label(self)
        self.panel.pack(side = "bottom", fill = "both", expand = "yes")

        self.set_image()

        self.id = self.after(2000, self.callback)

    def callback(self):
        self.x += 1
        
        
        if self.x == 5:
            self.x = 1

        self.set_image()
        self.search_twitter()
        
        #You can cancel the call by doing "self.after_cancel(self.id)"
        self.id = self.after(2000, self.callback)

    def set_image(self):
        

        img = ImageTk.PhotoImage(Image.open("img/" + str(self.x) + ".jpg"))
        self.panel.configure(image = img)
        self.panel.image = img

    def search_twitter(self):
        print(self.pics)

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


root = MyTk()
root.attributes("-fullscreen", True)

root.mainloop()
