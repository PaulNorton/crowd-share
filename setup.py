from twitter import *
import json
import requests

print('Welcome to CrowdShare. This program will help you set up your CrowdShare service.')
print('')
print('First of all, you must set up a Twitter developer account and register a Twitter app at https://dev.twitter.com')
print('When registration is complete, enter the app information.')
print('')

consumer_key = input('Enter your consumer key: ').strip()
consumer_secret = input('Enter your consumer secret: ').strip()

print('')
print('Getting your bearer token...')

bearer_token = oauth2_dance(consumer_key, consumer_secret)

print('')
print('Next, you must set up an Instagram developer account at https://www.instagram.com/developer/')
print('Register an app and set the redirect uri to http://localhost')
print('')

client_id = input('Enter your client id: ').strip()
client_secret = input('Enter your client secret: ').strip()

url = 'https://api.instagram.com/oauth/authorize/?client_id=' + client_id + '&redirect_uri=http://localhost&response_type=code&scope=public_content'

print('Next, paste the following url into your browser and authorize the app:')
print(url)

print('')
print('When the browser redirects, copy the code it returns.')
print('')

code = input('Enter your code: ').strip()

print('')
print('Getting your access token...')

url = 'https://api.instagram.com/oauth/access_token'
post_fields = {'client_id': client_id, 'client_secret': client_secret, 'grant_type': 'authorization_code', 'redirect_uri': 'http://localhost', 'code': code }
r = requests.post(url, post_fields)
json_data = json.loads(r.content.decode())
access_token = json_data['access_token']

print('')
hashtag = input('Enter your event hashtag: ').strip()

print('')
print('Writing data to file...')
data = { 'bearer_token': bearer_token, 'access_token': access_token, 'hashtag': hashtag }
file = open('.config', 'w')
file.write(json.dumps(data))
file.close()

print('')
print('Setup complete! You may now run the app by typing `python3 crowdshare.py`')
