import sqlite3
import os
from booking import Booking
from guest_info import Info
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime, timedelta
import pandas as pd
from tkinter import simpledialog
import calendar

class Summary:
    def __init__(self, root, conn):
        self.root = root
        self.conn = conn
        self.root.title("Summary")
        self.root.geometry("1295x550+230+220")

        # Title Section
        lb_title = Label(self.root, text="GUESTS SUMMARY", font=("times new roman", 10, "bold", "italic"), bg="black", fg="gold", bd=4, relief=RIDGE)
        lb_title.pack(fill=X)

        # Table Frame
        table_frame = LabelFrame(self.root, bd=2, relief=RIDGE, text="View Details And Search", font=("times new roman", 12, "bold", "italic"), padx=20, pady=20)
        table_frame.place(x=43, y=50, width=1200, height=490)

        lbsearch = Label(table_frame, text="Search By: ", font=("times new roman", 12), bg="red", fg="white")
        lbsearch.grid(row=0, column=0, sticky=W, padx=2)

        self.combo_search = ttk.Combobox(table_frame, font=("arial", 12, "bold"), width=24, state="readonly")
        self.combo_search["value"] = ("Reference", "Name", "Unit","Block", "Room Number", "Booking Date")
        self.combo_search.current(0)
        self.combo_search.grid(row=0, column=1, padx=2)

        self.entrySearch = Entry(table_frame, font=("times new roman", 12), width=24)
        self.entrySearch.grid(row=0, column=2, padx=2)

        btn_search = Button(table_frame, text="Search", command=self.search_guest, font=("times new roman", 12), bg="black", fg="gold", bd=3, relief=RAISED, width=10)
        btn_search.grid(row=0, column=3, padx=1)

        btn_all = Button(table_frame, text="Show All", command=self.fetch_summary_data, font=("times new roman", 12), bg="black", fg="gold", bd=3, relief=RIDGE, width=10)
        btn_all.grid(row=0, column=4, padx=1)

        btn_download = Button(table_frame, command=self.download_monthly_summary, text="Month-Wise", font=("times new roman", 12), bg="black", fg="gold", bd=3, relief=RIDGE, width=10)
        btn_download.place(x=1070, y=410)
        btn_download1 = Button(table_frame, command=self.download_block_summaries, text="Block-Wise", font=("times new roman", 12), bg="black", fg="gold", bd=3, relief=RIDGE, width=10)
        btn_download1.place(x=900, y=410)

        # Data table
        details_table = Frame(table_frame, bd=3, relief=RIDGE)
        details_table.place(x=0, y=50, width=1155, height=350)

        scroll_x = ttk.Scrollbar(details_table, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(details_table, orient=VERTICAL)

        self.Guest_Details_Table = ttk.Treeview(details_table, columns=("Reference", "Name", "Unit", "Booking Status", "Block", "Room Number", "Booking Date", "Departure Date", "Stay For","Contact No"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        # Set anchor to center for all columns
        for column in ("Reference", "Name", "Unit", "Booking Status", "Block", "Room Number", "Booking Date", "Departure Date", "Stay For", "Contact No"):
            self.Guest_Details_Table.heading(column, text=column, anchor="center")
            self.Guest_Details_Table.column(column, anchor="center")
        
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.Guest_Details_Table.xview)
        scroll_y.config(command=self.Guest_Details_Table.yview)

        self.Guest_Details_Table["show"] = "headings"

        self.Guest_Details_Table.column("Reference", width=100)
        self.Guest_Details_Table.column("Name", width=190)
        self.Guest_Details_Table.column("Unit", width=100)
        self.Guest_Details_Table.column("Booking Status", width=100)
        self.Guest_Details_Table.column("Block", width=100)
        self.Guest_Details_Table.column("Room Number", width=100)
        self.Guest_Details_Table.column("Booking Date", width=100)
        self.Guest_Details_Table.column("Departure Date", width=100)
        self.Guest_Details_Table.column("Stay For", width=100)
      
        self.Guest_Details_Table.column("Contact No", width=100)

        self.Guest_Details_Table.pack(fill=BOTH, expand=1)

        # Create summary view
        create_summary_view(conn)

        # Fetch summary data
        self.fetch_summary_data()

    def search_guest(self):
        try:
            search_by = self.combo_search.get()
            search_query = self.entrySearch.get()

            # Construct the search query based on the selected search criteria
            if search_by == "Reference":
                query_condition = f"g.guest_ref = '{search_query}'"
            elif search_by == "Name":
                query_condition = f"g.name LIKE '%{search_query}%'"
            elif search_by == "Unit":
                query_condition = f"g.unit_fmn LIKE '%{search_query}%'"
            elif search_by == "Block":
                query_condition = f"b.block_name LIKE '%{search_query}%'"
            elif search_by == "Room Number":
                query_condition = f"b.room_number = '{search_query}'"
            elif search_by == "Booking Date":
                # Convert the input date string to the appropriate format
                search_date = datetime.strptime(search_query, "%Y-%m-%d").date().strftime("%Y-%m-%d")
                query_condition = f"b.booking_date = '{search_date}'"
            else:
                # Default to searching by reference number
                query_condition = f"g.guest_ref = '{search_query}'"

            cursor = self.conn.cursor()
            cursor.execute(f"""
                SELECT g.guest_ref, g.name, g.unit_fmn, g.contact,
                    b.block_name, b.room_number, b.booking_date, 
                    b.departure_date
                FROM guest_info g 
                LEFT JOIN booking b ON g.guest_ref = b.guest_ref
                WHERE {query_condition}
            """)

            rows = cursor.fetchall()

            # Clear existing data in the table
            self.Guest_Details_Table.delete(*self.Guest_Details_Table.get_children())

            # Insert fetched data into the table with necessary modifications
            for row in rows:
                reference, name, unit_fmn, contact_no, block, room_number, booking_date, departure_date = row

                # Convert dates to the desired format ("%Y-%m-%d")
                booking_date = datetime.strptime(str(booking_date).split()[0], '%Y-%m-%d').date() if booking_date else ''
                departure_date = datetime.strptime(str(departure_date).split()[0], '%Y-%m-%d').date() if departure_date else ''

                # Calculate stay for
                stay_for = None
                if booking_date and departure_date:
                    stay_for = (departure_date - booking_date).days

                # Determine booking status
                booking_status = "No"
                if block and room_number:
                    booking_status = "Yes"

                # Determine advance payment status
                # advance_payment_status = "No" if advance_payment_status is None else "Yes"

                # Add row to the table
                self.Guest_Details_Table.insert('', 'end', values=(reference, name, unit_fmn, booking_status,
                                                                    block, room_number, booking_date,
                                                                    departure_date, stay_for,contact_no))

        except Exception as e:
            print(f"An error occurred while searching for guests: {str(e)}")



    def fetch_summary_data(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT g.guest_ref, g.name, g.unit_fmn, g.contact,
                    b.block_name, b.room_number,
                    DATE(b.booking_date) AS booking_date, 
                    DATE(b.departure_date) AS departure_date
                    
                FROM guest_info g 
                LEFT JOIN booking b ON g.guest_ref = b.guest_ref
            """)

            rows = cursor.fetchall()

            # Clear existing data in the table
            self.Guest_Details_Table.delete(*self.Guest_Details_Table.get_children())

            # Insert fetched data into the table with necessary modifications
            for row in rows:
                reference, name, unit_fmn, contact_no, block, room_number, booking_date, departure_date = row

                # Calculate stay for (assuming booking_date and departure_date are dates)
                stay_for = None
                # Calculate stay for (assuming booking_date and departure_date are dates)
                stay_for = None
                if booking_date and departure_date: 
                    try:
                        # Attempt conversion to date objects (assuming YYYY-MM-DD format)
                        booking_date = datetime.fromisoformat(str(booking_date))
                        departure_date = datetime.fromisoformat(str(departure_date))
                        # Check if both have values
                        booking_date_int = booking_date.toordinal()  # Only if booking_date is a date
                        departure_date_int = departure_date.toordinal()  # Only if departure_date is a date
                        stay_for = departure_date_int - booking_date_int

                        # Convert back to date object (optional)
                        # stay_for = departure_date - booking_date

                    except ValueError:
                        # Handle potential conversion errors (optional)
                        print("Error: Could not convert dates to valid format")


                # Determine booking status
                booking_status = "No"
                if block and room_number:
                    booking_status = "Yes"

                # Determine advance payment status
                # advance_payment_status = "No" if advance_payment_status is None else "Yes"

                # Add row to the table (excluding time from dates)
                self.Guest_Details_Table.insert('', 'end', values=(reference, name, unit_fmn, booking_status,
                                                                    block, room_number, booking_date,
                                                                    departure_date, stay_for, contact_no))

        except Exception as e:
            print(f"An error occurred while fetching summary data: {str(e)}")






        







    

  

    def download_monthly_summary(self):
        try:
            # Prompt the user for the month and year
            month_year = simpledialog.askstring("Input", "Enter the month and year (e.g., 'March 2024'):")
            if month_year is None:
                return  # Cancelled by the user

            # Parse the month and year input
            month, year = month_year.strip().split()
            month = month.capitalize()
            month_index = list(calendar.month_name).index(month)

            # Get the desktop directory path
            desktop_path = os.path.join(os.path.expanduser("~"), "Downloads")

            # Specify the file name
            monthly_filename = os.path.join(desktop_path, f"summary_{month}_{year}_monthly.xlsx")

            # Get all items from the Treeview
            items = self.Guest_Details_Table.get_children()

            if items:
                data = [self.Guest_Details_Table.item(item, 'values') for item in items]

                if data:
                    # Replace empty strings with None for Adv Payment Date
                    data = [[None if val == "" else val for val in row] for row in data]

                    # Convert data to DataFrame
                    df = pd.DataFrame(data, columns=["Reference", "Name", "Unit","Booking Status", "Block Name", "Room Number", "Booking Date", "Departure Date", "Stay For","Contact"])

                    # Filter data for the selected month and year
                    selected_month_data = df[pd.to_datetime(df['Booking Date'], errors='coerce').dt.month == month_index]

                    # Drop rows with NaT (corresponding to None values in 'Booking Date' column)
                    selected_month_data = selected_month_data.dropna(subset=['Booking Date'])

                    # Calculate monthly summary
                    monthly_summary_data = []
                    for day in range(1, 32):  # Assuming maximum of 31 days
                        date = f"{year}-{month_index:02d}-{day:02d}"
                        bookings_on_day = selected_month_data[selected_month_data['Booking Date'].str.startswith(date)].shape[0]
                        remaining_rooms = 55 - bookings_on_day
                        monthly_summary_data.append([date, bookings_on_day, 55, remaining_rooms])

                    # Calculate total summary for the month
                    total_bookings = selected_month_data.shape[0]
                    total_remaining_rooms = 55 - total_bookings
                    monthly_summary_data.append([f"Total for {month} {year}", total_bookings, 55, total_remaining_rooms])

                    # Convert monthly summary data to DataFrame
                    monthly_summary_df = pd.DataFrame(monthly_summary_data, columns=["Date", "Booked Rooms", "Total Rooms", "Remaining Rooms"])

                    # Write monthly summary DataFrame to Excel file
                    monthly_summary_df.to_excel(monthly_filename, index=False)
                    
                    messagebox.showinfo("Success", f"Monthly summary for {month} {year} downloaded successfully.")
                else:
                    messagebox.showwarning("Warning", "No data found to download.")
            else:
                messagebox.showwarning("Warning", "No data found to download.")
        except Exception as e:
            print(f"An error occurred while downloading monthly summary: {str(e)}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def download_block_summaries(self):
        try:
            # Get the desktop directory path
            desktop_path = os.path.join(os.path.expanduser("~"), "Downloads")

            # Get all items from the Treeview
            items = self.Guest_Details_Table.get_children()

            if items:
                data = [self.Guest_Details_Table.item(item, 'values') for item in items]

                if data:
                    # Replace empty strings with None for Adv Payment Date
                    data = [[None if val == "" else val for val in row] for row in data]

                    # Convert data to DataFrame
                    df = pd.DataFrame(data, columns=["Reference", "Name", "Unit",  "Booking Status", "Block Name", "Room Number", "Booking Date", "Departure Date", "Stay For","Contact"])

                    # Separate data for each block
                    block_data = {block: df[df['Block Name'] == block] for block in df['Block Name'].unique()}
                    
                    for block, block_df in block_data.items():
                        # Create a new Excel workbook with block name as filename
                        block_filename = os.path.join(desktop_path, f"summary_{block.lower().replace(' ', '_')}_block.xlsx")
                        with pd.ExcelWriter(block_filename, engine='xlsxwriter') as writer:
                            # Write block data to a sheet
                            block_df.to_excel(writer, index=False, sheet_name='Block Summary')
                            
                            # Calculate total summary for the block
                            total_bookings = block_df.shape[0]
                            total_remaining_rooms = 55 - total_bookings
                            total_summary_df = pd.DataFrame([[f"Total for {block}", total_bookings, 55, total_remaining_rooms]], columns=["Date", "Booked Rooms", "Total Rooms", "Remaining Rooms"])
                            
                            # Write total summary to a separate sheet
                            total_summary_df.to_excel(writer, index=False, sheet_name='Total Summary')
                    
                    messagebox.showinfo("Success", "Block summaries downloaded successfully.")
                else:
                    messagebox.showwarning("Warning", "No data found to download.")
            else:
                messagebox.showwarning("Warning", "No data found to download.")
        except Exception as e:
            print(f"An error occurred while downloading block summaries: {str(e)}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")




def save_to_excel(self, data):
    try:
        df = pd.DataFrame(data, columns=["Reference", "Name", "Unit", "Contact", "Booking Status", "Block Name", "Room Number", "Booking Date", "Departure Date", "Stay For", "Contact No"])
        
        # Save to Excel file
        df.to_excel("guest_summary.xlsx", index=False)
    except Exception as e:
        print(f"An error occurred while saving data to Excel: {str(e)}")











    def aggregate_data(self, data):
        try:
            # Convert data into DataFrame
            df = pd.DataFrame(data, columns=["Reference", "Name", "Unit", "Contact", "Booking Status", "Block", "Room Number", "Booking Date", "Departure Date", "Stay For", "Contact No"])
            
            # Perform aggregation
            # Assuming your date format is "%Y-%m-%d"
            df['Booking Date'] = pd.to_datetime(df['Booking Date'])
            df['Departure Date'] = pd.to_datetime(df['Departure Date'])
            df['Month'] = df['Booking Date'].dt.strftime('%Y-%m')
            agg_data = df.groupby(['Month', 'Booking Date'])['Room Number'].agg(['count']).reset_index()

            return agg_data

        except Exception as e:
            print(f"An error occurred while aggregating data: {str(e)}")
            return pd.DataFrame()


def create_summary_view(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE VIEW IF NOT EXISTS summary_view AS
            SELECT g.guest_ref AS "Reference", g.name AS "Name", g.unit_fmn AS "Unit", g.contact AS "Contact", 
                   CASE 
                       WHEN b.guest_ref IS NOT NULL THEN "Yes"
                       ELSE "No"
                   END AS "Booking Status",
                   b.block_name AS "Block", b.room_number AS "Room Number", b.booking_date AS "Booking Date", 
                   b.departure_date AS "Departure Date",
                   CASE 
                       WHEN b.departure_date IS NULL OR b.booking_date IS NULL THEN NULL
                       ELSE CAST((julianday(b.departure_date) - julianday(b.booking_date)) AS INTEGER)
                   END AS "Stay For",
                   
                   g.contact_no AS "Contact No"
            FROM guest_info g 
            LEFT JOIN booking b ON g.guest_ref = b.guest_ref
        ''')
        conn.commit()
        print("Summary view created successfully.")
    except Exception as e:
        print(f"An error occurred while creating the summary view: {str(e)}")


if __name__ == "__main__":
    try:
        conn = sqlite3.connect("guest_info.db")
        root = Tk()
        summary = Summary(root, conn)  # Instantiate the Summary class
        summary.fetch_summary_data()  # Call the fetch_summary_data method
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")