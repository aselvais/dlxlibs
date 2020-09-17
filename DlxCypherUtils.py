#!/usr/bin/python3
"""
Utility for encrypting and decrypting strings.

To use this library, you will need to have a key stored in the KEY var at the OS env level.
You can instantiate this var in the CDSW modifying the settings of your project and adding an
environment variable.

You need 2 arguments:

    d|e|g : D for decrypt, e for encrypt, g for generating a key
    str: The string to encore or decode (not relevant for g)

Example encrypting a string:

    {0} e MyPassword
"""
import os
from cryptography.fernet import Fernet
import sys

cipher_suite = ""

try:
    key = os.environ["KEY"]
    cipher_suite = Fernet(key)
except:
    print('The key is missing, please generate a key and place it in the os KEY env var.')
    # exit()


def decrypt(v=""):
    """Decrypt an encoded string

    Args:
        v (str, optional): String to decrypt. Defaults to "".

    Returns:
        String: decrypted string or an empty str in case of error.
    """
    global cipher_suite
    try:
        return cipher_suite.decrypt(v.encode()).decode()
    except Exception:
        return ""


def encrypt(v):
    """Encrypt a string

    Args:
        v (str, optional): String to encrypt. Defaults to "".

    Returns:
        String: encrypted string or an empty str in case of error.
    """
    global cipher_suite
    try:
        return cipher_suite.encrypt(v.encode()).decode()
    except Exception:
        return ""


def get_generated_key():
    return Fernet.generate_key().decode()


if __name__ == '__main__':
    try:
        if sys.argv[1] == 'd':
            print("\nDecrupted string:")
            print(decrypt(sys.argv[2]))
        elif sys.argv[1] == 'e':
            print("\nEncrypted string from \"" + sys.argv[2] + "\":")
            print(encrypt(sys.argv[2]))
        elif sys.argv[1] == 'g':
            print("\nGenerated key: ")
            print(get_generated_key())
        print("")
    except Exception:
        print("""
Utility for encrypting and decrypting strings.
To use this library, you will need to have a key stored in the KEY var at the OS env level.
You can instantiate this var in the CDSW modifying the settings of your project and adding an
environment variable.

You need 2 arguments:

    d|e|g : D for decrypt, e for encrypt, g for generating a key
    str: The string to encore or decode (not relevant for g)

Example encrypting a string:

    {0} e MyPassword
    """.format(sys.argv[0]))
