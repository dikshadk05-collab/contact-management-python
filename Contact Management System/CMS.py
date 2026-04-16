import mysql.connector
from tkinter import *
from tkinter import messagebox, ttk

# --- Database Connection (Kept same) ---
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Diksha@2305",   
        database="contact_db"
    )

# --- Enhanced Functions (Kept same) ---

def add_contact():
    name, phone, email = ent_name.get(), ent_phone.get(), ent_email.get()
    if not name or not phone:
        messagebox.showerror("Error", "Name and Phone are required!")
        return
    con = get_connection(); cur = con.cursor()
    cur.execute("INSERT INTO contacts (name, phone, email) VALUES (%s, %s, %s)", (name, phone, email))
    con.commit(); con.close()
    clear_entries(); view_contacts()

def delete_contact():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "Please select a contact to delete")
        return
    
    confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this contact?")
    if confirm:
        values = tree.item(selected_item)['values']
        con = get_connection(); cur = con.cursor()
        cur.execute("DELETE FROM contacts WHERE id=%s", (values[0],))
        con.commit(); con.close()
        view_contacts()

def update_contact():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "Please select a contact to update")
        return
    
    values = tree.item(selected_item)['values']
    name, phone, email = ent_name.get(), ent_phone.get(), ent_email.get()
    
    if not name or not phone:
        messagebox.showerror("Error", "Fields cannot be empty for update!")
        return

    con = get_connection(); cur = con.cursor()
    cur.execute("UPDATE contacts SET name=%s, phone=%s, email=%s WHERE id=%s", 
                (name, phone, email, values[0]))
    con.commit(); con.close()
    clear_entries(); view_contacts()

def search_contacts():
    query = ent_search.get()
    for item in tree.get_children(): tree.delete(item)
    con = get_connection(); cur = con.cursor()
    # Searches by ID or Name using LIKE for partial matches
    cur.execute("SELECT * FROM contacts WHERE id LIKE %s OR name LIKE %s", 
                ('%'+query+'%', '%'+query+'%'))
    for row in cur.fetchall():
        tree.insert("", END, values=row)
    con.close()

def view_contacts():
    ent_search.delete(0, END)
    for item in tree.get_children(): tree.delete(item)
    con = get_connection(); cur = con.cursor()
    cur.execute("SELECT * FROM contacts ORDER BY id ASC")
    for row in cur.fetchall():
        tree.insert("", END, values=row)
    con.close()

def on_tree_select(event):
    # Auto-fills the entry boxes when a row is clicked
    selected_item = tree.selection()
    if selected_item:
        values = tree.item(selected_item)['values']
        clear_entries()
        ent_name.insert(0, values[1])
        ent_phone.insert(0, values[2])
        ent_email.insert(0, values[3])

def clear_entries():
    ent_name.delete(0, END); ent_phone.delete(0, END); ent_email.delete(0, END)

# --- UI Setup ---
root = Tk()
root.title("Excel Style Contact Manager")
root.geometry("950x600")
root.configure(bg="white")

style = ttk.Style()
# We must use 'clam' or 'alt' as they support advanced layout changes
style.theme_use("clam")

# --- THE MAGIC FOR THE GRID LINES ---
# We configure the default Treeview layout to include cell borders.
# This forces the internal separator lines (columns) and row lines to be visible.
style.configure("Treeview",
                borderwidth=1,
                relief="solid", # This creates the main outer border
                rowheight=30) # Height makes cells look more spreadsheet-like

# Map a background to make selected rows stand out
style.map("Treeview", background=[('selected', '#3498db')])

# Standard Headings
style.configure("Treeview.Heading", 
                background="#5C4033", # Dark brown from image
                foreground="white", 
                font=("Arial", 11, "bold"))

Label(root, text="CONTACT DETAILS", font=("Arial", 24, "bold"), fg="#5C4033", bg="white").pack(pady=10)

# Search Bar Frame
search_frame = Frame(root, bg="white")
search_frame.pack(pady=5)
Label(search_frame, text="Search (ID/Name):", bg="white", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5)
ent_search = Entry(search_frame, bd=2, relief="groove", width=30)
ent_search.grid(row=0, column=1, padx=5)
Button(search_frame, text="Search", command=search_contacts, bg="#34495e", fg="white").grid(row=0, column=2, padx=5)

# Input Fields
input_frame = Frame(root, bg="white")
input_frame.pack(pady=10)

Label(input_frame, text="Name:", bg="white").grid(row=0, column=0, padx=5)
ent_name = Entry(input_frame, bd=2, relief="groove"); ent_name.grid(row=0, column=1, padx=10)

Label(input_frame, text="Phone:", bg="white").grid(row=0, column=2, padx=5)
ent_phone = Entry(input_frame, bd=2, relief="groove"); ent_phone.grid(row=0, column=3, padx=10)

Label(input_frame, text="Email:", bg="white").grid(row=0, column=4, padx=5)
ent_email = Entry(input_frame, bd=2, relief="groove"); ent_email.grid(row=0, column=5, padx=10)

# --- THE ACTUAL TREEVIEW (THE GRID TABLE) ---
# Wrapping in a frame for a neat border
table_frame = Frame(root, bd=1, relief="solid")
table_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)

# **show="headings"** is crucial to avoid the empty first column.
# The `relief="solid"` and `borderwidth=1` here apply to the table container,
# but the grid lines inside are controlled by the `style.configure("Treeview")` block above.
tree = ttk.Treeview(table_frame, columns=("ID", "Name", "Phone", "Email"), show="headings")

# ... Define Headings and Columns ... (Kept same)
tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Phone", text="Phone")
tree.heading("Email", text="Work Email")

tree.column("ID", width=50, anchor=CENTER)
tree.column("Name", width=200, anchor=W)
tree.column("Phone", width=150, anchor=CENTER)
tree.column("Email", width=250, anchor=W)

tree.pack(side=LEFT, fill=BOTH, expand=True)
tree.bind("<<TreeviewSelect>>", on_tree_select) 

scrollbar = ttk.Scrollbar(table_frame, orient=VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side=RIGHT, fill=Y)

# Action Buttons
btn_frame = Frame(root, bg="white")
btn_frame.pack(pady=20)
Button(btn_frame, text="Add Contact", command=add_contact, bg="#27ae60", fg="white", width=12).pack(side=LEFT, padx=5)
Button(btn_frame, text="Update", command=update_contact, bg="#f39c12", fg="white", width=12).pack(side=LEFT, padx=5)
Button(btn_frame, text="Delete", command=delete_contact, bg="#c0392b", fg="white", width=12).pack(side=LEFT, padx=5)
Button(btn_frame, text="Refresh All", command=view_contacts, bg="#95a5a6", fg="white", width=12).pack(side=LEFT, padx=5)

view_contacts()
root.mainloop()