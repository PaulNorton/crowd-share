#
# csclient
# Paul Norton
#

### Imports ###
import pickle
from modules.cstwitter import CSTwitter
from modules.csinstagram import CSInstagram
from modules.csaws import CSAws

### CSClient - Custom Class ###
# Handles all the main functionality of the CrowdShare app
class CSClient():
    def __init__(self):
        # Import configuration created by setup.py
        config = pickle.load( open( "config.p", "rb" ) )

        # Constants
        self.HASHTAG = config['hashtag']

        # Twitter
        self.twitter = CSTwitter(config['app_key'], config['app_secret'], config['oauth_token'], config['oauth_token_secret'])

        # Instagram
        self.instagram = CSInstagram(config['access_token'])

        # Amazon Web Service
        self.aws = CSAws(config['aws_access_key_id'], config['aws_secret_access_key'], self.HASHTAG)

        # Set up other attributes
        self.x = 0
        self.pics = []

    # search_twitter: get tweets with event hashtag
    def search_media(self):
        tweets = self.twitter.get_posts(self.HASHTAG)
        dms = self.twitter.get_dms(self.HASHTAG)
        instas = self.instagram.get_posts(self.HASHTAG)

        posts =  tweets + dms + instas

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

    # rotate_image: Rotate image on the window
    def get_next_image(self):
        success = False
        bytes = None
        message = ""

        # Make sure we have pictures
        if len(self.pics) > 0:
            success = True

            # Reset counter if necessary
            if self.x == len(self.pics):
                self.x = 0
            
            # Get next post
            post = self.pics[self.x]

            # Retrieve picture from AWS
            bytes = self.aws.retrieve_from_aws(post.file_name)

            message = post.message
            
            self.x += 1

        return { 'success': success, 'bytes': bytes, 'message': message }            