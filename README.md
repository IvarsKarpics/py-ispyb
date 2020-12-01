# py-ispyb

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/301f7c319e504a94950e7798bdb8cd31)](https://www.codacy.com/manual/IvarsKarpics/py-ispyb?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ispyb/py-ispyb&amp;utm_campaign=Badge_Grade)
[![Build Status](https://travis-ci.org/ispyb/py-ispyb.svg?branch=master)](https://travis-ci.org/ispyb/py-ispyb)
[![codecov](https://codecov.io/gh/ispyb/py-ispyb/branch/master/graph/badge.svg)](https://codecov.io/gh/ispyb/py-ispyb)
[![License: LGPL v3](https://img.shields.io/badge/License-LGPL%20v3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)


ISPyB backend server based on python flask-restx.


## Dependencies

* [**Python**](https://www.python.org/) 3.5+ / pypy2
* [**flask-restx**](https://github.com/python-restx/flask-restx) (+
  [*flask*](http://flask.pocoo.org/))
* [**sqlalchemy**](http://www.sqlalchemy.org/) (+
  [*flask-sqlalchemy*](http://flask-sqlalchemy.pocoo.org/)) - Database ORM.
* [**marshmallow**](http://marshmallow.rtfd.org/)
* [**ruamel.yaml**](https://pypi.org/project/ruamel.yaml/)


## How to run py-ispyb

### Install requirements

In case of MySQL or MariaDB you might have to install dev tools:

`sudo apt-get install -y python3-mysqldb`

or

`apt-get install libmariadbclient-dev`

Install python dependencies:

`sudo pip install -r requirements.txt`

### Copy and edit yaml configuration file

`cp ispyb_core_config_example.yml ispyb_core_config.yml`

### Regenerate data base models and schemas

```bash
cd scripts
./generate_core_models.sh
python3 generate_core_schemas.py
cd ..
```

If you do not have a running ispyb database then you can create one by running:

`scripts/create_core_db.sh`


### Run application in debug mode

* `python3 wsgi.py`
* `invoke app.run`

Now you can go to http://localhost:5000/ispyb/api/v1/doc and explore py-ispyb via swagger ui.
For authentication json web tokens (jwt) are used. Call http://localhost:5000/ispyb/api/v1/auth/login and retrieve access token from the response:

```bash
{
    "token": "YOUR_JWT_TOKEN",
    "roles": [
        "user"
    ]
}
```
For requests use the token in the `Authorization` header: `Bearer YOUR_JWT_TOKEN`. For example to retrieve proposals call:

`curl -X GET -H 'Authorization: Bearer YOUR_JWT_TOKEN' -i http://localhost:5000/ispyb/api/v1/proposals`

## Misc

* For deployment options see `deploy` directory.
* Status codes: https://www.flaskapi.org/api-guide/status-codes/

