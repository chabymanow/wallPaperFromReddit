import requests
import json
import os
import win32api, win32con, win32gui
import urllib.request
import ctypes, winreg
import praw
from pathlib import Path

# Function to set the wallpaper for Windows 10
def SetWallPaper(picPath):
    # Set tile style to zero so Not tile the image. Wallpaper style set to 3 so fit to screen
    for k, v in {("TileWallpaper", "0"), ("WallpaperStyle", "3")}:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, winreg.KEY_WOW64_32KEY | winreg.KEY_WRITE)
        winreg.SetValueEx(key, k, 0, winreg.REG_SZ, v)
    ctypes.windll.user32.SystemParametersInfoW(win32con.SPI_SETDESKWALLPAPER, 0, os.path.abspath(picPath), win32con.SPIF_SENDWININICHANGE | win32con.SPIF_UPDATEINIFILE)
    print("Done! The wallpaper is changed.")

# Function for get an image from reddit
def getimg():
    # Set a variable to the current user`s Downloads folder
    downloads_path = str(Path.home() / "Downloads")
    # Check image in Earthporn subreddit. Limit setted to one so it is get only one image    
    all = reddit.subreddit('EarthPorn').new(limit=1)
    img = None
    for post in all:           
        print('The post\`s URL: ' + post.url)
        if str(post.url).endswith('.jpg'):
            try:
                response = urllib.request.urlopen(post.url)
                img = response.read()
            except:
                continue
    # Set te folder to the current user`s home Downloads folder and set the filename to wallpaper01.jpg
    fileName = downloads_path + '\\wallpaper.jpg'
    # Open the file for write in binary
    if img != None:
        with open(fileName,'wb') as f:
            # Write the image file
            f.write(img)
        # Close the file
        f.close()
        # Return with the saved file name and location
        return fileName
    else:
        print('Something wrong. I don`t have any image.')

SPI_SETDESKWALLPAPER    = 0x0014
SPI_SETDESKPATTERN      = 0x0015
SPIF_UPDATEINIFILE      = 0x01
SPIF_SENDWININICHANGE   = 0x02

# Reach Reddit with the client`s account
reddit = praw.Reddit(client_id="WriteYourIDHere",client_secret="WriteYourSecretCodeHere",user_agent="YourProgram`sName")

# Call the function with a function which is download a file from reddit and give back the file location
SetWallPaper(getimg())