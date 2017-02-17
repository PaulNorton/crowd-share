#
# instagram
# Paul Norton
#

### Imports ###
import requests
import json
from modules.post import Post

### Instagram - Custom Class ###
# Accesses Instagram API
class Instagram():
    def __init__(self, access_token):
        self.ACCESS_TOKEN = access_token

    def get_posts(self, hashtag):
        r = requests.get('https://api.instagram.com/v1/tags/' + hashtag + '/media/recent?access_token=' + self.ACCESS_TOKEN)
        json_data = json.loads(r.content.decode())
        data = json_data['data']
        posts = []

        for post in data:
            post = Post(id=post['id'], user_name=post['user']['username'], platform='instagram', file_name='', url=post['images']['standard_resolution']['url'], text=post['caption']['text'])
            posts.append(post)

        return posts