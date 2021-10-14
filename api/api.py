# Science Fiction Novel API - Hug Edition
#
# Adapted from "Creating Web APIs with Python and Flask"
# <https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask>.
#

import configparser
import logging.config

import hug
import sqlite_utils

# Load configuration
#
config = configparser.ConfigParser()
config.read("./etc/api.ini")
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


# Routes
#
@hug.get("/users/")
def books(db: sqlite):
    return {"users": db["users"].rows}

@hug.get("/users/{id}")
def retrieve_book(response, id: hug.types.number, db: sqlite):
    users = []
    try:
        user = db["users"].get(id)
        user["follows"] = "me"
        users.append(user)
        # println(user['follows'])
    except sqlite_utils.db.NotFoundError:
        response.status = hug.falcon.HTTP_404
    return {"users": user}

# Create new user
@hug.post("/users/", status=hug.falcon.HTTP_201)
def create_user(
    response,
    username: hug.types.text,
    email_address: hug.types.text,
    password: hug.types.text,
    bio: hug.types.text,
    follows: hug.types.text,
    db: sqlite,
):
    users = db["users"]

    user = {
        "username": username,
        "email_address": email_address,
        "password": password,
        "bio": bio,
        "follows": follows,
    }

    try:
        users.insert(user)
        user["id"] = users.last_pk
    except Exception as e:
        response.status = hug.falcon.HTTP_409
        return {"error": str(e)}

    response.set_header("Location", f"/users/{user['id']}")
    return user

# Follow new user
@hug.get("/follow/username")
def add_follow(response, username: hug.types.text, db: sqlite):
    users = []
    try:
        user = db["users"].get(username)
        # user['follows'] += follow
        users.append(user)
        println(user['follows'])
    except sqlite_utils.db.NotFoundError:
        response.status = hug.falcon.HTTP_404
    return {"users": user}

# # Unfollow user
# @hug.post("/unfollow", status=hug.falcon.HTTP_201)
# def unfollow():

# Change bio

# Search
@hug.get(
    "/search",
    examples=[
        "published=2017",
        "author=Heinlein",
        "title=Star",
        "first_sentence=night",
    ],
)
def search(request, db: sqlite, logger: log):
    users = db["users"]

    conditions = []
    values = []

    for column in ["username", "email_address", "password", "bio", "follows"]:
        if column in request.params:
            conditions.append(f"{column} LIKE ?")
            values.append(f"%{request.params[column]}%")

    if conditions:
        where = " AND ".join(conditions)
        logger.debug('WHERE "%s", %r', where, values)
        return {"users": users.rows_where(where, values)}
    else:
        return {"users": users.rows}
