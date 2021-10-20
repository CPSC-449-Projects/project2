import hug
import sqlite_utils
import datetime
import configparser
import logging.config
import requests

# Load configuration
#
config = configparser.ConfigParser()
config.read("./etc/timelines_services.ini")
logging.config.fileConfig(config["logging"]["config"], disable_existing_loggers=False)


# Arguments to inject into route functions
#
@hug.directive()
def sqlite(section="sqlite", key="dbfile", **kwargs):
    dbfile = config[section][key]
    return sqlite_utils.Database(dbfile)

@hug.directive()
def log(name=__name__, **kwargs):
    return logging.getLogger(name)

# Using Routes
@hug.get("/post/")
def posts(db: sqlite):
    return {"post": db["post"].rows}

''' Design the service of user timeline '''
@hug.get("/userTimeline/{username}")
def retrieveUserTimeline(response, username: hug.types.text, db: sqlite):
    posts = []
    try:
    	for post in db.query("SELECT * FROM post WHERE username = ? ORDER BY timestamp DESC", [username]):
        	posts.append(post)
    except sqlite_utils.db.NotFoundError:
        response.status = '404 NOT FOUND'

    return {"post": posts}

''' Design the service of public timeline '''
@hug.get("/publicTimeline/")
def retrievePublicTimeline(response, db: sqlite):
    posts = []
    try:
        for post in db.query("SELECT * FROM post ORDER BY timestamp DESC"):
            posts.append(post)
    except sqlite_utils.db.NotFoundError:
        response.status = '404 NOT FOUND'

    return {"post": posts}

def check_user(username, password):
    r = requests.get(f'http://localhost:5000/login?username={username}&password={password}')
    if r.status_code == 200:
        return username

authentication=hug.authentication.basic(check_user)

''' Design the service of home timeline '''
@hug.get("/homeTimeline/{username}", requires=authentication)
def retrieveHomeTimeline(response, username: hug.types.text, user: hug.directives.user, db: sqlite):
    if username != user:
        return {"error": f"You are unauthorized to access the home timeline of {username}."}

    follows = []
    list_of_followings = requests.get(f'http://localhost:5000/get_following/{username}')
    list_of_followings = list_of_followings.json()

    for following in list_of_followings["follows"]:
        if following["username"] == username:
            follows.append(following["following"])

    posts = []
    try:
        for post in db.query("SELECT * FROM post WHERE username IN (%s) ORDER BY timestamp DESC"
                             % ','.join('?'*len(follows)), follows):
            posts.append(post)
    except sqlite_utils.db.NotFoundError:
        response.status = '404 NOT FOUND'

    return {"post": posts}

''' Design the service of allowing an existing user to post a message '''
@hug.post("/message", requires=authentication)
def postMessage(response, username: hug.directives.user, text: hug.types.text, db: sqlite):
    posts = db["post"]

    post = {
        "username": username["username"],
        "text": text,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    try:
        posts.insert(post)
    except Exception as e:
        response.status = hug.falcon.HTTP_400
        return {"error": str(e)}

    response.set_header("Location", "/post/")
    return post
