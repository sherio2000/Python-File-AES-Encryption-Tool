import os
import platform
import subprocess
import webbrowser
from datetime import datetime
from pathlib import Path
from tkinter import *
import mysql.connector
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad
from tkinter import filedialog
from tkinter.messagebox import showinfo
import db
from db import *
from crypto_utils import encrypt, decrypt
from tkinter.ttk import Treeview
from PIL import Image, ImageTk
from tkinter import simpledialog

# ----------------------------------
# FUNCTIONS
# ----------------------------------

global encrypt_pass


def init():
    root = Tk()
    root.title('Login')
    root.geometry('925x500+300+200')
    root.configure(bg='#fff')
    root.resizable(False, False)

    img = PhotoImage(file='login.png')
    Label(root, image=img, bg='white').place(x=50, y=50)

    frame = Frame(root, width=350, height=350, bg="white")
    frame.place(x=480, y=70)

    heading = Label(frame, text='Sign In', fg='#57a1f8', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold'))
    heading.place(x=120, y=5)

    #######--------------------------------------------
    def on_enter(e):
        user.delete(0, 'end')

    def on_leave(e):
        name = user.get()
        if name == '':
            user.insert(0, 'Email')

    user = Entry(frame, width=25, fg='black', border=0, highlightthickness=0, bg="white",
                 font=('Microsoft YaHei UI Light', 11))
    user.place(x=30, y=80)
    user.insert(0, 'Email')
    user.bind('<FocusIn>', on_enter)
    user.bind('<FocusOut>', on_leave)

    Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)

    #######--------------------------------------------

    def on_enter(e):
        password.delete(0, 'end')

    def on_leave(e):
        pwd = password.get()
        if pwd == '':
            password.insert(0, 'Password')

    password = Entry(frame, width=25, fg='black', border=0, highlightthickness=0, bg="white",
                     font=('Microsoft YaHei UI Light', 11))
    password.place(x=30, y=150)
    password.insert(0, 'Password')
    password.bind('<FocusIn>', on_enter)
    password.bind('<FocusOut>', on_leave)

    Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)

    ######################################

    def signin():
        if db.signIn(user.get(), password.get()):
            root.destroy()
            home_main()

    def registerScreen():
        root.destroy()
        register()

    # Login Button
    Button(frame, width=29, pady=7, text="Sign in", bg='#57a1f8', fg='black', command=lambda: signin(), border=0).place(
        x=35, y=204)

    # Sign up Button
    label = Label(frame, text="Don't have an account?", fg='black', bg='white', font=('Microsoft YaHei UI Light', 9))
    label.place(x=75, y=270)

    sign_up = Button(frame, width=6, text='Sign Up', border=0, borderwidth=0, takefocus=0,
                     command=lambda: registerScreen(),
                     bd=0, highlightthickness=0,
                     bg='white', cursor='hand2', fg='#57a1f8')
    sign_up.place(x=215, y=270)

    root.mainloop()


def register():
    root = Tk()
    root.title('Register')
    root.geometry('925x500+300+250')
    root.eval('tk::PlaceWindow . center')
    root.configure(bg='#fff')
    root.resizable(False, False)

    img = PhotoImage(file='login.png')
    Label(root, image=img, bg='white').place(x=50, y=50)

    frame = Frame(root, width=350, height=350, bg="white")
    frame.place(x=480, y=70)

    heading = Label(frame, text='Register', fg='#57a1f8', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold'))
    heading.place(x=120, y=5)

    #######--------------------------------------------
    def on_enter(e):
        username.delete(0, 'end')

    def on_leave(e):
        name = username.get()
        if name == '':
            username.insert(0, 'Full Name')

    username = Entry(frame, width=25, fg='black', border=0, highlightthickness=0, bg="white",
                     font=('Microsoft YaHei UI Light', 11))
    username.place(x=30, y=80)
    username.insert(0, 'Full Name')
    username.bind('<FocusIn>', on_enter)
    username.bind('<FocusOut>', on_leave)

    Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)

    #######--------------------------------------------

    #######--------------------------------------------
    def on_enter(e):
        email.delete(0, 'end')

    def on_leave(e):
        Email = email.get()
        if Email == '':
            email.insert(0, 'Email Address')

    email = Entry(frame, width=25, fg='black', border=0, highlightthickness=0, bg="white",
                  font=('Microsoft YaHei UI Light', 11))
    email.place(x=30, y=150)
    email.insert(0, 'Email Address')
    email.bind('<FocusIn>', on_enter)
    email.bind('<FocusOut>', on_leave)

    Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)

    #######--------------------------------------------

    def on_enter(e):
        password.delete(0, 'end')

    def on_leave(e):
        pwd = password.get()
        if pwd == '':
            password.insert(0, 'Password')

    password = Entry(frame, width=25, fg='black', border=0, highlightthickness=0, bg="white",
                     font=('Microsoft YaHei UI Light', 11))
    password.place(x=30, y=220)
    password.insert(0, 'Password')
    password.bind('<FocusIn>', on_enter)
    password.bind('<FocusOut>', on_leave)

    Frame(frame, width=295, height=2, bg='black').place(x=25, y=247)

    ######################################

    def loginScreen():
        root.destroy()
        init()

    def register():
        if db.register(email.get(), password.get(), username.get()):
            root.destroy()
            home_main()

    Button(frame, width=29, pady=7, text="Register", bg='#57a1f8', fg='black', command=lambda: register(),
           border=0).place(
        x=35, y=274)
    label = Label(frame, text="Already have an account?", fg='black', bg='white', font=('Microsoft YaHei UI Light', 9))
    label.place(x=75, y=320)

    sign_in = Button(frame, width=6, text='Sign In', border=0, borderwidth=0, command=lambda: loginScreen(),
                     takefocus=0, bd=0, highlightthickness=0,
                     bg='white', cursor='hand2', fg='#57a1f8')
    sign_in.place(x=215, y=320)

    root.mainloop()


def createPasswordInputPopBox():
    root = Tk()
    root.title('Enter Password')
    root.geometry('550x200')
    root.eval('tk::PlaceWindow . center')
    root.configure(bg='#fff')
    root.resizable(False, False)

    frame = Frame(root, width=550, height=200, bg="white")
    frame.place(x=0, y=0)

    ######--------------------------------------------
    def on_password_enter(e):
        passwrd.delete(0, 'end')

    def on_password_leave(e):
        pwd = passwrd.get()
        if pwd == '':
            passwrd.insert(0, 'Password')

    passwrd = Entry(frame, width=25, fg='black', border=0, highlightthickness=0, bg="white",
                    font=('Microsoft YaHei UI Light', 11))
    passwrd.insert(0, 'Password')
    passwrd.place(x=155, y=53)

    passwrd.bind('<FocusIn>', on_password_enter)
    passwrd.bind('<FocusOut>', on_password_leave)

    Frame(frame, width=225, height=2, bg='black').place(x=150, y=75)

    #######--------------------------------------------

    #######--------------------------------------------
    def on_enter(e):
        confirm_pass.delete(0, 'end')

    def on_leave(e):
        pwd = confirm_pass.get()
        if pwd == '':
            confirm_pass.insert(0, 'Confirm Password')

    confirm_pass = Entry(frame, width=25, fg='black', border=0, highlightthickness=0, bg="white",
                         font=('Microsoft YaHei UI Light', 11))

    confirm_pass.place(x=155, y=100)
    confirm_pass.insert(0, 'Confirm Password')

    confirm_pass.bind('<FocusIn>', on_enter)
    confirm_pass.bind('<FocusOut>', on_leave)

    Frame(frame, width=225, height=2, bg='black').place(x=150, y=125)

    #######--------------------------------------------

    def savePassword():
        if passwrd.get() == confirm_pass.get():
            my_password = passwrd.get()
            return my_password

    my_password = savePassword()

    save = Button(frame, width=6, text='Save', border=0, borderwidth=0, takefocus=0,
                  bd=0, highlightthickness=0,
                  bg='white', cursor='hand2', fg='#57a1f8')
    save.pack(side=LEFT, padx=280, pady=150)

    cancel = Button(frame, width=6, text='Cancel', border=0, borderwidth=0, takefocus=0,
                    bd=0, highlightthickness=0,
                    bg='white', cursor='hand2', fg='#57a1f8')
    cancel.place(x=160, y=150)

    root.mainloop()

    return my_password


def home_main():
    root = Tk()
    root.title('Home')
    root.geometry('925x500+300+200')
    root.configure(bg='#fff')
    root.resizable(False, False)
    root.eval('tk::PlaceWindow . center')
    frame = Frame(root, width=950, height=900, bg="white")
    frame.place(x=0, y=2)

    # User Icon Image
    image = Image.open('user.png')
    img = image.resize((110, 100))
    user_img = ImageTk.PhotoImage(img)
    Label(root, image=user_img, bg='white').place(x=5, y=10)
    welcome_back_lbl = Label(frame, text='Welcome back, ', fg='black', bg='white',
                             font=('Microsoft YaHei UI Light', 12, 'bold'))
    welcome_back_lbl.place(x=120, y=30)
    user_name_lbl = Label(frame, text='User', fg='#57a1f8', bg='white',
                          font=('Microsoft YaHei UI Light', 12, 'bold'))
    user_name_lbl.place(x=130, y=50)

    def doLogout():
        if db.logout():
            root.destroy()
            init()

    Button(frame, width=9, pady=7, text="Logout", bg='#57a1f8', command=lambda: doLogout(), fg='black', border=0).place(
        x=770, y=35)

    if db.userIsLoggedIn():
        user = db.getActiveUserInfo()
        for user in user:
            user_name_lbl['text'] = user[2]

    def fetchData():
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="A18535696!?",
            database="crypto"
        )
        mycursor = db_connection.cursor()
        user_info = db.getActiveUserInfo()
        for user in user_info:
            sql = "select * from encrypted_files where user_id = %s"
            mycursor.execute(sql, (user[1],))
            results = mycursor.fetchall()
            for data in encrypted_files_tableview.get_children():
                encrypted_files_tableview.delete(data)
            for row in results:
                print(row)
                encrypted_files_tableview.insert("", index='end', values=(row[0], row[1], row[3], row[5]))
            db_connection.close()

        # ListBox

    encrypted_files_tableview = Treeview(frame, height=17)
    encrypted_files_tableview['columns'] = ('file_id', 'file_name', 'file_path', 'encryption_date')
    encrypted_files_tableview.column("file_id", anchor=CENTER, width=80)
    encrypted_files_tableview.column("file_name", anchor=CENTER, width=200)
    encrypted_files_tableview.column("file_path", anchor=CENTER, width=270)
    encrypted_files_tableview.column("encryption_date", anchor=CENTER, width=200)
    encrypted_files_tableview.column("#0", width=0, stretch=NO)
    encrypted_files_tableview.heading("file_id", text="Id", anchor=CENTER)
    encrypted_files_tableview.heading("file_name", text="File Name", anchor=CENTER)
    encrypted_files_tableview.heading("file_path", text="Path", anchor=CENTER)
    encrypted_files_tableview.heading("encryption_date", text="Encryption Date", anchor=CENTER)

    encrypted_files_tableview.place(x=130, y=80)

    fetchData()

    def delete():
        selected_item = encrypted_files_tableview.selection()[0]
        id = encrypted_files_tableview.item(selected_item)['values'][0]
        if selected_item == "":
            showinfo("Error", "Please select row")
        else:
            try:
                db.removeEncryptedFile(id)
                encrypted_files_tableview.delete(selected_item)
                fetchData()
            except Exception as e:
                showinfo("Error", "Error deleting record")

    def select_file():
        filetypes = (
            ("Text files", "*.txt"),
            ("RTF", "*.rtf"),
            ('pdf file', '*.pdf'),
            ('docx file', '*.docx'),
            ('mp3 file', '*.mp3'),
            ('mp4 file', '*.mp4'),
            ('AVI file', '*.avi'),
            ('encrypted file', '*.enc'),
            ("all files", "*.*")
        )

        filename = filedialog.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)

        if filename == "":
            return NONE

        path = Path(filename)

        encrypt_pass = simpledialog.askstring(title="Set Password", prompt="Set a password", parent=root)
        while encrypt_pass == "" or encrypt_pass == NONE:
            if encrypt_pass == NONE:
                return NONE
            showinfo("Error", "Please input password")
            encrypt_pass = simpledialog.askstring(title="Set Password", prompt="Set a password", parent=root)
        if encrypt_pass != "" or encrypt_pass != NONE:
            encrypt_pass_confirm = simpledialog.askstring(title="Confirm Password", prompt="Confirm Password",
                                                          parent=root)
            if encrypt_pass_confirm is NONE:
                return NONE

            if encrypt_pass_confirm == "":
                showinfo("Error", "Please input password")

            if encrypt_pass == encrypt_pass_confirm:
                encrypt_pass_confirm = encrypt_pass_confirm.encode('UTF-8')
                encrypt_pass_confirm = pad(encrypt_pass_confirm, AES.block_size)
                encrypt(filename, encrypt_pass_confirm)
                now = datetime.now()
                dt_String = now.strftime("%d/%m/%Y %H:%M:%S")
                parent = os.path.dirname(filename)
                db.addEncryptedFile(path.stem, path.suffix, filename, parent, dt_String)
                fetchData()

            else:
                showinfo(
                    title='Error',
                    message='Passwords not matching'
                )

    def disableBtnWhileNoSelection():
        showFolderBtn["state"] = "disabled"
        decryptBtn["state"] = "disabled"

    def enableBtnWhileSelections():
        showFolderBtn["state"] = "enabled"
        decryptBtn["state"] = "enabled"

    def decrypt_file():
        selected_item = encrypted_files_tableview.selection()[0]
        if selected_item == "":
            showinfo("Error", "Please select file")
        else:
            id = encrypted_files_tableview.item(selected_item)['values'][0]
            filepath = encrypted_files_tableview.item(selected_item)['values'][2]
            filename = encrypted_files_tableview.item(selected_item)['values'][1]
            decrypt_pass = simpledialog.askstring(title="Enter Password", prompt="Enter password", parent=root)
            parent = os.path.dirname(filepath)
            file_out = parent + '/' + filename + '_decrypted' + db.getFileExtension(id)
            decryption = decrypt(filepath + '.enc', decrypt_pass, file_out)
            if decryption:
                delete()

    def showFolder():
        selected_item = encrypted_files_tableview.selection()[0]
        if selected_item == "":
            showinfo("Error", "Please select file")
        else:
            filepath = encrypted_files_tableview.item(selected_item)['values'][2]
            parent = os.path.dirname(filepath)
            if platform.system() == "Windows":
                os.startfile(parent)
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", parent])
            else:
                subprocess.Popen(["xdg-open", parent])

    Button(frame, width=9, pady=7, text="Manage Account", bg='#57a1f8', fg='black', border=0).place(
        x=8, y=200)
    Button(frame, width=9, pady=7, text="Encrypt File", command=select_file, bg='#57a1f8', fg='black', border=0).place(
        x=8, y=300)
    decryptBtn = Button(frame, width=9, pady=7, text="Decrypt File", command=decrypt_file, bg='#57a1f8', fg='black',
                        border=0)
    decryptBtn.place(x=770, y=430)
    showFolderBtn = Button(frame, width=9, pady=7, text="Show in folder", command=lambda: showFolder(), bg='#57a1f8', fg='black', border=0)
    showFolderBtn.place(x=140, y=430)
    # disableBtnWhileNoSelection()
    root.mainloop()


if db.userIsLoggedIn():
    home_main()
else:
    init()
