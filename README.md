# Setup
## Virtual Environment
* Install - `sudo apt install python3-venv`
* Create - `python -m venv venv`
* Activate - `source venv/bin/activate`
## Dependencies
* `pip install -r requirements.txt`
##  Database
* From the `database` folder, run `python init_db.py`
## Flask
* `export FLASK_APP=app`
## Run, Flask, Run!
* `flask run`

# General Approach
* Planned the whole data model first
* Searched the Internet how to setup a database in Flask (knew beforehand that Flask was the most popular and/or accessible Python framework) and a login mechanism (as I had no idea how to do it)
* Fetched code from the Internet
* Tried to understand what I should use for my own purpose
* Had a lot of fun
# Endpoints
A user has all APIs exposed (i.e. has all the buttons which trigger the APIs exposed in FE), but access is role-based and corresponding feedback is shown when unauthorized.

# Vulnerabilities
* Not hiding API-triggering buttons for non-authorized users
* There must be something wrong with that `secret_key` from `app.py`. It's "secret" after all, and I didn't do pretty much anything to "protect", only randomized it.

# Missing Required Features
* "A report with all the treatments applied to a Patient (JSON) (accessed by the General manager or Doctor)"
* "Minimal test coverage for unit and integration test"
  * Found the `unittest` library, but I didn't have time to set it up and write a few basic CRUD tests.
* "Include migration and fixture files"
  * Used SQLite for the Database. Searched the Internet how to generate such files, but nothing quick or useful came up.
  * Very few changes occured, anyway. Renaming an attribute or two for one or two entities. (recommendedTreatmentId @patient -> treatment_id)

# If I had more time...
* OpenAPI documentation
  * Searched Google for "Python API documentation generator". `Sphinx` came up. Not sure if it generates OpenAPI docs, but I sure would've tried
* Modularized the code better (the create & edit.html and the entities' .py really repeat themselves)
  * I think this implied modularizing the routes/blueprints somehow, but I didn't figure out how
* More beautiful FE
* Used SQLalchemy instead of SQLite as I see it abstractizes/encapsulates the whole DB manipulation better 
  * With SQLite, I dusted off my SQL knowledge. Grateful for that
  * However, on a bigger project I probably would've used SQLalchemy
* Implemented roles better. Right now, they're just a lof of "ifs". Nothing too smart

# Feedback
Both fun and challenging in a good way for an entry-level Python challenger. Thank you! It has been a great learning experience. 