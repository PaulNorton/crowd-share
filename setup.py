import json
import requests

print('Welcome to CrowdShare. This script will help you set up your CrowdShare service.')
print('')
print('First of all, you must set up a Twitter developer account and register a Twitter app at https://dev.twitter.com')
print('When registration is complete, go to Permissions and make sure the app can read and write direct messages.')
print('Under Keys and Access Tokens, generate an access token and secret.')
print('On the Twitter account you set up the app under, be sure to change your privacy settings to allow anyone to send you direct messages.')
print('Finally, then enter the app information.')
print('')

app_key = input('Enter your consumer key: ').strip()
app_secret = input('Enter your consumer secret: ').strip()
oauth_token = input('Enter your access token: ').strip()
oauth_token_secret = input('Enter your access token secret: ').strip()

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
print('If you have not already, please install the AWS CLI and configure a default profile at ~/.aws/credentials')
input('Press enter when complete: ')

print('')
hashtag = input('Enter your event hashtag: ').strip()

print('')
print('Writing data to file...')
data = {
        'app_key': app_key,
        'app_secret': app_secret,
        'oauth_token': oauth_token,
        'oauth_token_secret': oauth_token_secret,
        'access_token': access_token,
        'hashtag': hashtag,
        'aws': True
}
file = open('config.json', 'w')
file.write(json.dumps(data))
file.close()

print('')
print('Setup complete! You may now run the app by typing `python3 crowdshare.py`')
