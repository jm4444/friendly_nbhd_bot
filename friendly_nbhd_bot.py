"""

friendly_nbhd_bot

a reddit bot for monitoring r/thenbhd

project started May 15, 2018

"""



#  -  -  -  -  -  -  -  -  -  -  -  -  - IMPORT -  -  -  -  -  -  -  -  -  -  -  -  -  #

import praw, os
import private_variables as pv
from time import time, sleep, localtime, strftime
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError



#  -  -  -  -  -  -  -  -  -  -  -  -  - VARIABLES -  -  -  -  -  -  -  -  -  -  -  -  -  #

reddit = praw.Reddit(client_id = pv.client_id,
                     client_secret = pv.client_secret,
                     password = pv.password,
                     user_agent = 'a bot for monitoring /r/thenbhd by /u/scratch_pad',
                     username = 'friendly_nbhd_bot')

youtube = build("youtube", "v3", developerKey = pv.youtube_api_key)

nbhd_subreddit = reddit.subreddit('ScratchpadsScratchpad')    # Currently set to a personal subreddit for development



#  -  -  -  -  -  -  -  -  -  -  -  -  - CLASSES -  -  -  -  -  -  -  -  -  -  -  -  -  #

class YouTubeChannel:
    def __init__(self, channel_name, uploads_playlist):
        self.channel_name = channel_name
        self.uploads_playlist = uploads_playlist

        self.number_of_uploads = youtube.playlistItems().list(part="snippet, ContentDetails", maxResults=3, playlistId=uploads_playlist).execute()['pageInfo']['totalResults']
        print(self.number_of_uploads)



#  -  -  -  -  -  -  -  -  -  -  -  -  - RUNNING THE BOT -  -  -  -  -  -  -  -  -  -  -  -  -  #

print(reddit.user.me())    # Checks to make sure the bot has successfully logged into Reddit

nbhd_youtube_channel = YouTubeChannel("The Neighbourhood", "UUDAXusYwRJpiSP2CHnXnVnw")
nbhd_vevo_channel = YouTubeChannel("TheNeighbourhoodVEVO", "UUJRqaM_C1asb8fq-zeSps0w")
jesse_vevo_channel = YouTubeChannel("JesseRutherfordVEVO", 'UUghSc9_3AD8eLqfYvf01BnA')

# nbhd_subreddit.submit('Test Post', 'Hello Reddit :)', url = None)    # Code for submitting a post to the subreddit
