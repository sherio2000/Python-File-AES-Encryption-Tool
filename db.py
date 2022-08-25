from itertools import count
import re
import mysql.connector
from tkinter import messagebox

import crypto_utils


def connectDb():
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="A18535696!?"
    )
    mycursor = db_connection.cursor()
    mycursor.execute("CREATE DATABASE IF NOT EXISTS crypto;")
    db_connection.close()
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="A18535696!?",
        database="crypto"
    )
    mycursor = db_connection.cursor()
    mycursor.execute(
        "CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY , name VARCHAR(255), email VARCHAR(255), password binary(32), salt binary(32))")
    mycursor.execute(
        "CREATE TABLE IF NOT EXISTS encrypted_files (id INT AUTO_INCREMENT PRIMARY KEY, filename VARCHAR(255), extension VARCHAR(255), filepath VARCHAR(255), parent_filepath VARCHAR(255), encryption_date VARCHAR(255), user_id INT)")
    mycursor.execute(
        "CREATE TABLE IF NOT EXISTS active_session (id INT AUTO_INCREMENT PRIMARY KEY, user_id INT, name VARCHAR(255), email VARCHAR(255))")
    mycursor.execute(
        "SET SQL_SAFE_UPDATES = 0; ")


def signIn(email, password):
    if EmailIsNotValid(email):
        messagebox.showinfo("Error", "Email is invalid")
    else:
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="A18535696!?",
            database="crypto"
        )
        mycursor = db_connection.cursor()
        sql = "select id, name, email, password, salt from users where email = %s"
        mycursor.execute(sql, [email])
        results = mycursor.fetchall()
        if results:
            for row in results:
                if crypto_utils.PasswordHashMatch(password, row[3], row[4]):
                    messagebox.showinfo("", "Success")
                    addLoginSession(row[0], row[1], row[2])
                    return True
                else:
                    messagebox.showinfo("", "Incorrect Email/Password")
                    return False
        else:
            messagebox.showinfo("", "Incorrect Email/Password")
            return False


def getActiveUserInfo():
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="A18535696!?",
        database="crypto"
    )
    mycursor = db_connection.cursor()
    sql = "select * from active_session"
    mycursor.execute(sql)
    results = mycursor.fetchall()
    if results:
        return results
    else:
        return ""


def logout():
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="A18535696!?",
        database="crypto"
    )
    mycursor = db_connection.cursor()
    try:
        current_user = getActiveUserInfo()
        for user in current_user:
            sql = "delete from active_session where user_id = %d" % int(user[1])
            mycursor.execute(sql)
        results = mycursor.fetchall()
        db_connection.commit()
        if len(results) == 0:
            messagebox.showinfo("Logout", "Successfully Logged Out!")
            return True
    except Exception as e:
        print(e)
        return False


def addLoginSession(userid, name, email):
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="A18535696!?",
        database="crypto"
    )
    mycursor = db_connection.cursor()

    try:
        sql = "Insert into active_session (id, user_id, name, email) VALUES (%s, %s, %s, %s)"
        val = (0, userid, name, email)
        mycursor.execute(sql, val)
        db_connection.commit()
        return True
    except Exception as e:
        print(e)
        db_connection.rollback()
        db_connection.close()
        return False


def EmailIsNotValid(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.fullmatch(regex, email):
        return False
    else:
        return True


def register(email, password, fullname):
    print(email + "" + password)
    if email == "" or password == "" or fullname == "":
        messagebox.showinfo("", "Please fill in all fields")
        return None

    if email == "Email Address" or password == "Password" or fullname == "Full Name":
        messagebox.showinfo("", "Please fill in all fields correctly!")
        return None

    if EmailIsNotValid(email):
        messagebox.showinfo("Error", "Email is invalid")
        return None

    if emailExists(email):
        messagebox.showinfo("Error", "Email already exists!")
        return None
    else:
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="A18535696!?",
            database="crypto"
        )
        mycursor = db_connection.cursor()

        try:
            sql = "Insert into users (id, name, email, password, salt) VALUES (%s, %s, %s, %s, %s)"
            values = crypto_utils.hashPassword(password)
            val = (0, fullname, email, values[1], values[0])
            mycursor.execute(sql, val)
            sql = "Select id from users where email=%s AND name=%s"
            mycursor.execute(sql, (email, fullname))
            results = mycursor.fetchall()
            for row in results:
                addLoginSession(row[0], fullname, email)
            db_connection.commit()
            messagebox.showinfo("", "Registration Successful")
            return True
        except Exception as e:
            print(e)
            db_connection.rollback()
            db_connection.close()
            messagebox.showinfo("Error", "Failed to register!")
            return False


def userIsLoggedIn():
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="A18535696!?",
        database="crypto"
    )
    mycursor = db_connection.cursor()
    sql = "select * from active_session"
    mycursor.execute(sql)
    results = mycursor.fetchall()
    if len(results) == 1:
        return True
    else:
        return False


def addEncryptedFile(filename, extension, filepath, parent_filepath, encryption_date):
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="A18535696!?",
        database="crypto"
    )
    mycursor = db_connection.cursor()

    try:
        sql = "Insert into encrypted_files (id, filename, extension, filepath, parent_filepath, encryption_date, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        user_info = getActiveUserInfo()
        for user in user_info:
            val = (0, filename, extension, filepath, parent_filepath, encryption_date, user[1])
            mycursor.execute(sql, val)
            db_connection.commit()
            return True
    except Exception as e:
        print(e)
        db_connection.rollback()
        db_connection.close()
        messagebox.showinfo("Error", "Failed to add encrypted file to db!")
        return False


def emailExists(email):
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="A18535696!?",
        database="crypto"
    )
    mycursor = db_connection.cursor(buffered=True)

    try:
        sql = "select * FROM users WHERE email=%s"
        mycursor.execute(sql, (email,))
        results = mycursor.fetchall()
        if len(results) > 0:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        db_connection.rollback()
        db_connection.close()
        messagebox.showinfo("Error", "Failed to get file extension!")
        return False


def removeEncryptedFile(id):
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="A18535696!?",
        database="crypto"
    )
    mycursor = db_connection.cursor()

    try:
        sql = "DELETE FROM encrypted_files WHERE id=%d" % id
        mycursor.execute(sql)
        db_connection.commit()
        return True
    except Exception as e:
        print(e)
        db_connection.rollback()
        db_connection.close()
        messagebox.showinfo("Error", "Failed to add encrypted file to db!")
        return False


def getFileExtension(id):
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="A18535696!?",
        database="crypto"
    )
    mycursor = db_connection.cursor(buffered=True)

    try:
        sql = "select extension FROM encrypted_files WHERE id=%s"
        mycursor.execute(sql, (id,))
        db_connection.commit()
        results = mycursor.fetchall()
        if results:
            for row in results:
                return row[0]
        return ""
    except Exception as e:
        print(e)
        db_connection.rollback()
        db_connection.close()
        messagebox.showinfo("Error", "Failed to get file extension!")
        return ""


connectDb()
