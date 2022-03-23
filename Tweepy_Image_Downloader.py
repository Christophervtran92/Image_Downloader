import tweepy   #For Twitter API
import requests #For downloading images
import json     #For importing Tokens from JSON

tokens = json.load(open('tokens.json', 'r')) #Import tokens from JSON

#Set up authentication for twitter API
auth = tweepy.OAuth1UserHandler(
    tokens["api_Key"], tokens["api_Key_Secret"], tokens["access_Token"], tokens["access_Token_Secret"]
)
api = tweepy.API(auth)  #Ready the  API

tweets_Timeline = api.user_timeline()   #retrieve the user timeline
latest_Tweet_ID = tweets_Timeline[0].id #retrieve the id of the first tweet
latest_Tweet = api.get_status(latest_Tweet_ID)  #retrieve status information about the tweet
latest_Tweet_Media = latest_Tweet.entities["media"] #grab media properties from entities
latest_Tweet_Media_URL = latest_Tweet_Media[0]['media_url'] #grab the url of the image
truncated_URL = latest_Tweet_Media_URL[0:len(latest_Tweet_Media_URL)-4] #Remove the file extension
latest_Tweet_Media_URL_Lg = truncated_URL + "?format=jpg&name=4096x4096" #Append option to get largest size possible up to 4096x4096

location = "C:\\Users\\Chris\\Downloads\\"  #Location on computer to save image
filename = str(latest_Tweet_Media[0]['id']) #Use the id of the media as the file name
extension = ".jpg"                          #Append the extension of the file
latest_Tweet_Media_Filename = location + filename + extension   #Combine location, filename, and extension for saving

#Print information about the image being downloaded and then download it
print("\n---IMG NAME: " + filename + " ---\n" + "IMG SRC: " + latest_Tweet_Media_URL_Lg + "\nSAVE LOCATION: " + latest_Tweet_Media_Filename + "\n")
img_data = requests.get(latest_Tweet_Media_URL_Lg).content
with open(latest_Tweet_Media_Filename, 'wb') as handler:
    handler.write(img_data)