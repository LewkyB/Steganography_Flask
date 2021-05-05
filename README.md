# Encryption Tools #

Collection of encryption tools from [pyca/cryptography](https://cryptography.io/en/latest/) served through a flask application. 

## Requirements ##

    flask
    pre-commit 
    cryptography
## Installing ##

    $ python3 -m venv env
    $ source env/bin/activate
    $ pip install -r requirements.txt

## Running locally ##

    FLASK_DEBUG=TRUE FLASK_APP=encryption_tools flask run

## Running tests ##

    python setup.py test


## sources ##

- [sqlalchemy flask info](https://flask-sqlalchemy.palletsprojects.com/en/2.x/#)