#
# twitter
# Paul Norton
#

### Imports ###
from twython import *
from modules.post import Post

### Twitter - Twython Class Extension ###
# Mirrors Twython capability
class Twitter(Twython):
    def __init__(self, app_key, app_secret, oauth_token, oauth_token_secret):
        Twython.__init__(self, app_key, app_secret, oauth_token, oauth_token_secret)

    def get_posts(self, hashtag):
        # Call twitter API
        tweets = self.search(q='#'+hashtag)
        posts = []
        
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
                    post = Post(id=item['id'], user_name=status['user']['screen_name'], platform='twitter', file_name='', url=item['media_url_https'], text=status['text'])
                    posts.append(post)

        return posts

    def get_dms(self, hashtag):
        # Call twitter API
        dms = self.get_direct_messages()
        posts = []
        
        # Cycle through messages
        for dm in dms:
            # Check if there are media attached
            try:
                media = dm['entities']['media']
            except:
                continue
            
            # Ensure DM contains hashtag
            if hashtag in dm['text']:
                # Cycle through media and get photos
                for item in media:
                    if item['type'] == 'photo':
                        post = Post(id=item['id'], user_name=dm['sender']['screen_name'], platform='twitter', file_name='', url=item['media_url_https'], text=dm['text'])
                        posts.append(post)

        return posts
