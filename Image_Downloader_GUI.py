from turtle import window_width
import tweepy   #For Twitter API
import requests #For downloading images
import json     #For importing Tokens from JSON
from tkinter import *           #For GUI
from tkinter import ttk
from PIL import ImageTk, Image  #For images
from io import BytesIO

def gui(tokens):
    auth = tweepy.OAuth1UserHandler(
        tokens["api_Key"], tokens["api_Key_Secret"], tokens["access_Token"], tokens["access_Token_Secret"]
    )
    api = tweepy.API(auth)                          #Ready the API
    tweets_Timeline = api.user_timeline(count=10)   #Grab the 10 latest tweets
    imagesId = []
    imagesUrl = []                                  #Empty array to hold all the image URLs
    imageCreationTime = []
    imagesHashtags = []
    for tweet in tweets_Timeline:                   #Loop through and load the urls for images from tweets
        imagesId.append(str(api.get_status(tweet.id).entities["media"][0]['id']))
        imagesUrl.append(str(api.get_status(tweet.id).entities["media"][0]["media_url"]))
        imageCreationTime.append(api.get_status(tweet.id).created_at.ctime())
        tempHashtag = api.get_status(tweet.id).entities["hashtags"]
        hashtagArray = []
        for hashtag in tempHashtag:
            hashtagArray.append(hashtag['text'])
        imagesHashtags.append(hashtagArray)

    #Create the window for the application
    window = Tk(screenName="Image Downloader", baseName=None, className="Image Downloader", useTk=1)
    window.geometry('1000x900')
    window.title("Image Downloader")

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

    maxsize = (600, 600)
    thumbnails = []
    for url in imagesUrl:
        imageURL = requests.get(url)
        picture = Image.open(BytesIO(imageURL.content))
        picture.thumbnail(maxsize, Image.Resampling.LANCZOS)
        thumbnails.append(ImageTk.PhotoImage(picture))

    #Frame to hold the canvas and scrollbar
    frame = Frame(window, width=700, height=850)
    frame.pack(expand=True, fill=BOTH)

    #scroll region (approx height of frames) * len(thumbnails) where thumbnails array of images
    canvas = Canvas (frame, bg="#1da1f2", width=700, height=850, scrollregion=(0,0,900, 375 * len(thumbnails)))

    #Create a vertical scrollbar and place it on the RHS of frame, bind it to scroll canvas vertically
    scrollbar = Scrollbar(frame, orient=VERTICAL)
    scrollbar.pack(side=RIGHT, fill=Y)
    scrollbar.config(command=canvas.yview)

    #Configure the scroll of the canvas to be controlled by scrollbar, place on frame LHS
    #Canvas size seems to be dictated by the widgets placed inside
    canvas.config(yscrollcommand=scrollbar.set)
    canvas.pack(expand=True, side=LEFT, fill=BOTH)

    padding = 190   #Increase default padding for top most frame
    row = 0
    for thumbnail in thumbnails:
        infoFrame = LabelFrame(text=" " + imagesUrl[row] + " ", font=("Arial", 12)) #Parent frame for L&R frames
        leftFrame = Frame(infoFrame)    #lhs frame to hold thumbnail image
        leftFrame.pack(side = LEFT)     #place it on the lhs of infoFrame
        rightFrame = Frame(infoFrame)   #rhs frame to hold information and dl button
        rightFrame.pack(side = RIGHT)   #place it on the rhs of infoFrame
        label = Label(infoFrame, image=thumbnail)   #Label to display the thumbnail image
        label.pack(side = LEFT)                     #Place it on lhs of infoFrame
        infoBox = Text(rightFrame, width=35, height=16, padx=5)
        description = ( "Id:\n" + imagesId[row] +
                        "\n\nCreated at:\n" + imageCreationTime[row]  +
                        "\n\nHashtags: " + str(imagesHashtags[row]))
        infoBox.insert(END, description)
        infoBox.config(state="disabled")
        infoBox.pack(side = TOP, padx=5) #Place the infoBox on the top side of the right frame
        downloadBtn = Button(rightFrame, text="Download", width=20, height=2)
        downloadBtn.pack(side = BOTTOM, anchor="s", pady=15) #Placed at bottom of RHS of infoFrame, padding away from infoBox
        canvas.create_window(475, padding, window=infoFrame) #first number adjusts the lhs padding for each window
        padding += 370  #Adjust padding increment as needed to add spacing between frames
        row += 1

    # canvas = Canvas(window)
    # canvas.grid()
    # canvas.pack()

    # row = 0
    # for thumbnail in thumbnails:
    #     label = Label(canvas, image=thumbnail).grid(row=row, column = 0)
    #     downloadBtn = Button(canvas, text="Download", width=15, height=4).grid(row=row, column=4, columnspan=2, padx="100")
    #     row += 1

    # scrollbar = Scrollbar(window, orient=VERTICAL)
    # scrollbar.pack()
    # canvas.config(yscrollcommand = scrollbar.set)
    # scrollbar.config(command=canvas.yview)

    # label = Label(image=thumbnails[0])
    # label.grid(row=0, column=0, columnspan=3)
    # downloadBtn = Button(window, text="Download", width=15, height=4)
    # downloadBtn.grid(row=0, column=4, columnspan=2, padx="100")
    # label2 = Label(image=thumbnails[1])
    # label2.grid(row=1, column=0, columnspan=3)
    # downloadBtn2 = Button(window, text="Download", width=15, height=4)
    # downloadBtn2.grid(row=1, column=4, columnspan=2, padx="100")
    # label3 = Label(image=thumbnails[2])
    # label3.grid(row=2, column=0, columnspan=3)
    # downloadBtn3 = Button(window, text="Download", width=15, height=4)
    # downloadBtn3.grid(row=2, column=4, columnspan=2, padx="100")
    # label4 = Label(image=thumbnails[3])
    # label4.grid(row=3, column=0, columnspan=3)
    # downloadBtn4 = Button(window, text="Download", width=15, height=4)
    # downloadBtn4.grid(row=3, column=4, columnspan=2, padx="100")
    # label5 = Label(image=thumbnails[4])
    # label5.grid(row=4, column=0, columnspan=3)
    # downloadBtn5 = Button(window, text="Download", width=15, height=4)
    # downloadBtn5.grid(row=4, column=4, columnspan=2, padx="100")

    window.mainloop()

gui(json.load(open('tokens.json', 'r')))