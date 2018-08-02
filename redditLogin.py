import praw

import config


reddit = praw.Reddit(client_id=config.client_id,
                     client_secret=config.client_secret,
                     user_agent='My testBot',
                     username=config.username,
                     password=config.password)

#botCall = '!toImgur'

for comment in reddit.subreddit('pics').stream.comments():
