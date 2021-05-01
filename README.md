# irctube #

Videos from IRC

Uses pre-commit and black to format the code
## Requirements ##

    flask
    pre-commit 
    cryptography
## Installing ##

    $ python3 -m venv env
    $ source env/bin/activate
    $ pip install -r requirements.txt

## Running locally ##

    FLASK_DEBUG=TRUE FLASK_APP=irctube flask run

## Running tests ##

    python setup.py test
