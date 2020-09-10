#!/usr/bin/python3
"""
Utility for encrypting and decrypting strings.
You need 2 arguments:

    d|e : D for decrypt, e for encrypt
    str: The string to encore or decode
"""
import os
from cryptography.fernet import Fernet
import sys

key = os.environ["KEY"]
cipher_suite = Fernet(key)


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


if __name__ == '__main__':
    try:
        if sys.argv[1] == 'd':
            print("\nDecrupted string:")
            print(decrypt(sys.argv[2]))
        elif sys.argv[1] == 'e':
            print("\nEncrypted string from \"" + sys.argv[2] + "\":")
            print(encrypt(sys.argv[2]))
        print("")
    except Exception:
        print("""
Utility for encrypting and decrypting strings.
You need 2 arguments:

    d|e : D for decrypt, e for encrypt
    str: The string to encore or decode

Example encrypting a string:

    {0} e MyPassword
    """.format(sys.argv[0]))
