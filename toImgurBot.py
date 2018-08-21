from time import sleep

import praw

import redditConfig

from imgurpython import ImgurClient

import imgurConfig


def main():
    print('\nRunning toImgurBot...\n')
    reddit = redditLogin()
    client = imgurLogin()
    checkCommentsForCall(reddit, client)


def checkCommentsForCall(reddit, client):
    """
    :param client:  imgur login instance, used to interact with imgur api
    :param reddit: reddit login instance, used to interact with PRAW api
    :return: none, scrapes comments on /r/pics until it finds one with "!toImgur". Then checks if post has already been seen by bot,
    if post is self post, or if post is already hosted by imgur. If none of these, creates new host on imgur.
    """
    print('Searching Comments for !toImgur...\n')
    botCall = '!toImgur'
    for comment in reddit.subreddit('pics').stream.comments():
        if botCall in comment.body:
            print('!toImgur found in comments...')
            if comment.submission.url in open('redditURLs.txt', 'r').read():  # if submission already recorded
                print('This submission has already been mirrored\n')
            elif comment.submission.url is 'None':  # if a self post
                print('This submission does not contain an image')
            elif 'imgur.com' not in comment.submission.url:  # if url is not already imgur
                print('Comment post is not hosted by imgur, creating mirror...\n')
                postSubmissionToImgur(client, comment.submission)
                returnLinkToCallComment(client, comment)
            else:  # if url is already imgur
                print('Comment submission is already hosted by imgur.\n')
    print('No calls for bot found :(')


def redditLogin():
    print('Logging in to reddit...')
    r = praw.Reddit(client_id=redditConfig.client_id,
                    client_secret=redditConfig.client_secret,
                    user_agent='My testBot',
                    username=redditConfig.username,
                    password=redditConfig.password)
    print('Logged in to reddit\n')
    return r


def imgurLogin():
    print('Logging in to imgur account...')
    client = ImgurClient(imgurConfig.client_id, imgurConfig.client_secret)
    client.set_user_auth(imgurConfig.access_token, imgurConfig.refresh_token)
    print("Logged in to imgur\n")
    return client


def postSubmissionToImgur(client, submission):
    """
    :param client:  imgur login instance, used to interact with imgur api
    :param submission: submission to be rehosted, includes necessary submission information
    :return: none, writes submission url to .txt, and posts image to imgur
    """
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
    """
    :param client:  imgur login instance, used to interact with imgur api
    :param comment: original reddit comment that called bot
    :return: none, replies to reddit comment with imgur link
    """
    for image in client.get_account_images(imgurConfig.username, page=0):
        print('Replying to comment with imgur URL')
        try:
            comment.reply('You\'ve requested an imgur mirror of this post!\n'
                          'The imgur mirror is located at ' + image.link)
        except:
            print('RATELIMIT exceeded, waiting 10 minutes and trying again')
            sleep(600)
            returnLinkToCallComment(client, comment)

        print('Reply successful')
        break  # stop after returning first(most recent) image, only way to get url using imgur api


if __name__ == '__main__':
    while True:
        main()
