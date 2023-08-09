import tkinter as tk
from tkinter import messagebox
import random
import pyperclip
import json

BLACK = "#272829"
WHITE = "#FAF3F0"
RED = "#C51605"
GRAY = "#D8D9DA"

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    """Generates a random password."""
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v','w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R','S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [random.choice(letters) for char in range(random.randint(8, 10))]
    password_symbols = [random.choice(symbols) for char in range(random.randint(2, 4))]
    password_numbers = [random.choice(numbers) for char in range(random.randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers

    # randomizes the characters, numbers and symbols
    random.shuffle(password_list)

    # combines all the characters, numbers and symbols together into one variable.
    password = "".join(password_list)

    # generates the password in the entry.
    password_entry.insert(0, password)
    # saves the password into the clip board to be pasted.
    pyperclip.copy(password)

    print(f"Your password is: {password}")


def search_data():
    """Searches for account password."""
    website = website_entry.get()
    try:
        with open("data.json", "r") as data:
            file = json.load(data)
    except FileNotFoundError:
        messagebox.showinfo(title="File Error!", message="No Data File Found!")
    else:
        if website in file:
            messagebox.showinfo(title="Information Found!", message=f"{website} Information: \nEmail: "
                                                                    f"{file[website]['email']}"
                                                                    f"\nPassword: {file[website]['password']}")
        else:
            messagebox.showinfo(title="Website Entry Error!", message=f"{website} can not be found!")

# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    """Saves the entry data into a txt file."""
    website = website_entry.get()
    email = email_user_entry.get()
    password = password_entry.get()
    new_data = {website: {
        "email": email,
        "password": password,
    }}
    if len(website_entry.get()) == 0 or len(password_entry.get()) == 0:
        messagebox.showinfo("Blank Entry Error!", "Error: Entry left blank!")
    else:
        is_ok = messagebox.askokcancel(title=website_entry.get(), message=f"These are the details entered: "f"\nEmail: "
                                                                          f"{email_user_entry.get()} "f"\nPassword: "
                                                                          f"{password_entry.get()} \n Is it ok to save?")
        if is_ok:
            try:
                with open("data.json", "r") as data:
                    # reading old data.
                    file = json.load(data)
            except FileNotFoundError:
                with open("data.json", "w") as data:
                    json.dump(new_data, data, indent=4)
            else:
                # updating old data with new data.
                file.update(new_data)
                with open("data.json", "w") as data:
                    # saving updated data.
                    json.dump(file, data, indent=4)
            finally:
                # clear the data from the entries.
                website_entry.delete(0, len(website_entry.get()))
                password_entry.delete(0, len(password_entry.get()))


# ---------------------------- UI SETUP ------------------------------- #
window = tk.Tk()
window.title("Password Generator!")
window.config(padx=40, pady=40, bg=BLACK)

# Canvas
canvas = tk.Canvas(width=200, height=200, bg=BLACK, highlightthickness=0)
lock_pic = tk.PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock_pic)
canvas.grid(column=1, row=1)

# Website Label and Entry
website_label = tk.Label(text="Website:", bg=BLACK, fg=WHITE)
website_label.grid(column=0, row=2)

website_entry = tk.Entry(width=35)
website_entry.grid(column=1, row=2, columnspan=2)
website_entry.focus()

# Search Button
search_button = tk.Button(text="Search", width=13, command=search_data, bg=GRAY, fg=BLACK)
search_button.grid(column=3, row=2)

# Email/User Label and Entry
email_user_label = tk.Label(text="Email/Username:", bg=BLACK, fg=WHITE)
email_user_label.grid(column=0, row=3)

email_user_entry = tk.Entry(width=35)
email_user_entry.grid(column=1, row=3, columnspan=2)
email_user_entry.insert(0, "sydney@email.com")

# Password Label and Entry
password_label = tk.Label(text="Password:", bg=BLACK, fg=WHITE)
password_label.grid(column=0, row=4)

password_entry = tk.Entry(width=21)
password_entry.grid(column=1, row=4)

# Generate password Button
generate_button = tk.Button(text="Generate Password", command=generate_password, bg=GRAY, fg=BLACK)
generate_button.grid(column=2, row=4)

# Add Button
add_button = tk.Button(text="Add", width=36, command=save, bg=GRAY, fg=BLACK)
add_button.grid(column=1, row=5, columnspan=2)


window.mainloop()
