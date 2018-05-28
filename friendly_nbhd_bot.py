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

verbose = True    # Setting to false suppresses mundane information and most warnings



#  -  -  -  -  -  -  -  -  -  -  -  -  - FUNCTIONS -  -  -  -  -  -  -  -  -  -  -  -  -  #

# A decorator that ensures the playlist functions will execute until they get a response
def ensure_connection(f):
    def g(*args, **kwargs):
        timer = 1
        while True:
            try:
                return f(*args, **kwargs)
            except:
                verbose("Warning! Connection error while getting playlist items!")
                verbose("Retrying in %d seconds..." % (timer))
                sleep(timer)
                timer *= 2
    return g


@ensure_connection
def get_playlist_items(youtube, uploads_playlist):
    https = youtube.playlistItems().list(part = "snippet, contentDetails", maxResults = 50, playlistId = uploads_playlist)
    return https, https.execute()


@ensure_connection
def get_next_playlist_page(youtube, https, uploads):
    https = youtube.playlistItems().list_next(https, uploads)
    return https, https.execute()


def verbose(s, override = True):    # Provides a time stamp when an error occurs
    time_stamp = "[%s]:" % (strftime("%I:%M:%S %p",localtime(time())))

    if verbose or override:
        print(time_stamp, s)



#  -  -  -  -  -  -  -  -  -  -  -  -  - CLASSES -  -  -  -  -  -  -  -  -  -  -  -  -  #

class YouTubeChannel:

    def __init__(self, channel_name, uploads_playlist):
        self.channel_name = channel_name
        self.uploads_playlist = uploads_playlist
        self.number_of_uploads = youtube.playlistItems().list(part = "snippet, ContentDetails", maxResults=3, playlistId = uploads_playlist).execute()['pageInfo']['totalResults']
        print(self.channel_name + " has uploaded " + str(self.number_of_uploads) + " videos.")
        self.store_all_upload_ids()
        print("There are " + str(len(self.upload_ids)) + " upload IDs.")


    def store_all_upload_ids(self):
        self.upload_ids = []    # Keeps track of all previously uploaded videos
        self.new_uploads = set()    # Temporarily holds new uploads until they are posted
        https, uploads = get_playlist_items(youtube, self.uploads_playlist)
        more_videos = True

        while more_videos:

            for item in uploads['items']:    # Adds the video ID of every video to the upload_ids variable
                upload_id = item['contentDetails']['videoId']
                self.upload_ids.append(upload_id)

            if len(self.upload_ids) >= self.number_of_uploads:    # Ends the loop once every ID is known and stored
                more_videos = False

            if 'nextPageToken' in uploads.keys():    # Goes to the next page of uploads, if there is one
                https, uploads = get_next_playlist_page(youtube, https, uploads)
            elif more_videos:
                verbose('Warning: Loop reached while generating video list!', override=False)
                https, uploads = get_playlist_items(youtube, self.upload_IDs)


    def get_new_video(self, youtube):    # This function checks if the total number of videos in the upload playlist has increased, and returns the new videos if so
        https, uploads = get_playlist_items(youtube, self.uploads_playlist)
        current_number_of_uploads = uploads['pageInfo']['totalResults']
        if current_number_of_uploads <= self.number_of_uploads:    # Ends the function if there are no new videos
            return
        new_number_of_uploads = current_number_of_uploads - self.number_of_uploads
        self.number_of_uploads = current_number_of_uploads
        i = 0

        while i < new_number_of_uploads:

            for item in uploads['items']:    # Searches each page of the playlist for new videos until it has found them all
                upload_id = item['contentDetails']['videoId']

                if upload_id not in self.upload_ids:
                    title = item['snippet']['title']
                    url = "https://www.youtube.com/watch?v=%s" % (upload_id)
                    self.upload_ids.append(upload_id)
                    self.new_uploads.add((title, url))
                    i += 1

            if 'nextPageToken' in uploads.keys():    # Loads the next page if there is one
                https, uploads = get_next_playlist_page(youtube, https, uploads)
            elif i < new_number_of_uploads:
                verbose('Warning: Loop reached while searching for latest video!', override = False)
                https, uploads = get_playlist_items(youtube, self.uploads_playlist)


    def post_new_video(self, youtube):
        self.get_new_video(youtube)
        if self.new_uploads:
            verbose("Found new content uploaded by %s!" % (self.channel_name))
            for video in self.new_uploads.copy():
                try:
                    nbhd_subreddit.submit(title = video[VID_TITLE], url = video[VID_URL], resubmit = True, send_replies = False)
                    self.new_uploads.remove(video)
                    verbose('Submitted video \"%s\"' % (video[VID_TITLE]))
                except Exception as e:
                    verbose(e)
        else:
            verbose("No new uploads found for channel %s." % (self.channel_name), override = False)



#  -  -  -  -  -  -  -  -  -  -  -  -  - RUNNING THE BOT -  -  -  -  -  -  -  -  -  -  -  -  -  #

print(reddit.user.me())    # Checks to make sure the bot has successfully logged into Reddit

nbhd_youtube_channel = YouTubeChannel("The Neighbourhood", "UUDAXusYwRJpiSP2CHnXnVnw")
nbhd_vevo_channel = YouTubeChannel("TheNeighbourhoodVEVO", "UUJRqaM_C1asb8fq-zeSps0w")
jesse_vevo_channel = YouTubeChannel("JesseRutherfordVEVO", 'UUghSc9_3AD8eLqfYvf01BnA')

# nbhd_subreddit.submit('Test Post', 'Hello Reddit :)', url = None)    # Code for submitting a post to the subreddit
