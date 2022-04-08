import tweepy   #For Twitter API
import requests #For downloading images
import json     #For importing Tokens from JSON
from tkinter import *   #For GUI
from tkinter import messagebox
from PIL import ImageTk, Image  #For images
from io import BytesIO
from winreg import *

# Function:     download
# Description:  Helper function to handle the download functionality of the program, called when the Download button is pressed
#               on the GUI. It then downloads the image associated with that particular download button and saves to the
#               download folder. Currently only supports Windows.
# Argument(s):  info:   JSON with tweet information used to generate info on the download info messagebox and location to
#                       download the image from
def download(info):
    # From: https://www.reddit.com/r/learnpython/comments/4dfh1i/how_to_get_the_downloads_folder_path_on_windows/
    # Get user Download folder for saving
    with OpenKey(HKEY_CURRENT_USER, 'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders') as key:
        location = QueryValueEx(key, '{374DE290-123F-4565-9164-39C4925E467B}')[0]
    filename = info["id"]
    extension = ".jpg"
    save_Location = location + "\\" + filename + extension
    truncated_Url = info["url"][0:len(info["url"])-4]
    media_Url_Lg = truncated_Url + "?format=jpg&name=4096x4096"
    print("File: " + save_Location)
    img_Data = requests.get(media_Url_Lg).content
    with open(save_Location, 'wb') as handler:
        handler.write(img_Data)
    download_Info = ("\nFilename:\n" + filename + extension +
                    "\n\nSave Location:\n" + save_Location)
    messagebox.showinfo("Download Info", download_Info)

# Function:     gui
# Description:  Displays a GUI with large thumbnails, information, and download buttons for images from twitter tweets
# Argument(s):  tokens: JSON file with twitter authentication keys
def gui(tokens):
    #Create the window for the application
    window = Tk(screenName="Image Downloader", baseName=None, className="Image Downloader", useTk=1)
    window.geometry('1000x900')
    window.title("Image Downloader")

    #Authenticate the twitter account with info from tokens.json
    auth = tweepy.OAuth1UserHandler(
        tokens["api_Key"], tokens["api_Key_Secret"], tokens["access_Token"], tokens["access_Token_Secret"]
    )
    api = tweepy.API(auth)                          #Ready the API
    tweets_Timeline = api.user_timeline(count=10)   #Grab the 10 latest tweets
    
    #Loop through and add tweet info into a JSON and store it into details array
    detailsArray = []
    for tweet in tweets_Timeline:
        tempHashtag = api.get_status(tweet.id).entities["hashtags"]
        hashtagArray = []
        for hashtag in tempHashtag:
            hashtagArray.append(hashtag['text'])
        url = str(api.get_status(tweet.id).entities["media"][0]["media_url"])
        maxsize = (600, 600)
        imageURL = requests.get(url)
        picture = Image.open(BytesIO(imageURL.content))
        picture.thumbnail(maxsize, Image.Resampling.LANCZOS)

        #Store id, url, time created, and thumbnail into a JSON for current tweet and append to detailsArray
        infoJSON = {"id": str(api.get_status(tweet.id).entities["media"][0]['id']),
                    "url": str(api.get_status(tweet.id).entities["media"][0]["media_url"]),
                    "time":  api.get_status(tweet.id).created_at.ctime(),
                    "hashtags": hashtagArray,
                    "thumbnail": ImageTk.PhotoImage(picture)}
        detailsArray.append(infoJSON)

    #Create the menu for the application
    menu = Menu(window)
    window.config(menu=menu)

    #Start with a file menu with an exit button, add additional buttons as needed
    fileMenu = Menu(menu)
    menu.add_cascade(label="File", menu=fileMenu)
    fileMenu.add_command(label="Exit", command=window.quit)

    #Create a help menu with instructions and about button
    helpMenu = Menu(menu)
    menu.add_cascade(label="Help", menu=helpMenu)
    helpMenu.add_command(label="Instructions")
    helpMenu.add_command(label="About")

    #Frame to hold the canvas and scrollbar
    frame = Frame(window, width=700, height=850)
    frame.pack(expand=True, fill=BOTH)

    #scroll region (approx height of frames) * len(thumbnails) where thumbnails array of images
    canvas = Canvas (frame, bg="#1da1f2", width=700, height=850, scrollregion=(0,0,900, 371 * len(detailsArray)))

    #Create a vertical scrollbar and place it on the RHS of frame, bind it to scroll canvas vertically
    scrollbar = Scrollbar(frame, orient=VERTICAL)
    scrollbar.pack(side=RIGHT, fill=Y)
    scrollbar.config(command=canvas.yview)

    #Configure the scroll of the canvas to be controlled by scrollbar, place on frame LHS
    #Canvas size seems to be dictated by the widgets placed inside
    canvas.config(yscrollcommand=scrollbar.set)
    canvas.pack(expand=True, side=LEFT, fill=BOTH)

    padding = 190   #Increase default padding for top most frame
    for details in detailsArray:
        infoFrame = LabelFrame(text=" " + details["url"] + " ", font=("Arial", 12)) #Parent frame for L&R frames
        leftFrame = Frame(infoFrame)    #lhs frame to hold thumbnail image
        leftFrame.pack(side = LEFT)     #place it on the lhs of infoFrame
        rightFrame = Frame(infoFrame)   #rhs frame to hold information and dl button
        rightFrame.pack(side = RIGHT)   #place it on the rhs of infoFrame
        label = Label(infoFrame, image=details["thumbnail"])   #Label to display the thumbnail image
        label.pack(side = LEFT)                     #Place it on lhs of infoFrame
        infoBox = Text(rightFrame, width=35, height=16, padx=5)
        description = ( "Id:\n" + details['id'] +
                            "\n\nCreated on:\n" + details['time'] +
                            "\n\nHashtags: " + str(details["hashtags"]))
        infoBox.insert(END, description)
        infoBox.config(state="disabled")
        infoBox.pack(side = TOP, padx=5) #Place the infoBox on the top side of the right frame

        #Info for making unique buttons on each loop found here: 
        #https://stackoverflow.com/questions/10865116/tkinter-creating-buttons-in-for-loop-passing-command-arguments
        downloadBtn = Button(rightFrame, text="Download", width=20, height=2, command= lambda details=details: download(details, window))
        downloadBtn.pack(side = BOTTOM, anchor="s", pady=15) #Placed at bottom of RHS of infoFrame, padding away from infoBox
        canvas.create_window(475, padding, window=infoFrame) #first number adjusts the lhs padding for each window
        padding += 370  #Adjust padding increment as needed to add spacing between frames

    window.mainloop()

gui(json.load(open('tokens.json', 'r')))