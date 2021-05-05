# Encryption Tools #

Collection of encryption tools from [pyca/cryptography](https://cryptography.io/en/latest/) served through a flask application. 

## features ##

- Password Generator
- [Password Based Key Generator](https://cryptography.io/en/latest/hazmat/primitives/key-derivation-functions/#variable-cost-algorithms)
- [Symmetric Encryption/Decryption](https://cryptography.io/en/latest/fernet/)
- [RSA Encryption/Decryption](https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/)
- user authentication
- profile page for viewing/downloading keys and encrypted files
- sqlite3 database for storage


## Installing ##

    $ python3 -m venv env
    $ source env/bin/activate
    $ pip install -r requirements.txt

## Running locally ##

    FLASK_DEBUG=TRUE FLASK_APP=encryption_tools flask run

## Running tests ##

    python setup.py test


## sources ##

- [CSS by bootstrap](https://getbootstrap.com/docs/5.0/getting-started/introduction/)
- [bootstrap theme](https://github.com/ThemesGuide/bootstrap-themes/tree/master/fresca)
- [pyca/cryptography](https://cryptography.io/en/latest/)