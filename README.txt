# Members: Vinh Tran (Email: kimvinh@csu.fullerton.edu)
	   Quang Nguyen (Email: quangdnguyen2211@csu.fullerton.edu)

# CPSC 449 - 02

# Professor: Kenytt Avery

# Project 2: Microservice Implementation and Load Balancing

----------------------------------------------------------------------------------------------------

### SUMMARY ###

- There are two main microservices built in this project, one for 'users' and one for 'timelines' to provide
the services to users. With the 'users' services, users can register, follow/ unfollow each other, post messages, and
change their information (i.e., password, bio). With the 'timelines' services, they can show users' posts that they have made,
all posts from all users that this user followed, and all posts from all users. There are some services that require users
to log in before using. 

- For all new creations of a user or post, they will be stored in the database files. Each user created will have
a username, a bio, an email address, and a password. Each post that a user creates will have the author's username, the text (content) of the post,
and a timestamp.

- For production deployment, Gunicorn is used in this project as a WSGI server to run both microservices, and the program was designed to
handle the running of multiple instances of the 'timeline' service by using HAProxy as an load balancer.

----------------------------------------------------------------------------------------------------

### MICROSERVICES - DETAILED DESCRIPTIONS ###

----------------------------------------------------------------------------------------------------

### REQUIREMENTS ###

- There are some tools and libraries needed to be installed before running the microservices:

   1. Hug
   2. sqlite-utils libraries
   3. HAProxy
   4. Gunicorn server

----------------------------------------------------------------------------------------------------

### "CPSC-449-Project2.tar.gz" Contents ###

1. README.txt				// This file

2. timelines_services.py		// Containing the source code that executes the 'timelines' services

3. users_services.py			// Containing the source code that executes the 'users' services

4. Profile				// Containing The WSGI-compatible server (Gunicorn) to run both microservices

5. .env					// Avoiding missing output from Foreman

6. "var" folder				// Containing the log and database files
   6.1. "log" folder			// Containing the log files of microservices
      6.1.1. users_services.log		// Containing records of activities within the 'users' microservice
      6.1.2. timelines_services.log	// Containing records of activities within the 'timelines' microservice
   6.2. posts.db			// The database file that stores all users' posts
   6.3. users.db			// The database file that stores all users' information and followings

7. "bin" folder				// Containing the shell files
   7.1. init.sh				// The shell script that initializes all database files
   7.2. posts.sh			// The shell script that run the specific command(s)

8. "etc" folder				// Containing the configuration files related to two microservices
   8.1. users_services.ini
   8.2. timelines_services.ini
   8.3. logging.ini
   8.4. loggine2.ini

9. 'share' folder			// Containing the JSON and CSV files
   9.1. bio.json
   9.2. new_follow.json
   9.3. new_password.json
   9.4. user.json
   9.5. wrong_username_bio.json
   9.6. following.csv
   9.7. posts. csv
   9.8. users.csv

----------------------------------------------------------------------------------------------------

### HOW TO START THE SERVICES ###

# Note: The following steps will ask you to install some tools and libraries to meet the requirements
for running the project.

1. To install pip package installer and tools, command:
$ sudo apt update
$ sudo apt install --yes python3-pip ruby-foreman httpie sqlite3

2. To install Hug and sqlite-utils libraries, command:
$ python3 -m pip install hug sqlite-utils

3. To install the HAProxy and Gunicorn servers, command:
$ sudo apt install --yes haproxy gunicorn

4. To load the database for the services, command:
$ ./bin/init.sh

5. To run the services, command:
$ foreman start
