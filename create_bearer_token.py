from twitter import *

consumer_key = input("Enter your consumer key: ")
consumer_secret = input("Enter your consumer secret: ")

bearer_token = oauth2_dance(consumer_key, consumer_secret)

file = open("bearer_token.txt", "w")
file.write(bearer_token)
file.close()