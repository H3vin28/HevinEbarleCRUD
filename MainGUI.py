import sqlite3
import hashlib
import sys
import tkinter as tk
import tkinter as tk_image
from tkinter import messagebox
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from datetime import datetime
import mysql.connector

# master_conn = mysql.connector.connect(host="localhost", user="root", password="", database="barangay_db")
# master_cursor = master_conn.cursor()

conn = sqlite3.connect('barangay.db')
cursor = conn.cursor()

def delete_member_process():
    selected_item = member_table.selection()
    if selected_item:
        item_values = member_table.item(selected_item)['values']
        response = messagebox.askyesno("System Warning", f"Are you sure you want to delete this member?\n\nName: {item_values[2]}, {item_values[1]} {item_values[3]}")
        if response:  # True if "Yes" is clicked
            query = f"DELETE FROM members WHERE id = {item_values[0]}"
            cursor.execute(query)
            conn.commit()

            # master_cursor.execute(query)
            # master_conn.commit()

            messagebox.showinfo('Success', 'Family member successfully deleted!')
            display_residents()
            get_members(item_values[9])
    else:
        messagebox.showwarning('System Warning', 'Select row first!')
def get_members(head_id):
    for row in member_table.get_children():
        member_table.delete(row)
    cursor.execute(f'SELECT * FROM members WHERE head_id = {head_id}')
    rows = cursor.fetchall()
    for row in rows:
        member_table.insert('', tk.END, values=row)
def add_update_member_process(status):
    fname = firstname_mem.get()
    lname = lastname_mem.get()
    mname = middle_name_mem.get()
    ext = extension_mem.get()
    birthday = birthday_mem.get()
    gender = gender_mem.get()
    civil_status = civil_status_mem.get()
    relationship = relationship_mem.get()
    if ((fname != "Enter Firstname") and
        (lname != "Enter Lastname") and
        (birthday != "Ex. 01-31-1990") and
        (civil_status != "Select Here!") and
        (gender != "Select Here!") and
        (relationship != "Enter Relationship")):
        head_id = hidden_head_id.get()
        if mname == "Enter Middle Name":
            mname = ""
        if ext == "Ex. Jr., Sr.":
            ext = ""

        if status == "add":
            query = f"""INSERT INTO members
                (firstname, lastname, middle_name, extension, gender, birthday, civil_status, relationship, head_id)
                VALUES ('{fname}','{lname}','{mname}','{ext}','{gender}','{birthday}','{civil_status}','{relationship}','{head_id}') """
            cursor.execute(query)
            conn.commit()
            # master_cursor.execute(query)
            # master_conn.commit()
            messagebox.showwarning("SYSTEM INFORMATION", "New member successfully added!")
        else:
            member_id = hidden_member_id.get()
            query = f""" UPDATE members SET 
                    firstname = '{fname}', 
                    lastname = '{lname}', 
                    middle_name = '{mname}', 
                    extension = '{ext}', 
                    gender = '{gender}', 
                    birthday = '{birthday}', 
                    civil_status = '{civil_status}', 
                    relationship = '{relationship}'
                    WHERE id = {member_id}"""
            cursor.execute(query)
            conn.commit()
            # master_cursor.execute(query)
            # master_conn.commit()
            messagebox.showwarning("SYSTEM INFORMATION", "Family member successfully updated!")
        get_members(head_id)
        close_add_member_page()
    else:
        messagebox.showwarning("SYSTEM WARNING", "Datas are required! \n\nNote: Except Middle Name and Extension.")
def add_member_open_form():
    member_table.place_forget()
    add_member_form.place(x=15, y=130, width=920, height=470)
    firstname_mem.delete(0, tk.END)
    lastname_mem.delete(0, tk.END)
    middle_name_mem.delete(0, tk.END)
    extension_mem.delete(0, tk.END)
    birthday_mem.delete(0, tk.END)
    relationship_mem.delete(0, tk.END)
    add_placeholder(firstname_mem, "Enter Firstname")
    add_placeholder(lastname_mem, "Enter Lastname")
    add_placeholder(middle_name_mem, "Enter Middle Name")
    add_placeholder(extension_mem, "Ex. Jr., Sr.")
    add_placeholder(birthday_mem, "Ex. 01-31-1990")
    add_placeholder(relationship_mem, "Enter Relationship")

    gender_mem.set("Select Here!")
    civil_status_mem.set("Select Here!")
    add_member_button.place(x=650, y=230, width=200, height=30)
    update_member_button.place_forget()
def update_member_open_form():
    selected_item = member_table.selection()
    if selected_item:
        item_values = member_table.item(selected_item)['values']
        member_table.place_forget()
        add_member_form.place(x=15, y=130, width=920, height=470)
        add_member_button.place_forget()
        update_member_button.place(x=650, y=230, width=200, height=30)
        hidden_member_id.delete(0, tk.END)
        hidden_member_id.insert(0, item_values[0])

        firstname_mem.delete(0, tk.END)
        firstname_mem.insert(0, item_values[1])
        lastname_mem.delete(0, tk.END)
        lastname_mem.insert(0, item_values[2])
        middle_name_mem.delete(0, tk.END)
        middle_name_mem.insert(0, item_values[3])
        extension_mem.delete(0, tk.END)
        extension_mem.insert(0, item_values[4])
        birthday_mem.delete(0, tk.END)
        birthday_mem.insert(0, item_values[6])
        relationship_mem.delete(0, tk.END)
        relationship_mem.insert(0, item_values[8])

        gender_mem.set(item_values[5])
        civil_status_mem.set(item_values[7])

        firstname_mem.config(fg="black")
        lastname_mem.config(fg="black")
        middle_name_mem.config(fg="black")
        extension_mem.config(fg="black")
        birthday_mem.config(fg="black")
        relationship_mem.config(fg="black")
    else:
        messagebox.showwarning('System Warning', 'Select row first!')
def view_family_member():
    selected_item = tree.selection()
    if selected_item:
        connect_db()
        family_member_page.deiconify()
        home.withdraw()
        head_id = hid_id.get()

        hidden_head_id.delete(0, tk.END)
        hidden_head_id.insert(0, head_id)

        cursor.execute(f'SELECT * FROM residents WHERE id = {head_id}')
        row = cursor.fetchone()
        head_label.config(text=f"Head of the Family: {row[2]}, {row[1]}  {row[4]} {row[3]}")

        get_members(head_id)
    else:
        messagebox.showwarning('System Warning', 'Select row first!')
def close_add_member_page():
    firstname_mem.delete(0, tk.END)
    lastname_mem.delete(0, tk.END)
    middle_name_mem.delete(0, tk.END)
    extension_mem.delete(0, tk.END)
    birthday_mem.delete(0, tk.END)
    relationship_mem.delete(0, tk.END)
    add_placeholder(firstname_mem, "Enter Firstname")
    add_placeholder(lastname_mem, "Enter Lastname")
    add_placeholder(middle_name_mem, "Enter Middle Name")
    add_placeholder(extension_mem, "Ex. Jr., Sr.")
    add_placeholder(birthday_mem, "Ex. 01-31-1990")
    add_placeholder(relationship_mem, "Enter Relationship")

    gender_mem.set("Select Here!")
    civil_status_mem.set("Select Here!")
    member_table.place(x=15, y=130, width=920, height=470)
    add_member_form.place_forget()
def add_purok():
    add_purok_box.deiconify()
def add_new_purok_process():
    purok_name = purok_entry.get()
    query = f"INSERT INTO purok(purok_name) VALUES ('{purok_name}')"
    cursor.execute(query)
    conn.commit()
    # master_cursor.execute(query)
    # master_conn.commit()
    messagebox.showinfo("SYSTEM INFORMATION", "New purok successfully added!")
    add_purok_box.withdraw()
    purok_entry.delete(0, tk.END)
    add_placeholder(purok_entry, "Enter Purok Name")
    display_dashboard()
def display_purok():
    custom_box = tk.Tk()
    custom_box.title("ALL PUROK")
    tp = count_records("purok") * 30
    custom_box.geometry(f"300x{tp}")
    custom_box.resizable(False, False)
    custom_box.grid_columnconfigure(0, weight=1)

    query = """ SELECT * FROM purok """
    cursor.execute(query)
    rows = cursor.fetchall()
    y = 0
    for row in rows:
        y += 1
        (Label(custom_box, text=row[1], font=("Arial", 14))
            .grid(row=y, column=0, sticky="ew"))
def count_records(table):
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    count = cursor.fetchone()[0]
    return count
def delete_process():
    id = hid_id.get()
    if id != "":
        response = messagebox.askyesno("System Warning", "Are you sure you want to delete this data?")
        if response:
            query = f"DELETE FROM residents WHERE id = {id}"
            cursor.execute(query)
            conn.commit()
            # master_cursor.execute(query)
            # master_conn.commit()
            messagebox.showinfo('Success', 'Head of the family successfully deleted!')
            display_residents()
    else:
        messagebox.showwarning("System Warning", "Select row first!")
def update_resident():
    selected_item = tree.selection()
    if selected_item:
        update_head_form.deiconify()
    else:
        messagebox.showwarning('System Warning', 'Select row first!')
def update_head_process():
    up_val_id = up_id.get()
    up_val_fname = up_firstname.get()
    up_val_lname = up_lastname.get()
    up_val_mi = up_middlename.get()
    up_val_ext = up_extension.get()
    up_val_gender = up_gender.get()
    up_val_birthday = up_birthday.get()
    up_val_civil_status = up_civil_status.get()
    up_val_purok = up_purok.get()

    if ((up_val_fname != "Enter Firstname") and
            (up_val_lname != "Enter Lastname") and
            (up_val_birthday != "Ex. 01-31-1990") and
            (up_val_gender != "Select Here!") and
            (up_val_civil_status != "Select Here!") and
            (up_val_purok != "Select Here!")):
        if up_val_ext == "Ex. Jr.":
            up_val_ext = ""
        if up_val_mi == "Enter Middle Name":
            up_val_mi = ""

        query = f""" UPDATE residents SET 
                    firstname = '{up_val_fname}', 
                    lastname = '{up_val_lname}', 
                    middle_name = '{up_val_mi}', 
                    extension = '{up_val_ext}', 
                    gender = '{up_val_gender}', 
                    birthday = '{up_val_birthday}', 
                    civil_status = '{up_val_civil_status}', 
                    purok = '{up_val_purok}' 
                    WHERE id = '{up_val_id}'"""
        cursor.execute(query)
        conn.commit()
        # master_cursor.execute(query)
        # master_conn.commit()
        display_residents()
        messagebox.showinfo("System Information", "Data successfully update!")
        update_head_form.withdraw()
    else:
        messagebox.showwarning('Warning', 'Fields are required. Except extension!')
def populate_entries(event):
    selected_item = tree.selection()
    if selected_item:
        item_values = tree.item(selected_item)['values']
        up_id.config(state=NORMAL)
        up_id.delete(0, tk.END)
        up_id.insert(0, item_values[0])
        up_id.config(state=DISABLED)
        up_firstname.delete(0, tk.END)
        up_firstname.insert(0, item_values[1])
        up_lastname.delete(0, tk.END)
        up_lastname.insert(0, item_values[2])
        up_middlename.delete(0, tk.END)
        up_middlename.insert(0, item_values[3])
        up_extension.delete(0, tk.END)
        up_extension.insert(0, item_values[4])
        up_gender.set(item_values[5])
        up_birthday.delete(0, tk.END)
        up_birthday.insert(0, item_values[6])
        up_civil_status.set(item_values[7])
        up_purok.set(item_values[8])
        hid_id.delete(0, tk.END)
        hid_id.insert(0, item_values[0])
def search_residents():
    search_value = search_entry.get()
    if search_value != "":
        for row in tree.get_children():
            tree.delete(row)

        # conn = sqlite3.connect('barangay.db')
        # cursor = conn.cursor()
        query = """
        SELECT * FROM residents WHERE firstname LIKE ? OR lastname LIKE ?
        OR middle_name LIKE ? OR gender LIKE ? OR civil_status LIKE ?
        OR purok LIKE ?
        """
        cursor.execute(query, (f"%{search_value}%",f"%{search_value}%",f"%{search_value}%",f"%{search_value}%",f"%{search_value}%",f"%{search_value}%",))
        rows = cursor.fetchall()
        for row in rows:
            tree.insert('', tk.END, values=row)
        # conn.close()
    else:
        display_residents()
def on_closing():
    sys.exit()
def on_closing_update():
    update_head_form.withdraw()
def on_closing_members_page():
    close_add_member_page()
    family_member_page.withdraw()
    home.deiconify()
    display_residents()
def on_closing_add_purok_box():
    add_purok_box.withdraw()
def display_add_form():
    add_purok_box.withdraw()
    clear_add_form()
    menu_text.config(text="Head of Family Form >")
    add_screen.place(x=200, y=100, width="850", height="230")
    message_widget.place(x=200, y=350)
    total_households.place_forget()
    total_residents.place_forget()
    total_purok.place_forget()
    tree.place_forget()
    search_button.place_forget()
    search_entry.place_forget()
    view_member.place_forget()
    delete_resident.place_forget()
    update_data.place_forget()
    update_data.place_forget()

    # conn = sqlite3.connect('barangay.db')
    # cursor = conn.cursor()
    cursor.execute('SELECT * FROM purok')
    rows = cursor.fetchall()
    values = []
    for row in rows:
        values.append(row[1])
    # conn.close()
    purok.configure(values=values)
def add_process():
    fistname_inputted = firstname.get()
    lastname_inputted = lastname.get()
    middle_name_inputted = middle_name.get()
    extension_inputted = extension.get()
    birthday_inputted = birthday.get()
    gender_inputted = gender.get()
    civil_status_inputted = civil_status.get()
    purok_inputted = purok.get()

    if ((fistname_inputted != "Enter Firstname") and
            (lastname_inputted != "Enter Lastname") and
            (birthday_inputted != "Ex. 01-31-1990") and
            (gender_inputted != "Select Here!") and
            (civil_status_inputted != "Select Here!") and
            (purok_inputted != "Select Here!")):
        if extension_inputted == "Ex. Jr.":
            extension_inputted = ""
        if middle_name_inputted == "Enter Middle Name":
            middle_name_inputted = ""

        query = f"""INSERT INTO residents (firstname, lastname, middle_name, extension, gender, birthday, civil_status, purok) 
                VALUES ('{fistname_inputted}', '{lastname_inputted}', '{middle_name_inputted}', '{extension_inputted}', '{gender_inputted}', '{birthday_inputted}', '{civil_status_inputted}', '{purok_inputted}')"""
        cursor.execute(query)
        conn.commit()

        # master_cursor.execute(query)
        # master_conn.commit()

        messagebox.showinfo('Success', 'Data inserted successfully.')
        clear_add_form()
    else:
        messagebox.showwarning('Warning', 'Fields are required. Except extension!')
def display_dashboard():
    add_purok_box.withdraw()
    menu_text.config(text="Dashboard >")
    total_households.place(x=520, y=150, width="250", height="100")
    total_residents.place(x=520, y=270, width="250", height="100")
    total_purok.place(x=520, y=390, width="250", height="100")
    tree.place_forget()
    search_button.place_forget()
    search_entry.place_forget()
    view_member.place_forget()
    delete_resident.place_forget()
    update_data.place_forget()
    add_screen.place_forget()
    message_widget.place_forget()
    th = count_records("residents")
    tp = count_records("purok")
    tr = count_records("members") + th
    total_households.config(text=f"Total Households\n{th}")
    total_purok.config(text=f"Total Purok\n{tp}")
    total_residents.config(text=f"Total Residents\n{tr}")
def display_residents():
    add_purok_box.withdraw()
    menu_text.config(text="All Head of the Family >")
    total_households.place_forget()
    total_residents.place_forget()
    total_purok.place_forget()
    tree.place(x=165, y=125, width="920", height="480")
    search_button.place(x=960, y=85, width=125, height=30)
    search_entry.place(x=720, y=85, width=230, height=30)
    view_member.place(x=165, y=85, width=200, height=30)
    update_data.place(x=375, y=85, width=130, height=30)
    delete_resident.place(x=515, y=85, width=150, height=30)
    add_screen.place_forget()
    message_widget.place_forget()

    for row in tree.get_children():
        tree.delete(row)
    cursor.execute('SELECT * FROM residents')
    rows = cursor.fetchall()
    for row in rows:
        tree.insert('', tk.END, values=row)

    cursor1 = conn.cursor()
    cursor1.execute('SELECT * FROM purok')
    rows = cursor1.fetchall()
    values = []
    for row in rows:
        values.append(row[1])
    # conn.close()
    up_purok.configure(values=values)
def start_progress():
    loading_label.place(x=100, y=250, width=300, height=40)
    progress_bar.place(x=100, y=300, width=300, height=40)
    progress_bar["value"] = 0  # Reset progress bar
    max_value = 100
    progress_bar["maximum"] = max_value

    def update_progress(value):
        if value <= 30:
            # Update progress bar value
            progress_bar["value"] = value

            # Update loading text
            loading_label.config(text=f"Loading please wait... ( {value}% )")

            # Schedule the next update
            login.after(31, update_progress, value + 1)
        elif value > 30 and value <= 70:
            # Update progress bar value
            progress_bar["value"] = value
            # Update loading text
            loading_label.config(text=f"Initializing data... ( {value}% )")
            # Schedule the next update
            login.after(71, update_progress, value + 1)
        elif value > 70 and value <= max_value:
            # Update progress bar value
            progress_bar["value"] = value

            # Update loading text
            loading_label.config(text=f"Finalizing all data... ( {value}% )")

            # Schedule the next update
            login.after(100, update_progress, value + 1)
        else:
            display_dashboard()
            home.deiconify()
            login.withdraw()

    update_progress(0)
def logout():
    add_purok_box.withdraw()
    home.withdraw()
    login.deiconify()
def clear_add_form():
    firstname.delete(0, tk.END)
    lastname.delete(0, tk.END)
    middle_name.delete(0, tk.END)
    extension.delete(0, tk.END)
    birthday.delete(0, tk.END)

    add_placeholder(firstname, "Enter Firstname")
    add_placeholder(lastname, "Enter Lastname")
    add_placeholder(middle_name, "Enter Middle Name")
    add_placeholder(extension, "Ex. Jr.")
    add_placeholder(birthday, "Ex. 01-31-1990")

    gender.set("Select Here!")
    civil_status.set("Select Here!")
    purok.set("Select Here!")
def login_process():
    user = username.get()
    get_pass = password.get()
    hash_object = hashlib.sha256(get_pass.encode())
    hash_password = hash_object.hexdigest()

    # Retrieve the hashed password for the given username
    cursor.execute("SELECT username, password FROM users WHERE username = ? AND password = ?", (user, hash_password))
    result = cursor.fetchone()
    # slave_conn.close()

    if result:
        messagebox.showinfo("System Notification", "Login successful!")
        start_progress()
    else:
        messagebox.showwarning("System Warning", "Invalid credentials!")
def toggle_password():
    if password.cget("show") == "":
        password.config(show="•")
        toggle_button.config(text="Show Password")
    else:
        password.config(show="")
        toggle_button.config(text="Hide Password")
def add_placeholder(entry, placeholder_text):
    """Add placeholder text to the Entry widget."""
    entry.insert(0, placeholder_text)  # Insert placeholder text
    entry.config(fg="grey")            # Set placeholder color

    def on_focus_in(event):
        """Remove placeholder text when the user focuses on the Entry."""
        if entry.get() == placeholder_text:
            entry.delete(0, tk.END)  # Remove the placeholder text
            entry.config(fg="black") # Set text color back to normal

    def on_focus_out(event):
        """Restore placeholder text if the Entry is empty."""
        if entry.get() == "":
            entry.insert(0, placeholder_text)
            entry.config(fg="grey")

    entry.bind("<FocusIn>", on_focus_in)   # Bind focus-in event
    entry.bind("<FocusOut>", on_focus_out) # Bind focus-out event
def update_time():
    # Get current date and time
    now = datetime.now()
    current_time = now.strftime("%I:%M:%S %p")  # Format time as HH:MM:SS
    current_date = now.strftime("%B %d, %Y")  # Format date as YYYY-MM-DD

    # Update the labels with current date and time
    date_label.config(text=f"Today is {current_date} {current_time}")
    date_label_member.config(text=f"Today is {current_date} {current_time}")

    # Call this function again after 1000ms (1 second)
    home.after(1000, update_time)
def connect_db():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,   
            password TEXT NOT NULL
        )
    ''')
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS residents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                firstname TEXT NOT NULL,
                lastname TEXT NOT NULL,
                middle_name TEXT NOT NULL,
                extension TEXT NOT NULL,
                gender TEXT NOT NULL,
                birthday TEXT NOT NULL,
                civil_status TEXT NOT NULL,
                purok TEXT NOT NULL
            )
        ''')
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS purok (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                purok_name TEXT NOT NULL UNIQUE
            )
        ''')

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                firstname TEXT NOT NULL,
                lastname TEXT NOT NULL,
                middle_name TEXT NULL,
                extension TEXT NULL,
                gender TEXT NOT NULL,
                birthday TEXT NOT NULL,
                civil_status TEXT NOT NULL,
                relationship TEXT NOT NULL,
                head_id INTEGER NOT NULL
            )
        ''')
    # master_cursor.execute('''
    #         CREATE TABLE IF NOT EXISTS users (
    #             id INTEGER PRIMARY KEY AUTO_INCREMENT,
    #             username TEXT NOT NULL UNIQUE,
    #             password TEXT NOT NULL
    #         )
    #     ''')
    # master_cursor.execute('''
    #             CREATE TABLE IF NOT EXISTS residents (
    #                 id INTEGER PRIMARY KEY AUTO_INCREMENT,
    #                 firstname TEXT NOT NULL,
    #                 lastname TEXT NOT NULL,
    #                 middle_name TEXT NOT NULL,
    #                 extension TEXT NOT NULL,
    #                 gender TEXT NOT NULL,
    #                 birthday TEXT NOT NULL,
    #                 civil_status TEXT NOT NULL,
    #                 purok TEXT NOT NULL
    #             )
    #         ''')
    # master_cursor.execute('''
    #             CREATE TABLE IF NOT EXISTS purok (
    #                 id INTEGER PRIMARY KEY AUTO_INCREMENT,
    #                 purok_name TEXT NOT NULL UNIQUE
    #             )
    #         ''')
    #
    # master_cursor.execute('''
    #             CREATE TABLE IF NOT EXISTS members (
    #                 id INTEGER PRIMARY KEY AUTO_INCREMENT,
    #                 firstname TEXT NOT NULL,
    #                 lastname TEXT NOT NULL,
    #                 middle_name TEXT NULL,
    #                 extension TEXT NULL,
    #                 gender TEXT NOT NULL,
    #                 birthday TEXT NOT NULL,
    #                 civil_status TEXT NOT NULL,
    #                 relationship TEXT NOT NULL,
    #                 head_id INTEGER NOT NULL
    #             )
    #         ''')

    table_name = "users"
    cursor.execute(f"""
        SELECT name 
        FROM sqlite_master 
        WHERE type='table' AND name='{table_name}';
        """)
    exists = cursor.fetchone()[0]

    if exists:
        cursor.execute(f"SELECT COUNT(*) FROM users WHERE username = 'admin'")
        exists1 = cursor.fetchone()[0]
        if exists1 == 0:
            cursor.execute(f"INSERT INTO {table_name} (username, password) VALUES ('admin', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9')")

    # master_cursor.execute(f"""
    #         SELECT COUNT(*)
    #         FROM information_schema.tables
    #         WHERE table_schema = DATABASE()
    #         AND table_name = '{table_name}';
    #     """)
    # exists = master_cursor.fetchone()[0]
    #
    # if exists:
    #     master_cursor.execute(f"SELECT COUNT(*) FROM users WHERE username = 'admin'")
    #     exists1 = master_cursor.fetchone()[0]
    #     if exists1 == 0:
    #         master_cursor.execute(f"INSERT INTO {table_name} (username, password) VALUES ('admin', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9')")
    #
    # master_conn.commit()
    conn.commit()
# UPDATE FORM
update_head_form = tk.Tk()
update_head_form.resizable(False, False)
update_head_form.title("UPDATE HEAD OF FAMILY INFO")
update_head_form.geometry("400x420")
(Label(update_head_form, text="UPDATE FORM", font=("Arial", 18), anchor="center", justify="center", bg="light blue")
    .place(x=0, y=0, width=400, height="50"))

(Label(update_head_form, text="ID No. : ", font=("Arial", 14), anchor="nw")
    .place(x=10, y=70, width=120))
(Label(update_head_form, text="Firstname: ", font=("Arial", 14), anchor="nw")
    .place(x=10, y=100, width=120))
(Label(update_head_form, text="Lastname: ", font=("Arial", 14), anchor="nw")
    .place(x=10, y=130, width=120))
(Label(update_head_form, text="Middle Name: ", font=("Arial", 14), anchor="nw")
    .place(x=10, y=160, width=120))
(Label(update_head_form, text="Extension: ", font=("Arial", 14), anchor="nw")
    .place(x=10, y=190, width=120))
(Label(update_head_form, text="Gender: ", font=("Arial", 14), anchor="nw")
    .place(x=10, y=220, width=120))
(Label(update_head_form, text="Birthday: ", font=("Arial", 14), anchor="nw")
    .place(x=10, y=250, width=120))
(Label(update_head_form, text="Civil Status: ", font=("Arial", 14), anchor="nw")
    .place(x=10, y=280, width=120))
(Label(update_head_form, text="Purok: ", font=("Arial", 14), anchor="nw")
    .place(x=10, y=310, width=120))

up_id = tk.Entry(update_head_form, font=("Arial", 14), bd=1, justify="left")
up_id.place(x=135, y=70, width=250)
up_firstname = tk.Entry(update_head_form, font=("Arial", 14), bd=1, justify="left")
up_firstname.place(x=135, y=100, width=250)
up_lastname = tk.Entry(update_head_form, font=("Arial", 14), bd=1, justify="left")
up_lastname.place(x=135, y=130, width=250)
up_middlename = tk.Entry(update_head_form, font=("Arial", 14), bd=1, justify="left")
up_middlename.place(x=135, y=160, width=250)
up_extension = tk.Entry(update_head_form, font=("Arial", 14), bd=1, justify="left")
up_extension.place(x=135, y=190, width=250)
options = ["Male", "Female"]
up_gender = ttk.Combobox(update_head_form, values=options, font=("Arial", 14))
up_gender.place(x=135, y=220, width=250)
up_birthday = tk.Entry(update_head_form, font=("Arial", 14), bd=1, justify="left")
up_birthday.place(x=135, y=250, width=250)
options1 = ["Single", "Married", "Widowed", "Separated"]
up_civil_status = ttk.Combobox(update_head_form, values=options1, font=("Arial", 14))
up_civil_status.place(x=135, y=280, width=250)
options2 = ["Single", "Married", "Widowed", "Separated"]
up_purok = ttk.Combobox(update_head_form, font=("Arial", 14))
up_purok.place(x=135, y=310, width=250)

(Button(update_head_form, text="UPDATE DATA", font=("Arial", 14), bg="blue", fg="white", command=update_head_process)
    .place(x=80, y=350, width=250))

# LOGIN FORM
login = tk.Tk()
login.resizable(False, False)
login.title("BARANGAY INFORMATION SYSTEM (Login Form)")
login.geometry("500x625")
# background image start
bg = PhotoImage(file="login_bg.png", master=login)
canvas1 = Canvas(login, width=500, height=625)
canvas1.pack(fill="both", expand=True)
canvas1.create_image(0, 0, image=bg, anchor="nw")
# background image end

username = tk.Entry(login, font=("Arial", 16), bd=1, justify="left")
username.place(x=100, y=320, width=300, height=40)
add_placeholder(username, "Enter Username")
password = tk.Entry(login, font=("Arial", 16), bd=1, justify="left", show="•")
password.place(x=100, y=380, width=300, height=40)
add_placeholder(password, "Enter Password")

toggle_button = tk.Button(login, text="Show Password", command=toggle_password)
toggle_button.place(x=100, y=430, width=100, height=30)
(Button(login, text="LOGIN", font=("Arial", 16), bg='white', command=login_process)
 .place(x=100, y=480, width=300, height=40))


loading_label = tk.Label(login, font=("Arial", 14))
progress_bar = ttk.Progressbar(login, orient="horizontal", length=300, mode="determinate")
progress_bar.place_forget()  # Hide the progress bar
loading_label.place_forget()  # Hide the loading label

home = tk_image.Tk()
home.resizable(False, False)
home.configure(background="light blue")
home.title("BARANGAY INFORMATION SYSTEM")
home.geometry("1100x620")

mainScreen = LabelFrame(home, padx=10, pady=0, background="White")
mainScreen.place(x=0, y=0, width=150, height=720)
image1 = Image.open("logo.png")
image1 = image1.resize((100, 100))
image1_tk = ImageTk.PhotoImage(image1, master=home)
label1 = tk_image.Label(mainScreen, image=image1_tk, bg="white")
label1.image = image1_tk
label1.place(x=10, y=20)
(Label(mainScreen, text="Welcome\nAdmin!", font=("arial", 16), bg="white", anchor="center", justify="center")
 .place(x=15, y=130))

(Button(mainScreen, text="Dashboard", font=("Arial Black", 12), fg="white", bg='blue', anchor="center", justify="center", command=display_dashboard)
 .place(x=0, y=190, width=125, height=30))
(Button(mainScreen, text="Display\nHoF", font=("Arial Black", 12), fg="white", bg='blue', anchor="center", justify="center", command=display_residents)
 .place(x=0, y=230, width=125, height=60))
(Button(mainScreen, text="Add Head\nOf Family", font=("Arial Black", 12), fg="white", bg='blue', anchor="center", justify="center", command=display_add_form)
 .place(x=0, y=300, width=125, height=60))
(Button(mainScreen, text="Display\nPurok", font=("Arial Black", 12), fg="white", bg='blue', anchor="center", justify="center", command=display_purok)
 .place(x=0, y=370, width=125, height=60))
(Button(mainScreen, text="Add New\nPurok", font=("Arial Black", 12), fg="white", bg='blue', anchor="center", justify="center", command=add_purok)
 .place(x=0, y=440, width=125, height=60))
(Button(mainScreen, text="Logout", font=("Arial Black", 12), fg="white", bg='blue', anchor="center", justify="center", command=logout)
 .place(x=0, y=510, width=125, height=30))

date_label = tk.Label(home, text="", font=("Arial", 18), bg="light blue")
date_label.place(x=165, y=10)

hid_id = tk.Entry(home, font=("Arial", 18))
# hid_id.place(x=500, y=45)
menu_text = tk.Label(home, text="Dashboard >", font=("Arial", 18), bg="light blue", fg="blue")
menu_text.place(x=165, y=45)

total_households = tk.Label(home, text="", font=("Arial", 18), fg="white", bg="green", anchor="center", justify="center")
total_households.place(x=520, y=150, width="250", height="100")
total_residents = tk.Label(home, text="Total Residents\n60", font=("Arial", 18), fg="white", bg="dark red", anchor="center", justify="center")
total_residents.place(x=520, y=270, width="250", height="100")
total_purok = tk.Label(home, text="No. of Purok\n4", font=("Arial", 18), fg="white", bg="purple", anchor="center", justify="center")
total_purok.place(x=520, y=390, width="250", height="100")

search_button = tk.Button(home, text="Search", font=("Arial Black", 12), anchor="center", justify="center", command=search_residents)
view_member = tk.Button(home, text="View Family Member", font=("Arial Black", 12), bg="green", fg="white", anchor="center", justify="center", command=view_family_member)
update_data = tk.Button(home, text="Update Data", font=("Arial Black", 12), bg="blue", fg="white", anchor="center", justify="center", command=update_resident)
delete_resident = tk.Button(home, text="Delete Resident", font=("Arial Black", 12), bg="dark red", fg="white", anchor="center", justify="center", command=delete_process)
search_entry = tk.Entry(home, font=("Arial Black", 12))
# Create a style object
style = ttk.Style()
style.configure("Treeview.Heading", font=("Arial Black", 16, "bold"))  # Font, size, and style
style.configure("Treeview", font=("Helvetica", 14))  # Font for table content

tree = ttk.Treeview(home, columns=('ID', 'Firstname', 'Lastname', 'MiddleName', 'Extension', 'Gender', 'Birthday', 'CivilStatus', 'Purok'), show='headings')
tree.heading('ID', text='ID')
tree.heading('Firstname', text='Firstname')
tree.heading('Lastname', text='Lastname')
tree.heading('MiddleName', text='Middle Name')
tree.heading('Extension', text='Extension')
tree.heading('Gender', text='Gender')
tree.heading('Birthday', text='Birthday')
tree.heading('CivilStatus', text='Civil Status')
tree.heading('Purok', text='Purok')
tree.column("ID", width=40, anchor="center")
tree.column("Firstname", width=100, stretch=True, anchor="center")
tree.column("Lastname", width=100, stretch=True, anchor="center")
tree.column("MiddleName", width=100, stretch=True, anchor="center")
tree.column("Extension", width=100, stretch=True, anchor="center")
tree.column("Gender", width=100, stretch=True, anchor="center")
tree.column("Birthday", width=100, stretch=True, anchor="center")
tree.column("CivilStatus", width=100, stretch=True, anchor="center")
tree.column("Purok", width=100, stretch=True, anchor="center")

# Bind Treeview selection to populate entries
tree.bind('<<TreeviewSelect>>', populate_entries)
tree.place_forget()
search_button.place_forget()
search_entry.place_forget()
view_member.place_forget()
update_data.place_forget()
delete_resident.place_forget()

add_screen = LabelFrame(home, padx=10, pady=10, background="White")

(Label(add_screen, text="HEAD OF FAMILY INFORMATION", font=("Arial", 18), anchor="center", justify="center", bg="white")
    .place(x=0, y=0, width="825", height="30"))
(Label(add_screen, text="Firstname: ", font=("Arial", 14), justify="left", anchor="nw", bg="white")
    .place(x=0, y=40, width="130", height="30"))
(Label(add_screen, text="Lastname: ", font=("Arial", 14), justify="left", anchor="nw", bg="white")
    .place(x=445, y=40, width="130", height="30"))
(Label(add_screen, text="Middle Name: ", font=("Arial", 14), justify="left", anchor="nw", bg="white")
    .place(x=0, y=80, width="130", height="30"))
(Label(add_screen, text="Extension: ", font=("Arial", 14), justify="left", anchor="nw", bg="white")
    .place(x=390, y=80, width="120", height="30"))
(Label(add_screen, text="Gender: ", font=("Arial", 14), justify="left", anchor="nw", bg="white")
    .place(x=570, y=80, width="80", height="30"))
(Label(add_screen, text="Birthday: ", font=("Arial", 14), justify="left", anchor="nw", bg="white")
    .place(x=0, y=120, width="130", height="30"))
(Label(add_screen, text="Civil Status: ", font=("Arial", 14), justify="left", anchor="nw", bg="white")
    .place(x=290, y=120, width="100", height="30"))
(Label(add_screen, text="Purok: ", font=("Arial", 14), justify="left", anchor="nw", bg="white")
    .place(x=555, y=120, width="100", height="30"))

firstname = tk.Entry(add_screen, font=("Arial", 14), bd=2, justify="left")
firstname.place(x=130, y=40, width=250, height=30)
lastname = tk.Entry(add_screen, font=("Arial", 14), bd=2, justify="left")
lastname.place(x=575, y=40, width=250, height=30)
middle_name = tk.Entry(add_screen, font=("Arial", 14), bd=2, justify="left")
middle_name.place(x=130, y=80, width=250, height=30)
extension = tk.Entry(add_screen, font=("Arial", 14), bd=2, justify="left")
extension.place(x=490, y=80, width=70, height=30)
birthday = tk.Entry(add_screen, font=("Arial", 14), bd=2, justify="left")
birthday.place(x=130, y=120, width=150, height=30)

options = ["Male", "Female"]
gender = ttk.Combobox(add_screen, values=options, font=("Arial", 14))
gender.place(x=650, y=80, width=175, height=30)
options1 = ["Single", "Married", "Widowed", "Separated"]
civil_status = ttk.Combobox(add_screen, values=options1, font=("Arial", 14))
civil_status.place(x=395, y=120, width=150, height=30)
purok = ttk.Combobox(add_screen, font=("Arial", 14))
purok.place(x=645, y=120, width=180, height=30)

(Button(add_screen, text="Add New", font=("Arial Black", 14), bg="light green", anchor="center", justify="center", command=add_process)
 .place(x=645, y=160, width=180, height=40))
(Button(add_screen, text="Clear", font=("Arial Black", 14), bg="white", anchor="center", justify="center", command=clear_add_form)
 .place(x=455, y=160, width=180, height=40))

long_text = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."
message_widget = tk.Message(home, text=long_text, width=840, font=("Broadway", 16))

add_purok_box = tk.Tk()
add_purok_box.title("ADD NEW PUROK")
add_purok_box.geometry("340x100")
add_purok_box.resizable(False, False)
add_purok_box.grid_columnconfigure(0, weight=1)
(Label(add_purok_box, text="Purok Name: ", font=("Arial", 14))
    .place(x=10, y=10))
purok_entry = tk.Entry(add_purok_box, font=("Arial", 14))
purok_entry.place(x=130, y=10, width=200)
add_placeholder(purok_entry, "Enter Purok Name")

(Button(add_purok_box, text="Add New Purok", font=("Arial", 14), bg="light green", command=add_new_purok_process)
    .place(x=70, y=50, width=200))

# head_id = tk.Entry(home, font=("Arial", 14), bd=2, justify="left")
# head_id.place(x=700, y=50)

family_member_page = tk.Tk()
family_member_page.resizable(False, False)
family_member_page.configure(background="light blue")
family_member_page.title("BARANGAY INFORMATION SYSTEM (Family Members)")
family_member_page.geometry("950x620")
date_label_member = tk.Label(family_member_page, text="", font=("Arial", 18), bg="light blue")
date_label_member.place(x=10, y=10)
update_time()

head_label = tk.Label(family_member_page, text="Head of the Family: ", font=("Arial", 18), bg="light blue")
head_label.place(x=10, y=40)

(Button(family_member_page, text="Add Family Member", font=("Arial Black", 12), bg="light green", anchor="center", justify="center", command=add_member_open_form)
    .place(x=15, y=80, width=200))
(Button(family_member_page, text="Update Member", font=("Arial Black", 12), bg="blue", fg="white", anchor="center", justify="center", command=update_member_open_form)
    .place(x=225, y=80, width=200))
(Button(family_member_page, text="Delete Member", font=("Arial Black", 12), bg="dark red", fg="white", anchor="center", justify="center", command=delete_member_process)
    .place(x=435, y=80, width=200))
member_table = ttk.Treeview(family_member_page, columns=('id', 'Firstname', 'Lastname', 'MiddleName', 'Extension', 'Gender', 'Birthday', 'CivilStatus', 'Relationship'), show='headings')
member_table.heading('id', text='id')
member_table.heading('Firstname', text='Firstname')
member_table.heading('Lastname', text='Lastname')
member_table.heading('MiddleName', text='Middle Name')
member_table.heading('Extension', text='Extension')
member_table.heading('Gender', text='Gender')
member_table.heading('Birthday', text='Birthday')
member_table.heading('CivilStatus', text='Civil Status')
member_table.heading('Relationship', text='Relationship')
member_table.column("id", width=40, anchor="center")
member_table.column("Firstname", width=100, stretch=True, anchor="center")
member_table.column("Lastname", width=100, stretch=True, anchor="center")
member_table.column("MiddleName", width=100, stretch=True, anchor="center")
member_table.column("Extension", width=100, stretch=True, anchor="center")
member_table.column("Gender", width=100, stretch=True, anchor="center")
member_table.column("Birthday", width=100, stretch=True, anchor="center")
member_table.column("CivilStatus", width=100, stretch=True, anchor="center")
member_table.column("Relationship", width=100, stretch=True, anchor="center")
member_table.place(x=15, y=130, width=920, height=470)

add_member_form = LabelFrame(family_member_page, padx=10, pady=0, background="White")
add_member_form.place(x=15, y=130, width=920, height=470)

(Label(add_member_form, text="Add Family Members", font=("Arial Bold", 18), anchor="center", justify="center", bg="white")
    .place(x=40, y=10, width="825", height="40"))
(Label(add_member_form, text="Firstname: ", font=("Arial", 14), justify="left", anchor="nw", bg="white")
    .place(x=40, y=60, width="130", height="30"))
(Label(add_member_form, text="Lastname: ", font=("Arial", 14), justify="left", anchor="nw", bg="white")
    .place(x=40, y=100, width="130", height="30"))
(Label(add_member_form, text="Middle Name: ", font=("Arial", 14), justify="left", anchor="nw", bg="white")
    .place(x=40, y=140, width="130", height="30"))
(Label(add_member_form, text="Extension: ", font=("Arial", 14), justify="left", anchor="nw", bg="white")
    .place(x=40, y=180, width="130", height="30"))
(Label(add_member_form, text="Birthday: ", font=("Arial", 14), justify="left", anchor="nw", bg="white")
    .place(x=480, y=60, width="130", height="30"))
(Label(add_member_form, text="Gender: ", font=("Arial", 14), justify="left", anchor="nw", bg="white")
    .place(x=480, y=100, width="130", height="30"))
(Label(add_member_form, text="Civil Status: ", font=("Arial", 14), justify="left", anchor="nw", bg="white")
    .place(x=480, y=140, width="130", height="30"))
(Label(add_member_form, text="Relationship: ", font=("Arial", 14), justify="left", anchor="nw", bg="white")
    .place(x=480, y=180, width="130", height="30"))

firstname_mem = tk.Entry(add_member_form, font=("Arial", 14), bd=2, justify="left")
firstname_mem.place(x=170, y=60, width=250, height=30)
lastname_mem = tk.Entry(add_member_form, font=("Arial", 14), bd=2, justify="left")
lastname_mem.place(x=170, y=100, width=250, height=30)
middle_name_mem = tk.Entry(add_member_form, font=("Arial", 14), bd=2, justify="left")
middle_name_mem.place(x=170, y=140, width=250, height=30)
extension_mem = tk.Entry(add_member_form, font=("Arial", 14), bd=2, justify="left")
extension_mem.place(x=170, y=180, width=250, height=30)
birthday_mem = tk.Entry(add_member_form, font=("Arial", 14), bd=2, justify="left")
birthday_mem.place(x=600, y=60, width=250, height=30)
gender_mem = ttk.Combobox(add_member_form, values=["Male", "Female"], font=("Arial", 14))
gender_mem.place(x=600, y=100, width=250, height=30)
civil_status_mem = ttk.Combobox(add_member_form, values=["Single", "Married", "Widowed", "Separated"], font=("Arial", 14))
civil_status_mem.place(x=600, y=140, width=250, height=30)
relationship_mem = tk.Entry(add_member_form, font=("Arial", 14), bd=2, justify="left")
relationship_mem.place(x=600, y=180, width=250, height=30)

hidden_head_id = tk.Entry(add_member_form, font=("Arial", 14), bd=2, justify="left")
hidden_member_id = tk.Entry(add_member_form, font=("Arial", 14), bd=2, justify="left")
# hidden_member_id.place(x=600, y=10, width=250, height=30)
add_member_button = tk.Button(add_member_form, text="ADD MEMBER", font=("Arial", 14), bg="green", fg="white", command=lambda: add_update_member_process("add"))
add_member_button.place(x=650, y=230, width=200, height=30)
update_member_button = tk.Button(add_member_form, text="UPDATE MEMBER", font=("Arial", 14), bg="blue", fg="white", command=lambda: add_update_member_process("update"))
(Button(add_member_form, text="CLOSE", font=("Arial", 14), bg="red", fg="white", command=close_add_member_page)
    .place(x=440, y=230, width=200, height=30))

close_add_member_page()

# Initialize Database and Display Data
connect_db()

# login.withdraw()
add_purok_box.withdraw()
family_member_page.withdraw()
home.withdraw()
update_head_form.withdraw()


# mainScreen.place_forget()
# Run the Application

add_purok_box.protocol("WM_DELETE_WINDOW", on_closing_add_purok_box)
update_head_form.protocol("WM_DELETE_WINDOW", on_closing_update)
home.protocol("WM_DELETE_WINDOW", on_closing)
login.protocol("WM_DELETE_WINDOW", on_closing)
family_member_page.protocol("WM_DELETE_WINDOW", on_closing_members_page)
login.mainloop()