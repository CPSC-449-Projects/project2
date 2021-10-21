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

4. Microservices Documentation.pdf	// Containing detailed descriptions about what services are in both
					   'users' and 'timelines' microservices and how they work

5. Profile				// Containing The WSGI-compatible server (Gunicorn) to run both microservices

6. .env					// Avoiding missing output from Foreman

7. 'var' folder				// Containing the log and database files
   5.1. 'log' folder			// Containing the log files of microservices
      5.1.1. users_services.log		// Containing records of activities within the 'users' microservice
      5.1.2. timelines_services.log	// Containing records of activities within the 'timelines' microservice
      5.1.3. posts.db			// The database file that stores all users' posts
      5.1.4. users.db			// The database file that stores all users' information and followings

8. 'bin' folder				// Containing the shell files
   6.1. init.sh				// The shell script that initializes all database files
   6.2. posts.sh			// The shell script that run the specific command(s)

9. 'etc' folder				// Containing the configuration files related to two microservices
   7.1. users_services.ini
   7.2. timelines_services.ini
   7.3. logging.ini
   7.4. loggine2.ini

10. 'share' folder			// Containing the JSON and CSV files
   8.1. bio.json
   8.2. new_follow.json
   8.3. new_password.json
   8.4. user.json
   8.5. wrong_username_bio.json
   8.6. following.csv
   8.7. posts. csv
   8.8. users.csv

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
