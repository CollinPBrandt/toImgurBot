import praw

import config

from imgurpython import ImgurClient

import imgurConfig

from time import sleep

def runBot():
    reddit = redditLogin()
    client = imgurLogin()

    print('Searching Comments for !toImgur...\n')
    botCall = '!toImgur'
    for comment in reddit.subreddit('test').stream.comments():
        if botCall in comment.body:
            print('!toImgur found in comments...')
            if comment.submission.url in open('redditURLs.txt', 'r').read():    # if submission already recorded
                print('This submission has already been mirrored\n')
            elif comment.submission.url is 'None':                              # if a self post
                print('This submission does not contain an image')
            elif 'imgur.com' not in comment.submission.url:                     # if url is not already imgur
                print('Comment post is not hosted by imgur, creating mirror...')
                postSubmissionToImgur(client, comment.submission)
                returnLinkToCallComment(client, comment)
            else:                                                               # if url is already imgur
                print('Comment submission is already hosted by imgur.\n')


def redditLogin():
    print('Logging in to reddit...')
    r = praw.Reddit(client_id=config.client_id,
                    client_secret=config.client_secret,
                    user_agent='My testBot',
                    username=config.username,
                    password=config.password)
    print('Logged in to reddit\n')
    return r


def imgurLogin():
    print('Authenticating imgur account...')
    client = ImgurClient(imgurConfig.client_id, imgurConfig.client_secret)
    client.set_user_auth(imgurConfig.access_token, imgurConfig.refresh_token)
    print("Logged in to imgur\n")
    return client


def postSubmissionToImgur(client, submission):
    with open('redditURLs.txt', 'a') as f:
        f.write('\n' + submission.url)
        f.close()

    print('Posting submission to Imgur')
    album = None
    submissionConfig = {
        'album': album,
        'name': submission.title,
        'title': submission.title,
        'description': ''
    }
    client.upload_from_url(submission.url, config=submissionConfig, anon=False)
    print('Posted image mirror to imgur\n')


def returnLinkToCallComment(client, comment):
    for image in client.get_account_images(imgurConfig.username, page=0):
        print('Replying to comment with imgur URL')
        comment.reply('You\'ve requested an imgur mirror of this post!\n'
                      'The imgur mirror is located at ' + image.link)
        print('Reply successful')
        break  # stop after returning first(most recent) image


while True:
    runBot()
    sleep(60)
