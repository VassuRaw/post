from tkinter import *
from tkinter import ttk
from tkcalendar import *
import sqlite3
from datetime import datetime, date
from autocomplete import *

conn = sqlite3.connect('database.db')
db = conn.cursor()
try:
    db.execute("CREATE TABLE descriptions (id INTEGER NOT NULL UNIQUE, name TEXT NOT NULL, PRIMARY KEY(id AUTOINCREMENT))")

    db.execute("CREATE TABLE offices (id INTEGER NOT NULL UNIQUE, name TEXT NOT NULL, ddo TEXT NOT NULL, gst TEXT NOT NULL,\
                PRIMARY KEY(id AUTOINCREMENT))")

    db.execute("CREATE TABLE sanctions (id INTEGER NOT NULL UNIQUE, sanction_date DATE NOT NULL, amount NUMERIC NOT NULL,\
                PRIMARY KEY(id AUTOINCREMENT))")

    db.execute("CREATE TABLE vendors (id INTEGER NOT NULL UNIQUE, name TEXT NOT NULL, address TEXT NOT NULL, gst TEXT,\
                PRIMARY KEY(id AUTOINCREMENT))")

    db.execute("CREATE TABLE data (id INTEGER NOT NULL UNIQUE,\
               bill_no	INTEGER NOT NULL,\
               amount	NUMERIC NOT NULL,\
               office_name	TEXT NOT NULL,\
               vendor_name	TEXT NOT NULL,\
               description	TEXT NOT NULL,\
               account_head	TEXT NOT NULL,\
               bill_date	DATE NOT NULL,\
               received_date	DATE NOT NULL,\
               sanction_id	INTEGER,\
               PRIMARY KEY(id AUTOINCREMENT),\
               FOREIGN KEY(sanction_id) REFERENCES sanctions(id))")
    
    print("Database created successfully")
except:
    print("Database already available")

def main():
    print("Select options:")
    print("1. Data Entry ")
    print("2. Sanction Bills")
    print("3. Reports")
    option = int(input())
    if option == 1:
        data()
    elif option == 2:
        sanction()
    elif option == 3:
        reports()
    else:
        print("Wrong option")

def data():
    temp = list(db.execute("SELECT name FROM offices"))
    offices = []
    for row in temp:
        offices.append(row[0])

    temp = list(db.execute("SELECT name FROM vendors"))
    vendors = []
    for row in temp:
        vendors.append(row[0])
        
    root = Tk(className='AutocompleteCombobox')

    def handle_focus(event):
        if event.widget == root:
            bill_no_field.focus_set()

    def insert():
        db.execute("INSERT INTO data(bill_no, amount, account_head, description, office_name, vendor_name, bill_date, received_date)\
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                   (bill_no_field.get(), amount_field.get(), account_head_field.get(), description_field.get(), office_name_field.get(),
                    vendor_name_field.get(), bill_date_field.get(), received_date_field.get()))
        conn.commit()
        
            
    root.configure(background='light green')
    root.title('Data Entry')
    root.geometry('500x300')

    heading = Label(root, text="Data Entry", bg='light green')
    bill_no = Label(root, text="Bill Number", bg='light green')
    amount = Label(root, text="Amount", bg='light green')
    account_head = Label(root, text="Account Head", bg='light green')
    description = Label(root, text="Description", bg='light green')
    office_name = Label(root, text="Office Name", bg='light green')
    vendor_name = Label(root, text="Vendor Name", bg='light green')
    bill_date = Label(root, text="Bill Date", bg='light green')
    received_date = Label(root, text="Received Date", bg='light green')

    heading.grid(row=1, column=1)
    bill_no.grid(row=3, column=0)
    amount.grid(row=5, column=0)
    account_head.grid(row=7, column=0)
    description.grid(row=8, column=0)
    office_name.grid(row=9, column=0)
    vendor_name.grid(row=11, column=0)
    bill_date.grid(row=13, column=0)
    received_date.grid(row=15, column=0)

    bill_no_field = ttk.Entry(root)
    
    amount_field = ttk.Entry(root)
    
    account_head_field = AutocompleteCombobox(root)
    account_head_field.set_completion_list(['OE', 'MW', 'AMC NP'])

    description_field = ttk.Entry(root)
    
    office_name_field = AutocompleteCombobox(root)
    office_name_field.set_completion_list(offices)
    
    vendor_name_field = AutocompleteCombobox(root)
    vendor_name_field.set_completion_list(vendors)
    
    bill_date_field = DateEntry(root, date_pattern='dd-mm-yyyy')
    received_date_field = DateEntry(root, date_pattern='dd-mm-yyyy')

    bill_no_field.grid(row=3, column=1, ipadx="100")
    amount_field.grid(row=5, column=1, ipadx="100")
    account_head_field.grid(row=7, column=1, ipadx="91")
    description_field.grid(row=8, column=1, ipadx="100")
    office_name_field.grid(row=9, column=1, ipadx="91")
    vendor_name_field.grid(row=11, column=1, ipadx="91")
    bill_date_field.grid(row=13, column=1, ipadx="115")
    received_date_field.grid(row=15, column=1, ipadx="115")

    submit = Button(root, text="Submit", fg="Black", bg="Red", command=insert) 
    submit.grid(row=16, column=1) 

    root.lift()
    root.attributes('-topmost', True)
    root.focus_force()

    root.bind('<FocusIn>', handle_focus)

    hwnd = root.winfo_id()
    
    root.mainloop()

def sanction():
    temp = list(db.execute("SELECT * FROM data WHERE sanction_id is NULL"))
    print(temp)

    offices = {"All"}
    head = {"All"}
    for row in temp:
        offices.add(row[3])
        head.add(row[6])
    
    print(offices)
    print(head)
    
    def post():
        pass

    root = Tk()
    
    var_office = StringVar(root)
    var_office.set("All")
    var_head = StringVar(root)
    var_head.set("All")
    OptionMenu(root, var_office, *offices).grid(row=1, column=1)
    OptionMenu(root, var_head, *head).grid(row=1, column=2)

    for i in range(len(temp)):
        for j in range(len(temp[0])-1):
            if var_office.get() == temp[i][3]:
                if j==0:
                    Checkbutton(root,text=temp[i][j], height=2, variable=temp[i][j]).grid(row=i+2, column=j)
                else:
                    data = Listbox(root, height=2)
                    data.grid(row=i+2, column= j)
                    data.insert(END, temp[i][j])
    Button(root, text="Submit", command=post).grid(row=i+3)
    root.mainloop()

def reports():
    print("TO DO")

main()
