import hug
import sqlite_utils
import configparser
import logging.config

# Load the database
db = sqlite_utils.Database("posts.db")

# Using Routes

''' Design the service of user timeline '''
@hug.get("/userTimeline/{username}")
def retrieveUserTimeline(response, username: hug.types.text):
    posts = []
    try:
    	for post in db.query("SELECT * FROM post WHERE username = ? ORDER BY timestamp DESC", [username]):
        	posts.append(post)
    except sqlite_utils.db.NotFoundError:
        response.status = '404 NOT FOUND'

    return {"post": posts}

''' Design the service of home timeline '''
@hug.get("/homeTimeline/{username}")
def retrieveHomeTimeline(response):

    return

''' Design the service of public timeline '''
@hug.get("/publicTimeline/")
def retrievePublicTimeline(response):
    posts = []
    try:
        for post in db.query("SELECT * FROM post ORDER BY timestamp DESC"):
            posts.append(post)
    except sqlite_utils.db.NotFoundError:
        response.status = '404 NOT FOUND'

    return {"post": posts}
