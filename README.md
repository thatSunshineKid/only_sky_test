# Tasks
#### *Adam's notes are in italics*

- [x] Create an about me page and link to it in the nav
    - *Notes: new about me page located at /about , link in nav 'about'*
- [x] Create a create blog post page
    - *create blog post page located at /post/create , also link in nav 'create post'*
    - *No user is attached to Post model as of now*
    - *The category of the blog post being created is automatically added as 'General'*

    - [x] a post must have a title
        - *WTforms validators do this work*
    - [x] the post itelf must be at least 10 characters long (yes totally arbitrary :-) )
        - *WTforms validator Length*

- [x] Update the index page to list all blog posts (showing 10 per page)
    - *index route returns list of posts on index template, ordered by last created, along with pagination of 10 if needed*
- [x] Add archive listing page that limits the results to a specific month/year
    - *archive page located at '/archive/month/year' shows post list, but filtered to return only the correct month and year, based on url parameters month and year*

# Helpful Tips

## Language
- This application is written in Python 3.6

## Requirements

- You will need to install docker (https://store.docker.com/search?offering=community&platform=desktop&q=&type=edition)
- If you are running on windows the make commands won't work.  You will have to manually run the commands found in Makefile

## Where is the code?

All the code currently lives in sample/app/main.py

## How to start the server

    $ make build -- only needed the first time you run things
    $ make up

## How to stop and reset the database

    $ make down
    $ make up

**NOTE** running make down will blow away your database!

## How to regenerate the db schema

    $ make up
    $ make dump-db-schema -- separate terminal

## How to access the server from your browser
- localhost (no port should be specified)

# Useful Resources

## Flask (Web Framework) documentation
http://flask.pocoo.org/

## How do to DB stuff
http://flask-sqlalchemy.pocoo.org/2.1/quickstart/

## Flask WTForms
http://flask.pocoo.org/docs/0.12/patterns/wtforms/

## Flask Login
https://flask-login.readthedocs.io/en/latest/

## Bootstrap 4
https://v4-alpha.getbootstrap.com/


