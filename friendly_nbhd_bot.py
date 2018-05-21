"""

friendly_nbhd_bot

a reddit bot for monitoring r/thenbhd

project started May 15, 2018

"""


#  -  -  -  -  -  -  -  -  -  -  -  -  - SETUP -  -  -  -  -  -  -  -  -  -  -  -  -  #

import praw, private_variables as pv

friendly_nbhd_bot = praw.Reddit(client_id = pv.client_id,
                     client_secret = pv.client_secret,
                     password = pv.password,
                     user_agent = 'a bot for monitoring /r/thenbhd by /u/scratch_pad',
                     username = 'friendly_nbhd_bot')

nbhd_subreddit = friendly_nbhd_bot.subreddit('ScratchpadsScratchpad')

print(friendly_nbhd_bot.user.me())    # Checks to make sure the bot has successfully logged into Reddit

# nbhd_subreddit.submit('Test Post', 'Hello Reddit :)', url = None)    # Code for submitting a post to the subreddit
