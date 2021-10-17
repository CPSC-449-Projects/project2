import hug
import sqlite_utils
import datetime
import configparser
import logging.config
import requests

# Load the database
db = sqlite_utils.Database("posts.db")

# Using Routes
@hug.get("/post/")
def posts():
    return {"post": db["post"].rows}

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
def retrieveHomeTimeline(response, username: hug.types.text):
    posts = []
    try:
        for post in db.query("SELECT * from post WHERE username IN (SELECT following FROM follow WHERE username = ?) ORDER BY timestamp DESC",
                             [username]):
            posts.append(post)
    except sqlite_utils.db.NotFoundError:
        response.status = '404 NOT FOUND'

    return {"post": posts}

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

def check_user(username, password):
    r = requests.get(f'localhost:8005/check_password?username={username}&password={password}')
    return r.status

authentication=hug.authentication.basic(check_user)
''' Design the service of allowing an existing user to post a message '''
@hug.post("/message", requires=authentication)
def postMessage(response, user: hug.directives.user):
    return user
    '''
    posts = db["post"]

    post = {
        "username": username,
        "text": text,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    foundUsername = False
    for usern in db.query("SELECT username FROM post GROUP BY username"):
        if usern["username"] == username:
            foundUsername = True
            break;

    if foundUsername == False:
        response.status = hug.falcon.HTTP_401
        return {"error": f"You are unauthorized to post a message because '{username}' is invalid."}

    try:
        posts.insert(post)
    except Exception as e:
        response.status = hug.falcon.HTTP_400
        return {"error": str(e)}

    response.set_header("Location", "/post/")
    return post
    '''
