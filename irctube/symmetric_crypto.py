import random
import string
import os
import base64

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def generate_password(character_set, length):

    if character_set == "ascii":
        characters = string.ascii_letters
    elif character_set == "ascii+num":
        characters = string.ascii_letters + string.digits
    elif character_set == "ascii+num+sym":
        characters = string.ascii_letters + string.digits + string.punctuation

    return "".join(random.choice(characters) for _ in range(length))


def generate_key(password):

    # prepare password for use with Fernet
    byte_password = bytes(password, "utf-8")  # password must be in byte form
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )

    key = base64.urlsafe_b64encode(kdf.derive(byte_password))

    # with open("symmetric_secret.key", "wb") as key_file:
    #     key_file.write(key)
    # return key_file

    return key


def encrypt_file(target_filename, key_file):

    with open(key_file, "rb") as key_file:
        key = key_file.read()
        f = Fernet(key)

    with open(target_filename, "rb") as fp:
        file_data = fp.read()
        encrypted_data = f.encrypt(file_data)

    with open(target_filename, "wb") as fp:
        fp.write(encrypted_data)


def decrypt_file(filename, key_file):

    with open(key_file, "rb") as key_file:
        key = key_file.read()
        f = Fernet(key)

    with open(filename, "rb") as fp:
        encrypted_file_data = fp.read()
        decrypted_data = f.decrypt(encrypted_file_data)

    with open(filename, "wb") as fp:
        fp.write(decrypted_data)


# which_chars = "ascii+num+sym"
# generated_password = generate_password(which_chars, 8)
# print(generated_password)

# generate_key(generated_password)
# key_file_name = "symmetric_secret.key"

# encrypt_file("test.txt", key_file_name)
# decrypt_file("test.txt", key_file_name)
# print(generate_key("luke"))
