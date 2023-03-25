Setup

venv?
flask?

* Install venv - sudo apt install python3-venv
* Create venv - python3 -m venv venv
* Activate venv - source venv/bin/activate
* Installs:
- flask - pip install flask
- login - pip install flask-login

// ceva cu requirements.txt ca sa nu incarci venv pe repo - https://stackoverflow.com/questions/6590688/is-it-bad-to-have-my-virtualenv-directory-inside-my-git-repository

* Setup flask run - export FLASK_APP=app
* // Debug mode - export FLASK_DEBUG=1

* Run flask app - flask run



Database

sqllite?
templates? "{%}"
secret key? clar o vulnerabilitate

* SQLlite - https://www.digitalocean.com/community/tutorials/how-to-use-an-sqlite-database-in-a-flask-application


Flask

web form?

Login

blueprints?

https://flask.palletsprojects.com/en/2.2.x/tutorial/views/