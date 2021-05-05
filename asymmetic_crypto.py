from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa


def encrypt_file(filename, password):

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    # convert password to bytes for use with serialization
    byte_pass = bytes(password, "utf-8")

    # create private key with password and write to file
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(byte_pass),
    )
    print("private pem:")
    print(private_pem.decode())

    # with open("private.pem", "wb") as key_file:
    #     key_file.write(pem)

    # prepare and write public key to file
    public_key = private_key.public_key()
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    print("public pem:")
    print(public_pem.decode())
    # with open("public.pem", "wb") as key_file:
    #     key_file.write(public_pem)

    # load and encrypt data
    with open(filename, "rb") as fp:
        file_data = fp.read()
        encrypted_data = public_key.encrypt(
            file_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        print("encrypted data:")
        print(encrypted_data)

    # with open("encrypted.txt", "wb") as fp:
    #     fp.write(encrypted_data)


def decrypt_file(filename, private_key_filename, password):

    byte_password = bytes(password, "utf-8")

    with open(private_key_filename, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=byte_password,
        )

    with open(filename, "rb") as fp:
        encrypted_file_data = fp.read()

        decrypted_data = private_key.decrypt(
            encrypted_file_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )

    with open("decrypted.txt", "wb") as fp:
        fp.write(decrypted_data)


encrypt_file("test.txt", "lukeluke")
# decrypt_file("encrypted.txt", "private.pem", "lukeluke")
