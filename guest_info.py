from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3

class Info:
    def __init__(self, root, conn):
        self.root = root
        self.root.title("GUEST INFO")
        self.root.geometry("1295x550+230+220")
        self.conn = conn
        self.conn = sqlite3.connect("guest_info.db")
        self.create_table()  # Call method to create table if not exists

        
        # Title Section
        lb_title = Label(self.root, text="GUEST DETAILS", font=("times new roman", 10, "bold", "italic"), bg="black", fg="gold", bd=4, relief=RIDGE)
        lb_title.pack(fill=X)
        # Label Frame
        labelframeleft = LabelFrame(self.root, bd=2, relief=RIDGE, text="Details", font=("times new roman", 12, "bold", "italic"), padx=20, pady=20)
        labelframeleft.pack(fill="both", expand="yes", padx=20, pady=20)

        # Labels and Entry Widgets
        labels = [
            "Guest Ref:", "Name:", "Unit/FMN:", "Contact:", "Reference:"
        ]
        self.entry_widgets = []

        for i, label_text in enumerate(labels):
            lbl = Label(labelframeleft, text=label_text, font=("times new roman", 12), padx=5, pady=5)
            lbl.grid(row=i, column=0, sticky="w")

            entry = Entry(labelframeleft, font=("times new roman", 12), bd=2, relief=GROOVE)
            entry.grid(row=i, column=1, padx=10, pady=3, sticky="w")
            self.entry_widgets.append(entry)

        # Buttons
        btn_frame = Frame(labelframeleft, bd=5, relief=RIDGE)
        btn_frame.grid(row=15, columnspan=2, padx=40, pady=50)

        btn_add = Button(btn_frame, text="Add", font=("times new roman", 12), command=self.add_guest, bd=3, relief=RAISED, width=10)
        btn_add.grid(row=0, column=0, padx=20, pady=25, sticky="nsew")

        btn_update = Button(btn_frame, text="Update", font=("times new roman", 12), command=self.update_guest, bd=3, relief=RAISED, width=10)
        btn_update.grid(row=0, column=1, padx=20, pady=25, sticky="nsew")

        btn_delete = Button(btn_frame, text="Delete", font=("times new roman", 12), command=self.delete_guest, bd=3, relief=RAISED, width=10)
        btn_delete.grid(row=1, column=0, padx=20, pady=25, sticky="nsew")

        btn_reset = Button(btn_frame, text="Reset", font=("times new roman", 12), command=self.reset_fields, bd=3, relief=RAISED, width=10)
        btn_reset.grid(row=1, column=1, padx=20, pady=25, sticky="nsew")



        # Table Frame
        Tableframe = LabelFrame(self.root, bd=2, relief=RIDGE, text="View Details And Search", font=("times new roman", 12, "bold", "italic"), padx=20, pady=20)
        Tableframe.place(x=435, y=50, width=830, height=490)

        lbsearch = Label(Tableframe, text="Search By: ", font=("times new roman", 12),bg="red",fg="white")
        lbsearch.grid(row=0, column=0, sticky=W,padx=2)

        self.combo_search=ttk.Combobox(Tableframe,font=("arial",12,"bold"),width=24,state="readonly")
        self.combo_search["value"]=("Guest Ref","Name")
        self.combo_search.current(0)
        self.combo_search.grid(row=0,column=1,padx=2)

        self.entrySearch = Entry(Tableframe, font=("times new roman", 12), width=24)
        self.entrySearch.grid(row=0, column=2,padx=2)

        btn_search = Button(Tableframe, text="Search",command=self.search_guest, font=("times new roman", 12), bg="black", fg="gold", bd=3, relief=RAISED, width=10)
        btn_search.grid(row=0, column=3, padx=1)

        btn_all = Button(Tableframe, text="Show All", command=self.show_all_guests, font=("times new roman", 12), bg="black", fg="gold", bd=3, relief=RIDGE, width=10)
        btn_all.grid(row=0, column=4, padx=1)


        # Data table
        details_table=Frame(Tableframe,bd=3,relief=RIDGE)
        details_table.place(x=0,y=50,width=800,height=350)

        scroll_x=ttk.Scrollbar(details_table,orient=HORIZONTAL)
        scroll_y=ttk.Scrollbar(details_table,orient=VERTICAL)

        self.Guest_Details_Table=ttk.Treeview(details_table,columns=("Guest Ref", "Name", "Unit/FMN", "Contact", "Reference"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)

         # Set anchor to center for all columns
        for column in ("Guest Ref", "Name", "Unit/FMN", "Contact", "Reference"):
            self.Guest_Details_Table.heading(column, text=column, anchor="center")
            self.Guest_Details_Table.column(column, anchor="center")
        
        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)

        scroll_x.config(command=self.Guest_Details_Table.xview)
        scroll_y.config(command=self.Guest_Details_Table.yview)

        self.Guest_Details_Table.heading("Guest Ref",text="Reference Number")
        self.Guest_Details_Table.heading("Name",text="Guest Name")
        self.Guest_Details_Table.heading("Unit/FMN",text="Unit")
        self.Guest_Details_Table.heading("Contact",text="Contact")
        self.Guest_Details_Table.heading("Reference",text="Reference")

        self.Guest_Details_Table["show"]="headings"

        self.Guest_Details_Table.column("Guest Ref",width=100)
        self.Guest_Details_Table.column("Name",width=100)
        self.Guest_Details_Table.column("Unit/FMN",width=100)
        self.Guest_Details_Table.column("Contact",width=100)
        self.Guest_Details_Table.column("Reference",width=100)
        self.Guest_Details_Table.pack(fill=BOTH,expand=1)

    def create_table(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS guest_info (
                    guest_ref TEXT PRIMARY KEY,
                    name TEXT,
                    unit_fmn TEXT,
                    contact TEXT,
                    reference TEXT
                )
            """)
            self.conn.commit()
        except Exception as e:
            print(f"An error occurred while creating the table: {str(e)}")

    def add_guest(self):
        guest_ref = self.entry_widgets[0].get()
        name = self.entry_widgets[1].get()
        unit_fmn = self.entry_widgets[2].get()
        contact = self.entry_widgets[3].get()
        reference = self.entry_widgets[4].get()

        if guest_ref and name and unit_fmn and contact:
            try:
                cursor = self.conn.cursor()
                cursor.execute("INSERT INTO guest_info (guest_ref, name, unit_fmn, contact, reference) VALUES (?, ?, ?, ?, ?)",
                            (guest_ref, name, unit_fmn, contact, reference))
                self.conn.commit()
                messagebox.showinfo("Success", "Guest information added successfully")
                self.reset_fields()  # Clear entry fields after successful addition
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
        else:
            messagebox.showerror("Error", "Please fill in all required fields")

    def update_guest(self):
        guest_ref = self.entry_widgets[0].get()
        name = self.entry_widgets[1].get()
        unit_fmn = self.entry_widgets[2].get()
        contact = self.entry_widgets[3].get()
        reference = self.entry_widgets[4].get()

        if guest_ref:
            try:
                cursor = self.conn.cursor()
                # Check if the guest record exists
                cursor.execute("SELECT * FROM guest_info WHERE guest_ref = ?", (guest_ref,))
                existing_record = cursor.fetchone()
                if existing_record:
                    # Construct the SET clause of the SQL query dynamically
                    set_clause = []
                    params = []
                    if name:
                        set_clause.append("name=?")
                        params.append(name)
                    if unit_fmn:
                        set_clause.append("unit_fmn=?")
                        params.append(unit_fmn)
                    if contact:
                        set_clause.append("contact=?")
                        params.append(contact)
                    if reference:
                        set_clause.append("reference=?")
                        params.append(reference)

                    # If at least one field has been provided for updating
                    if set_clause:
                        set_clause_str = ", ".join(set_clause)
                        params.append(guest_ref)  # Add the guest_ref for WHERE clause
                        cursor.execute(f"UPDATE guest_info SET {set_clause_str} WHERE guest_ref=?", tuple(params))
                        self.conn.commit()
                        messagebox.showinfo("Success", "Guest information updated successfully")
                    else:
                        messagebox.showerror("Error", "No fields provided for updating")
                else:
                    messagebox.showerror("Error", "Guest record not found")

            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
        else:
            messagebox.showerror("Error", "Please enter a guest reference")




    def delete_guest(self):
        guest_ref = self.entry_widgets[0].get()
        
        if guest_ref:
            try:
                cursor = self.conn.cursor()
                cursor.execute("SELECT * FROM guest_info WHERE guest_ref = ?", (guest_ref,))
                record = cursor.fetchone()

                if record:
                    cursor.execute("DELETE FROM guest_info WHERE guest_ref = ?", (guest_ref,))
                    self.conn.commit()
                    messagebox.showinfo("Success", "Guest information deleted successfully")
                else:
                    messagebox.showerror("Error", "Guest record not found")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
        else:
            messagebox.showerror("Error", "Please enter a guest reference to delete")

    def reset_fields(self):
        for entry in self.entry_widgets:
            entry.delete(0, END)

    def search_guest(self):
        search_by = self.combo_search.get()  # Assuming combo_search is defined globally
        search_text = self.entrySearch.get()  # Assuming entrySearch is defined globally

        try:
            cursor = self.conn.cursor()
            if search_by == "Guest Ref":
                cursor.execute("SELECT * FROM guest_info WHERE guest_ref=?", (search_text,))
            elif search_by == "Name":
                cursor.execute("SELECT * FROM guest_info WHERE name=?", (search_text,))
            else:
                messagebox.showerror("Error", "Invalid search criteria")

            rows = cursor.fetchall()

            # Clear existing table contents
            for row in self.Guest_Details_Table.get_children():
                self.Guest_Details_Table.delete(row)

            # Insert matching records into the data table
            for row in rows:
                self.Guest_Details_Table.insert("", END, values=row)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    def show_all_guests(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM guest_info")
            rows = cursor.fetchall()

            # Clear existing table contents
            for row in self.Guest_Details_Table.get_children():
                self.Guest_Details_Table.delete(row)

            # Insert all records into the data table
            for row in rows:
                self.Guest_Details_Table.insert("", END, values=row)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    try:
        conn = sqlite3.connect("guest_info.db")
        root = Tk()
        obj = Info(root, conn)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
    finally:
        conn.close()


