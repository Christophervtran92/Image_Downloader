import tweepy   #For Twitter API
import requests #For downloading images
import json     #For importing Tokens from JSON
import os       #For pause before ending execution

tokens = json.load(open('tokens.json', 'r')) #Import tokens from JSON

#Set up authentication for twitter API
auth = tweepy.OAuth1UserHandler(
    tokens["api_Key"], tokens["api_Key_Secret"], tokens["access_Token"], tokens["access_Token_Secret"]
)
api = tweepy.API(auth)  #Ready the  API
tweets_Timeline = api.user_timeline(count=10)   #Grab the 10 latest tweets

#Print list of 10 most recent tweets
counter = 0
print("\n\tDate\t\t\t\tID\t\t\tURL\t\t\t\t\t\t\tHashtags")
for tweet in tweets_Timeline:
    temp_Tweet = api.get_status(tweet.id)                       #Store the current tweet being looked at
    temp_Id = str(temp_Tweet.entities["media"][0]['id'])        #Store the current media id
    temp_Url = str(temp_Tweet.entities["media"][0]['media_url'])#Store the current media url
    temp_Hashtags = temp_Tweet.entities["hashtags"]             #Store the current tweet hashtags
    hashtags_List = []                          #list to store all the hashtags
    for hashtag in temp_Hashtags:               #loop through the list of hashtags and store them
        hashtags_List.append(hashtag['text'])   #into hashtags_List
    print(str(counter) + ". " + temp_Tweet.created_at.ctime() + "\t" + temp_Id + "\t" + temp_Url + "\t\t" + str(hashtags_List)) #Print info for each tweet
    counter += 1

#Have the user select one of the tweets to download an image from and store the info of the tweets into variables
selection = input("Choose a image to download: (0-9)")
tweet_Date = tweets_Timeline[int(selection)].created_at.ctime()
tweet_ID = tweets_Timeline[int(selection)].entities["media"][0]['id']
tweet_Url = str(tweets_Timeline[int(selection)].entities["media"][0]['media_url'])
tweet_Hashtags = tweets_Timeline[int(selection)].entities["hashtags"]
hashtags = []
for hashtag in tweet_Hashtags:
    hashtags.append(hashtag['text'])

#Print the info for the user selected tweet and asks them if they want to download the image
print("\nYou selected:\n" + "\t\tDate: " + "\t\t" + tweet_Date + "\n\t\tID: " + "\t\t" + str(tweet_ID) + "\n\t\tURL: " + "\t\t" + tweet_Url + "\n\t\tHashtags: " + "\t" + str(hashtags))
selection = input("\nConfirm download: (y/n)")

#If they accept, go through with the download, otherwise end the program
if selection == 'y' or selection == 'Y':
    truncated_URL = tweet_Url[0:len(tweet_Url)-4]                               #Remove the file extension
    latest_Tweet_Media_URL_Lg = truncated_URL + "?format=jpg&name=4096x4096"    #Append option to get largest size possible up to 4096x4096

    location = "C:\\Users\\Chris\\Downloads\\"  #Location on computer to save image
    filename = str(tweet_ID)                    #Use the id of the media as the file name
    extension = ".jpg"                          #Append the extension of the file
    latest_Tweet_Media_Filename = location + filename + extension   #Combine location, filename, and extension for saving

    #Print information about the image being downloaded and then download it
    print("\n--- IMG NAME: " + filename + " ---\n" + "IMG SRC: " + latest_Tweet_Media_URL_Lg + "\nSAVE LOCATION: " + latest_Tweet_Media_Filename + "\n")
    img_data = requests.get(latest_Tweet_Media_URL_Lg).content
    with open(latest_Tweet_Media_Filename, 'wb') as handler:
        handler.write(img_data)
    os.system("pause")
else:
    print("Save declined")
    os.system("pause")
