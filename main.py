# This is a random password generator #

from tkinter import *
from tkinter import messagebox
from random import choice, shuffle
import pyperclip
import json

# ---------------------------- PASSWORD GENERATORS ------------------------------- #

# CHARACTER BANK

LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
           ]
NUMBERS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
SYMBOLS = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


# password type

# All characters
# Easy to say = Avoids numbers & Special Chars
# Easy to read = avoids ambiguous chars I: 1, O: 0


def pw_gen_all_char(user_length=12):

    new_length = user_length//3
    print(f"current number = {new_length}")

    choose_letter = [choice(LETTERS) for x in range(new_length)]
    choose_number = [choice(NUMBERS) for x in range(new_length)]
    choose_symbol = [choice(SYMBOLS) for x in range(new_length)]

    password_list = choose_letter + choose_number + choose_symbol
    shuffle(password_list)

    return "".join(password_list)


def pw_gen_easy_to_say(pw_length=12):

    print(f"current number = {pw_length}")
    choose_letter = [choice(LETTERS) for x in range(pw_length)]

    shuffle(choose_letter)

    return "".join(choose_letter)


def pw_gen_easy_to_read(user_length=12):

    print(f"current number = {user_length}")
    password = []

    while len(password) < user_length:

        choose_letter = choice(LETTERS)
        if choose_letter == "I" or choose_letter == "O" or choose_letter == "l":
            pass
        else:
            password.append(choose_letter)

        choose_symbol = choice(SYMBOLS)
        if len(password) < user_length:
            if choose_symbol == "!":
                pass
            else:
                password.append(choose_symbol)

        choose_number = choice(NUMBERS)
        if len(password) < user_length:
            if choose_letter == "1" or choose_letter == "0":
                pass
            else:
                password.append(choose_number)

        return "".join(password)


password_gen = True

# while password_gen:
#     prompt_type = int(input("What type of password would you like? \nType '1' for "
#                             "'All char'\nType '2' for 'Easy to say'\nType '3' for 'Easy to read': \nType '0' to quit"
#                             "\n\n"))
#
#     if prompt_type == 1:
#         prompt_number = int(input("Type in a number for the length of password: "))
#         pw = pw_gen_all_char(prompt_number//3)
#         print(f"Your password is:  {pw} \n")
#
#     elif prompt_type == 2:
#         prompt_number = int(input("Type in a number for the length of password: "))
#         pw = pw_gen_easy_to_say(prompt_number)
#         print(f"Your password is:  {pw} \n")
#
#     elif prompt_type == 3:
#         prompt_number = int(input("Type in a number for the length of password: "))
#         pw = pw_gen_easy_to_read(prompt_number)
#         print(f"Your password is:  {pw} \n")
#
#     elif prompt_type == 0:
#         print("Thanks for using the password generator!")
#         password_gen = False
#
#     else:
#         print("Invalid answer")
#         continue


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save(password_entry=None, email_entry=None, website_entry=None):

    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")
    else:
        try:
            with open("data.json", "r") as data_file:
                # Reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # Updating old data with new data
            data.update(new_data)

            with open("data.json", "w") as data_file:
                # Saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password(website_entry=None):
    website = website_entry.get()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website} exists.")

# ---------------------------- UI SETUP ------------------------------- #


master = Tk()
master.title("Password Manager")
master.config(padx=50, pady=50)


# declaring intvar for radio buttons and password_length to store values
radio_var = IntVar()
pw_length = StringVar(value="12")


# func grabs value of password_length button and returns value
# this value is will be submitted as arg for password generator funcs
def grab_val():
    test = pw_length.get()
    print(test)
    return test


# func returns values of each radio button for window two_a
# occurs after generate password button is clicked
def type_selection(entry, text1, text2, text3):
    if radio_var.get() == 1:
        print(text1)
        return entry.insert(0, text1)
    elif radio_var.get() == 2:
        print(text2)
        return entry.insert(0, text2)
    elif radio_var.get() == 3:
        print(text3)
        return entry.insert(0, text3)
    else:
        pass


def create_save_window():

    # Toplevel object which will be treated as a new window
    two_a = Toplevel(master)
    two_a.title("Password Manager | Create / Save")

    # logo for window
    new_win_canvas = Canvas(master=two_a, height=300, width=200)
    logo_lock = PhotoImage(file="logo.png")
    new_win_canvas.create_image(150, 150, image=logo_lock)
    new_win_canvas.image = logo_lock  # necessary step b/c the image gets lost when transferring to another page
    new_win_canvas.grid(row=0, column=1, columnspan=2)

    # website entry box and label
    website_label = Label(master=two_a, text="Website:")
    website_label.grid(row=1, column=0)
    website_entry = Entry(master=two_a, width=30)
    website_entry.grid(row=1, column=1, columnspan=2)
    website_entry.insert(0, "website.com")
    website_entry.focus()

    # email entry box and label
    email_label = Label(master=two_a, text="Email / Username:")
    email_label.grid(row=2, column=0, pady=10, padx=10)
    email_entry = Entry(master=two_a, width=30)
    email_entry.grid(row=2, column=1, columnspan=2)
    email_entry.insert(0, "email@test.com")

    # password entry box and label
    password_label = Label(master=two_a, text="Password:")
    password_label.grid(row=3, column=0, pady=10, padx=10)

    password_entry = Entry(master=two_a, width=30)
    password_entry.grid(row=3, column=1, columnspan=2)

    # password length label and entry box
    pw_length_label = Label(master=two_a, text="Choose a password length")
    pw_length_label.grid(row=4, column=0, padx=10, pady=10)

    pw_length_entry_box = Entry(master=two_a, width=10, textvariable=pw_length)
    pw_length_entry_box.grid(row=4, column=1)

    pw_length_button = Button(master=two_a, text="Submit", command=grab_val)
    pw_length_button.grid(row=4, column=2)

    # password type select
    password_type_label = Label(master=two_a, text="Password Type: ")
    password_type_label.grid(row=5, column=0, padx=10)

    r1 = Radiobutton(master=two_a, text='All characters', variable=radio_var, value=1, command=all_char_test)
    r1.grid(row=5, column=1)
    r1_text = r1.cget("command")

    r2 = Radiobutton(master=two_a, text='Easy to say', variable=radio_var, value=2, command=ez_say_test)
    r2.grid(row=5, column=2)
    r2_text = r2.cget("command")

    r3 = Radiobutton(master=two_a, text='Easy to read', variable=radio_var, value=3, command=ez_read_test)
    r3.grid(row=5, column=3)
    r3_text = r3.cget("command")

    # generate password button - will trigger password generation when clicked IF a radio button is selected
    password_gen_button = Button(master=two_a, text="Generate Password", width=50,
                                 command=lambda: type_selection(entry=password_entry,
                                                                text1=r1_text, text2=r2_text, text3=r3_text)
                                 )
    password_gen_button.grid(row=6, column=1, columnspan=3, pady=10)


password_length_val = int(grab_val())
all_char_test = pw_gen_all_char(password_length_val)
ez_say_test = pw_gen_easy_to_say(password_length_val)
ez_read_test = pw_gen_easy_to_read(password_length_val)


canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)
button = Button(master=master, text="Create Password", command=create_save_window)
button.grid(row=1, column=1)


master.mainloop()

# window = Tk()
# window.title("Password Manager")
# window.config(padx=50, pady=50)
#
# canvas = Canvas(height=200, width=200)
# logo_img = PhotoImage(file="logo.png")
# canvas.create_image(100, 100, image=logo_img)
# canvas.grid(row=0, column=1)
#
#
# # Test for Text variable -- spinbox
# test_var = ["1", "2", "3"]
#
#
# # New Window
# #Labels
# website_label = Label(text="Website:")
# website_label.grid(row=1, column=0)
# email_label = Label(text="Email/Username:")
# email_label.grid(row=2, column=0)
# password_label = Label(text="Password:")
# password_label.grid(row=3, column=0)
#
# #Entries
# website_entry = Entry(width=21)
# website_entry.grid(row=1, column=1)
# website_entry.focus()
# email_entry = Entry(width=35)
# email_entry.grid(row=2, column=1, columnspan=2)
# email_entry.insert(0, "email@test.com")
# password_entry = Entry(width=21)
# password_entry.grid(row=3, column=1)
#
# # Buttons
# search_button = Button(text="Search", width=13, command=find_password)
# search_button.grid(row=1, column=2)
# add_button = Button(text="Add", width=36, command=save)
# add_button.grid(row=4, column=1, columnspan=2)
#
#
# # Password Buttons and Slider
# generate_password_button = Button(text="Generate Password", command=pw_gen_easy_to_read(12))
# generate_password_button.grid(row=3, column=2)
# window.mainloop()




