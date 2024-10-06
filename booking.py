from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from datetime import datetime 
from dateutil import parser
class Booking:
    def __init__(self, root, conn):
        self.root = root
        self.conn = conn  # Store the database connection
        self.root.title("BOOKING")
        self.root.geometry("1295x550+230+220")
        
        self.create_booking_table()
        self.selected_block = StringVar()  # Add selected_block attribute
        # self.advance_payment_date_var = StringVar()  # Corrected attribute name
        self.selected_room = StringVar()  # Add selected_room attribute
        self.booking_date = StringVar()
        self.departure_date=StringVar()
        # Title Section
        lb_title = Label(self.root, text="GUEST BOOKING", font=("times new roman", 10, "bold", "italic"), bg="black", fg="gold", bd=4, relief=RIDGE)
        lb_title.pack(fill=X)

        # Label Frame
        labelframeleft = LabelFrame(self.root, bd=2, relief=RIDGE, text="Booking", font=("times new roman", 12, "bold", "italic"), padx=20, pady=20)
        labelframeleft.place(x=5, y=50, width=430, height=540)  # Increased height to accommodate the additional label and button

        # Labels and Entry Widgets
        labels = [
            "Guest Ref:", "Block Name:", "Room Number:", "Booking Date:", "Departure Date:", 
        ]
        self.entry_widgets = []  # Generic entry widgets list for Guest Ref, Room Number, etc.

        for i, label_text in enumerate(labels):
            lbl = Label(labelframeleft, text=label_text, font=("times new roman", 12), padx=5, pady=5)
            lbl.grid(row=i, column=0, sticky="w")

            if label_text == "Guest Ref:":
                guest_ref_entry = Entry(labelframeleft, font=("times new roman", 12), bd=2, relief=GROOVE)
                guest_ref_entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")
                self.entry_widgets.append(guest_ref_entry)
            
            elif label_text == "Block Name:":
                block_options = ["Old", "Carippa", "Manekshaw"]
                block_dropdown = OptionMenu(labelframeleft, self.selected_block, *block_options, command=self.update_room_numbers)
                block_dropdown.config(width=15)
                block_dropdown.grid(row=i, column=1, padx=10, pady=5, sticky="w")

            elif label_text == "Room Number:":
                self.room_menu = OptionMenu(labelframeleft, self.selected_room, "", command=self.update_room_numbers)
                self.room_menu.config(width=15)
                self.room_menu.grid(row=i, column=1, padx=10, pady=5, sticky="w")
                self.entry_widgets.append(self.room_menu)
            
            elif label_text == "Booking Date:":
                # Special handling for booking date
                self.booking_date_var = StringVar()  # StringVar to hold the booking date
                booking_date_entry = Entry(labelframeleft, textvariable=self.booking_date_var, font=("times new roman", 12), bd=2, relief=GROOVE)
                booking_date_entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")
                self.entry_widgets.append(booking_date_entry)  # You can add this to the general list if needed
            
            elif label_text == "Departure Date:":
                # Special handling for departure date
                self.departure_date_var = StringVar()  # StringVar to hold the departure date
                departure_date_entry = Entry(labelframeleft, textvariable=self.departure_date_var, font=("times new roman", 12), bd=2, relief=GROOVE)
                departure_date_entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")
                self.entry_widgets.append(departure_date_entry)  # You can add this to the general list if needed




            # elif label_text == "Advance Payment:":
            #     payment_options = ["Yes", "No"]
            #     payment_dropdown = OptionMenu(labelframeleft, self.advance_payment_date_var, *payment_options, command=self.toggle_advance_fields)
            #     payment_dropdown.config(width=10)
            #     payment_dropdown.grid(row=i, column=1, padx=10, pady=5, sticky="w")
        self.advance_payment_fields = [self.booking_date, self.departure_date]  # Update the list here

        # Advance Payment Fields (Hidden by Default)
        self.advance_payment_fields = []
        # advance_labels = ["Advance Payment Date:", "Advance Payment Receipt No.:", "Advance Amount:"]
        # for i, label_text in enumerate(advance_labels):
        #     lbl = Label(labelframeleft, text=label_text, font=("times new roman", 12), padx=5, pady=5)
        #     lbl.grid(row=len(labels) + i, column=0, sticky="w")
        #     entry = Entry(labelframeleft, font=("times new roman", 12), bd=2, relief=GROOVE, state="disabled")
        #     entry.grid(row=len(labels) + i, column=1, padx=10, pady=5, sticky="w")
        #     self.entry_widgets.append(entry)  # Append the entry widget to the list
        #     self.advance_payment_fields.append(entry)

        # Assign Button Frame
        assign_frame = Frame(labelframeleft, bd=2, relief=RIDGE)
        assign_frame.grid(row=len(labels)+2, columnspan=2, padx=0, pady=10)  # Increased pady to provide spacing

        btn_assign = Button(assign_frame, text="Assign", font=("times new roman", 12), bg="black", fg="gold", bd=3, relief=RAISED, width=10, command=self.assign_room)
        btn_assign.grid(row=0, column=0, padx=5, pady=5)

        # Table Frame
        table_frame = LabelFrame(self.root, bd=2, relief=RIDGE, text="View Details And Search", font=("times new roman", 12, "bold", "italic"), padx=20, pady=20)
        table_frame.place(x=435, y=50, width=830, height=490)

        lbsearch = Label(table_frame, text="Search By: ", font=("times new roman", 12),bg="red",fg="white")
        lbsearch.grid(row=0, column=0, sticky=W,padx=2)

        self.combo_search=ttk.Combobox(table_frame,font=("arial",12,"bold"),width=24,state="readonly")
        self.combo_search["value"]=("Guest Ref","Block Name","Room Number")
        self.combo_search.current(0)
        self.combo_search.grid(row=0,column=1,padx=2)

        self.entrySearch = Entry(table_frame, font=("times new roman", 12), width=24)
        self.entrySearch.grid(row=0, column=2,padx=2)

        btn_search = Button(table_frame, text="Search",command=self.search_guest, font=("times new roman", 12), bg="black", fg="gold", bd=3, relief=RAISED, width=10)
        btn_search.grid(row=0, column=3, padx=1)

        btn_all = Button(table_frame, text="Show All", command=self.show_all_guests, font=("times new roman", 12), bg="black", fg="gold", bd=3, relief=RIDGE, width=10)
        btn_all.grid(row=0, column=4, padx=1)


        # Data table
        details_table=Frame(table_frame,bd=3,relief=RIDGE)
        details_table.place(x=0,y=50,width=800,height=350)

        scroll_x=ttk.Scrollbar(details_table,orient=HORIZONTAL)
        scroll_y=ttk.Scrollbar(details_table,orient=VERTICAL)

        self.Guest_Details_Table=ttk.Treeview(details_table,columns=("Guest Ref", "Name", "Block", "Room Number", "Booking Date", "Departure Date"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)

        # Set anchor to center for all columns
        for column in ("Guest Ref", "Name", "Block", "Room Number", "Booking Date", "Departure Date"):
            self.Guest_Details_Table.heading(column, text=column, anchor="center")
            self.Guest_Details_Table.column(column, anchor="center")
        
        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)

        scroll_x.config(command=self.Guest_Details_Table.xview)
        scroll_y.config(command=self.Guest_Details_Table.yview)

        self.Guest_Details_Table["show"]="headings"

        self.Guest_Details_Table.column("Guest Ref",width=100)
        self.Guest_Details_Table.column("Name",width=100)
        self.Guest_Details_Table.column("Block",width=100)
        self.Guest_Details_Table.column("Room Number",width=100)
        self.Guest_Details_Table.column("Booking Date",width=100)
        self.Guest_Details_Table.column("Departure Date",width=100)
        self.Guest_Details_Table.pack(fill=BOTH,expand=1)

    # def toggle_advance_fields(self, selected_option):
    #     if selected_option == "Yes":
    #         for entry in self.advance_payment_fields:
    #             entry.config(state="normal")
    #     else:
    #         for entry in self.advance_payment_fields:
    #             entry.delete(0, END)  # Clear the contents of the entry
    #             entry.config(state="disabled")

    def update_room_numbers(self, selected_block):
        if selected_block == "Old":
            available_rooms = [41, 42, 43, 44, 45, 46, 48]
        elif selected_block == "Carippa":
            available_rooms = list(range(1, 8)) + list(range(11, 18)) + list(range(21, 28)) + list(range(31, 38))
        elif selected_block == "Manekshaw":
            available_rooms = list(range(1, 21))
        else:
            available_rooms = []

        self.selected_room.set("")  # Clear the selection
        self.room_menu['menu'].delete(0, 'end')
        for room_number in available_rooms:
            self.room_menu['menu'].add_command(label=room_number, command=lambda value=room_number: self.selected_room.set(value))

    def assign_room(self):
        guest_ref = self.entry_widgets[0].get()
        block_name = self.selected_block.get()
        room_number = self.selected_room.get()

        # Use the StringVar's .get() to retrieve date values
        booking_date_str = self.booking_date_var.get().strip()
        departure_date_str = self.departure_date_var.get().strip()

        print("Booking Date:", booking_date_str)
        print("Departure Date:", departure_date_str)

        if not booking_date_str or not departure_date_str:
            messagebox.showerror("Error", "Please fill in the Booking Date and Departure Date.")
            return

        expected_format = '%Y-%m-%d'  # Specify the expected date format
        try:
            # Attempt to parse date strings with the expected format
            booking_date = datetime.strptime(booking_date_str, expected_format)
            departure_date = datetime.strptime(departure_date_str, expected_format)
        except ValueError:
            messagebox.showerror("Error", f"Invalid date format. Please use {expected_format}.")
            return

        if booking_date >= departure_date:
            messagebox.showerror("Error", "Booking Date should be before the Departure Date.")
            return

        # Check for overlapping bookings
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT * FROM booking
            WHERE room_number = ?
            AND (
                (? >= booking_date AND ? < departure_date)
                OR (? >= booking_date AND ? < departure_date)
                OR (booking_date >= ? AND booking_date < ?)
            )
            """,
            (room_number, booking_date, booking_date, departure_date, departure_date, booking_date, departure_date)
        )

        existing_overlapping_booking = cursor.fetchone()

        if existing_overlapping_booking:
            messagebox.showerror("Error", "The selected room is already booked for the specified period.")
            return

        # Insert the booking
        try:
            cursor.execute(
                "INSERT INTO booking (guest_ref, block_name, room_number, booking_date, departure_date) VALUES (?, ?, ?, ?, ?)",
                (guest_ref, block_name, room_number, booking_date.isoformat(), departure_date.isoformat())
            )
            self.conn.commit()
            messagebox.showinfo("Success", "Room assigned successfully")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")




    def search_guest(self):
        search_by = self.combo_search.get()
        search_text = self.entrySearch.get()

        try:
            cursor = self.conn.cursor()
            if search_by == "Guest Ref":
                cursor.execute("SELECT b.guest_ref, g.name, b.block_name, b.room_number, b.booking_date, b.departure_date FROM booking b INNER JOIN guest_info g ON b.guest_ref = g.guest_ref WHERE b.guest_ref=?", (search_text,))
            elif search_by == "Block Name":
                cursor.execute("SELECT b.guest_ref, g.name, b.block_name, b.room_number, b.booking_date, b.departure_date FROM booking b INNER JOIN guest_info g ON b.guest_ref = g.guest_ref WHERE b.block_name=?", (search_text,))
            elif search_by == "Room Number":
                cursor.execute("SELECT b.guest_ref, g.name, b.block_name, b.room_number, b.booking_date, b.departure_date FROM booking b INNER JOIN guest_info g ON b.guest_ref = g.guest_ref WHERE b.room_number=?", (search_text,))
            else:
                messagebox.showerror("Error", "Invalid search criteria")

            rows = cursor.fetchall()

            # Clear existing table contents
            for row in self.Guest_Details_Table.get_children():
                self.Guest_Details_Table.delete(row)

            # Insert matching records into the data table
            for row in rows:
                # Convert dates to proper format before inserting
                booking_date = row[4] if row[4] else ""
                departure_date = row[5] if row[5] else ""
                self.Guest_Details_Table.insert("", END, values=(row[0], row[1], row[2], row[3], booking_date, departure_date))

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def show_all_guests(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT b.guest_ref, g.name, b.block_name, b.room_number, b.booking_date, b.departure_date FROM booking b INNER JOIN guest_info g ON b.guest_ref = g.guest_ref")
            rows = cursor.fetchall()

            # Clear existing table contents
            for row in self.Guest_Details_Table.get_children():
                self.Guest_Details_Table.delete(row)

            # Insert all records into the data table
            for row in rows:
                # Convert dates to proper format before inserting
                booking_date = row[4] if row[4] else ""
                departure_date = row[5] if row[5] else ""
                self.Guest_Details_Table.insert("", END, values=(row[0], row[1], row[2], row[3], booking_date, departure_date))

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    def create_booking_table(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS booking (
    guest_ref TEXT,
    block_name TEXT,
    room_number INTEGER,
    booking_date DATE,
    departure_date DATE,
    
    FOREIGN KEY (guest_ref) REFERENCES guest_info(guest_ref)
)

            ''')
            self.conn.commit()
        except Exception as e:
            print(f"An error occurred while creating the 'booking' table: {str(e)}")

# Main block to start the application
if __name__ == "__main__":
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect("guest_info.db")
        print("Successfully connected to the database.")
        
        # Create the root window
        root = Tk()
        
        # Instantiate the Booking class
        obj = Booking(root, conn)
        
        # Start the tkinter main loop
        root.mainloop()
        
        # Close the database connection
        conn.close()
        print("Connection closed successfully.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
