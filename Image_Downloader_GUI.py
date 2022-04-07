from turtle import window_width
import tweepy   #For Twitter API
import requests #For downloading images
import json     #For importing Tokens from JSON
import os       #For pause before ending execution
from tkinter import *           #For GUI
from tkinter import ttk
from PIL import ImageTk, Image  #For images
from io import BytesIO

def gui(tokens):
    auth = tweepy.OAuth1UserHandler(
        tokens["api_Key"], tokens["api_Key_Secret"], tokens["access_Token"], tokens["access_Token_Secret"]
    )
    api = tweepy.API(auth)  #Ready the API
    tweets_Timeline = api.user_timeline(count=10)   #Grab the 10 latest tweets
    images = []     #Empty array to hold all the image URLs
    for tweet in tweets_Timeline:
        images.append(str(api.get_status(tweet.id).entities["media"][0]["media_url"]))

    window = Tk(screenName="Image Downloader", baseName=None, className="Image Downloader", useTk=1)
    window.geometry('800x900')

    menu = Menu(window)
    window.config(menu=menu)

    fileMenu = Menu(menu)
    menu.add_cascade(label="File", menu=fileMenu)
    fileMenu.add_command(label="Exit", command=window.quit)

    helpMenu = Menu(menu)
    menu.add_cascade(label="Help", menu=helpMenu)
    helpMenu.add_command(label="Instructions")
    helpMenu.add_command(label="About")

    maxsize = (500, 500)
    thumbnails = []
    for url in images:
        imageURL = requests.get(url)
        picture = Image.open(BytesIO(imageURL.content))
        picture.thumbnail(maxsize, Image.ANTIALIAS)
        thumbnails.append(ImageTk.PhotoImage(picture))

    frame = Frame(window, width=700, height=850)
    frame.pack(expand=True, fill=BOTH)

    canvas = Canvas (frame, bg="#1da1f2", width=700, height=850, scrollregion=(0,0,900, 300 * len(thumbnails)))

    scrollbar = Scrollbar(frame, orient=VERTICAL)
    scrollbar.pack(side=RIGHT, fill=Y)
    scrollbar.config(command=canvas.yview)
    canvas.config(width=800, height=200)
    canvas.config(yscrollcommand=scrollbar.set)
    canvas.pack(expand=True, side=LEFT, fill=BOTH)

    padding = 150
    row = 0
    for thumbnail in thumbnails:
        infoFrame = Frame()
        label = Label(infoFrame, image=thumbnail).grid(row=row, column=0, columnspan=3)
        downloadBtn = Button(infoFrame, text="Download", width=15, height=4).grid(row=row, column=4, columnspan=2, padx="70")
        infoFrame.pack()
        #label.pack()
        canvas.create_window(390, padding, window=infoFrame)
        padding += 300
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