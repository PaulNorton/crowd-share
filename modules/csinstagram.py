#
# csinstagram
# Paul Norton
#

### Imports ###
import requests
import json
from modules.cspost import CSPost

### CSInstagram - Custom Class ###
# Accesses Instagram API
class CSInstagram():
    def __init__(self, access_token):
        self.ACCESS_TOKEN = access_token

    def get_posts(self, hashtag):
        r = requests.get('https://api.instagram.com/v1/tags/' + hashtag + '/media/recent?access_token=' + self.ACCESS_TOKEN)
        json_data = json.loads(r.content.decode())
        data = json_data['data']
        posts = []

        for post in data:
            post = CSPost(id=post['id'], user_name=post['user']['username'], platform='instagram', file_name='', url=post['images']['standard_resolution']['url'], text=post['caption']['text'])
            posts.append(post)

        return posts

    def generate_url(self, client_id):
        return 'https://api.instagram.com/oauth/authorize/?client_id=' + client_id + '&redirect_uri=http://localhost&response_type=code&scope=public_content'

    def get_access_token(self, client_id, client_secret, code):
        url = 'https://api.instagram.com/oauth/access_token'
        post_fields = {'client_id': client_id, 'client_secret': client_secret, 'grant_type': 'authorization_code', 'redirect_uri': 'http://localhost', 'code': code }
        r = requests.post(url, post_fields)
        json_data = json.loads(r.content.decode())
        return json_data['access_token']