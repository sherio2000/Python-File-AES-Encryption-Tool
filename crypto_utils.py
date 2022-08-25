import hashlib
import os
from base64 import b64encode, b64decode
from tkinter.messagebox import showinfo

import bcrypt
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad


def encrypt(file_name, key):
    with open(file_name, 'rb') as entry:
        data = entry.read()
        cipher = AES.new(key, AES.MODE_CFB)
        ciphertext = cipher.encrypt(pad(data, AES.block_size))
        iv = b64encode(cipher.iv).decode('UTF-8')
        ciphertext = b64encode(ciphertext).decode('UTF-8')
        to_write = iv + ciphertext
    entry.close()
    with open(file_name + '.enc', 'w') as data:
        data.write(to_write)
    data.close()
    showinfo(
        title='Success',
        message='File Encrypted!'
    )


def decrypt(file_path, key, out_file_path):
    with open(file_path, 'r') as entry:
        try:
            key = key.encode('UTF-8')
            key = pad(key, AES.block_size)
            data = entry.read()
            length = len(data)
            iv = data[:24]
            iv = b64decode(iv)
            ciphertext = data[24:length]
            ciphertext = b64decode(ciphertext)
            cipher = AES.new(key, AES.MODE_CFB, iv)
            decrypted = cipher.decrypt(ciphertext)
            decrypted = unpad(decrypted, AES.block_size)
            with open(out_file_path, 'wb') as data:
                data.write(decrypted)
            data.close()
            showinfo(
                title='Success',
                message='File Decrypted!'
            )
            return True
        except(ValueError, KeyError):
            showinfo(
                title='Error',
                message='Invalid password!'
            )
            return False


def hashPassword(password):
    salt = os.urandom(32)  # A new salt for this user
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    values = [salt, key]
    return values


def PasswordHashMatch(password, hashValue, salt):
    new_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    if new_key == hashValue:
        return True
    else:
        return False
