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

friendly_nbhd_bot = praw.Reddit(client_id = pv.client_id,
                     client_secret = pv.client_secret,
                     password = pv.password,
                     user_agent = 'a bot for monitoring /r/thenbhd by /u/scratch_pad',
                     username = 'friendly_nbhd_bot')

nbhd_subreddit = friendly_nbhd_bot.subreddit('ScratchpadsScratchpad')



#  -  -  -  -  -  -  -  -  -  -  -  -  - RUNNING THE BOT -  -  -  -  -  -  -  -  -  -  -  -  -  #

print(friendly_nbhd_bot.user.me())    # Checks to make sure the bot has successfully logged into Reddit

# nbhd_subreddit.submit('Test Post', 'Hello Reddit :)', url = None)    # Code for submitting a post to the subreddit
