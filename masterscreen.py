import tkinter

# TODO: Add update_password functionality
# TODO: Debug the code and fix the bug which is causing multiple windows to open.

_MASTER_PASS = 'ohhimark'
# I have used this only for demonstration purposes. In a real program, we would probably
# store this like an API key in our environment variables and use the os module to access 
# them
_MASTER_PASS_FILE = 'passwords/master_pass.txt'
_EMAIL_FILE = 'passwords/email.txt'
_FONT_TUPLE = ('Hack Nerd Font', 15)


def encrypt(text):
    enc_text = ""
    for character in text:
        new_char = chr(ord(character) + 16)
        enc_text += new_char
    return enc_text
    

def decrypt(enc_text):
    dec_text = ""
    for character in enc_text:
        new_char = chr(ord(character) - 16)
        dec_text += new_char
    return dec_text


def write_file(file_path, text):
    with open(file_path, 'w') as pass_file:
        pass_file.write(encrypt(_MASTER_PASS)) 


def read_file(file_path):
    decrypted_text = ""
    with open(file_path,'r') as read_file:
        for content in read_file:
            decrypted_text = decrypt(content)
    return decrypted_text


def err_message(error_text):
    error_root = tkinter.Tk()
    error_root.title = 'Wrong'
    err_label = tkinter.Label(error_root, text=error_text)
    err_label.pack()
    err_btn = tkinter.Button(error_root, text='OK', command=error_root.destroy)
    err_btn.pack()
   

def add_email(email, password):
    with open(_EMAIL_FILE, 'a') as email_file:
        email_file.write(f'{email}\t{password}\n')
    err_message('New entry has been created!')
    
    
def login(root_file):
    root_file.destroy()
    main_root = tkinter.Tk()
    main_root.title = 'Main Root'
    main_root.geometry('500x200')
    main_root['padx'] = 90

    email_label = tkinter.Label(main_root, text='Enter Email: ', font=_FONT_TUPLE)
    email_entry = tkinter.Entry(main_root, width=15, font=_FONT_TUPLE)

    password_label = tkinter.Label(main_root, text='Enter Password: ', font=_FONT_TUPLE)
    password_entry = tkinter.Entry(main_root, width=15, show='*', font=_FONT_TUPLE)

    email_label.grid(row=0, column=0)
    email_entry.grid(row=0, column=1)

    password_label.grid(row=1, column=0)
    password_entry.grid(row=1, column=1)


    def verify():
        email = email_entry.get()
        password = password_entry.get()
        if email == "" or password == "":
            err_message("Please fill out both the fields!")
        else:
            with open(_EMAIL_FILE, 'r') as email_file:
                for entry in email_file:
                    entry_email = entry.split('\t')
                    if entry_email[0] == email:
                        err_message("The Email already exists.")
                        break
                    elif entry_email[0] != email:
                        add_email(email, password)


    main_root_submit_button = tkinter.Button(main_root, text='Submit', command=verify)

    main_root_submit_button.grid(row=2, column=0, columnspan=2)
    main_root_submit_button['padx'] = 30


root = tkinter.Tk()
root.title = 'Master Screen'
root.geometry('500x200')
root['padx'] = 50
root['pady'] = 70


def on_press():
    password = password_field.get()
    corr_pass = read_file(_MASTER_PASS_FILE)

    if password == corr_pass:
        login(root)
    else:
        err_message("Either the password field is empty or it is wrong!")


master_label = tkinter.Label(root, text='Enter the master password:', font=_FONT_TUPLE)
password_field = tkinter.Entry(root, show='*', width=15, font=_FONT_TUPLE)

master_label.grid(column=0, row=0)
password_field.grid(column=1, row=0)

submit_button = tkinter.Button(root, text='Submit', command=on_press)
submit_button.grid(row=1, column=0, columnspan=2)
submit_button['padx'] = 30

root.mainloop()

write_file(_MASTER_PASS_FILE, _MASTER_PASS)
