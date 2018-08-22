# toImgurBot

A reddit bot that logs in to Reddit and Imgur.
It continually scrapes new comments in the subreddit chose (/r/pics) for a reference call "!toImgur".
When this call is seen, it takes the parent submission from this comment and rehosts the image to Imgur.com.
It will then return a link to the newly hosted image back to the commenter

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development.

### Prerequisites

You must create a reddit account for your bot and register it as a script.
You must also download PRAW library for python, step by step directions for this are found below:

```
https://praw.readthedocs.io/en/latest/getting_started/installation.html#
```

You must follow similar steps with imgur and their python API.
Directions for this are found below:

```
https://apidocs.imgur.com/
```

### Installing

Download the code and add your imgur and reddit credentials for your bot in the redditConfig.py and imgurConfig.py files.


## Built With

* Python 3.6
* PRAW 3.6
* imgurpython

## Contributing

## Authors

* Collin Brandt
