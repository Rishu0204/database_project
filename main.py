from tkinter import *
from PIL import Image, ImageTk
from booking import Booking
from guest_info import Info
from summary import Summary

import sqlite3

class Infantry_Mess:
    def __init__(self, root, conn):
        self.root = root
        self.conn = conn
        self.root.title("INFANTRY MESS")
        self.root.geometry("1550x800+0+0")

        # Top Logo Section
        img1 = Image.open(r"E:\git_database\logo.jpeg")
        img1 = img1.resize((1550, 140), Image.LANCZOS)
        self.photoimg1 = ImageTk.PhotoImage(img1)
        lbimg = Label(self.root, image=self.photoimg1, bd=4, relief=RIDGE)
        lbimg.place(x=180, y=0, width=1400, height=140)

        # Left Logo Section
        img2 = Image.open(r"E:\git_database\mainlogo.jpeg")  
        img2 = img2.resize((180, 140), Image.LANCZOS)
        self.photoimg2 = ImageTk.PhotoImage(img2)
        lbimg = Label(self.root, image=self.photoimg2, bd=4, relief=RIDGE)
        lbimg.place(x=0, y=0, width=180, height=140)

        # Title Section
        lb_title = Label(self.root, text="HOTEL BOOKING", font=("times new roman", 40, "bold", "italic"), bg="black", fg="gold", bd=4, relief=RIDGE)
        lb_title.place(x=0, y=140, width=1550, height=50)

        # Main Frame
        main_frame = Frame(self.root, bd=4, relief=RIDGE)
        main_frame.place(x=0, y=190, width=1550, height=620)

        # Menu Section
        lb_menu = Label(main_frame, text="MENU", font=("times new roman", 20, "bold", "italic"), bg="black", fg="gold", bd=4, relief=RIDGE)
        lb_menu.place(x=0, y=0, width=230)

        # Button Frame
        btn_frame = Frame(main_frame, bd=4, relief=RIDGE, bg="black")
        btn_frame.place(x=0, y=35, width=230, height=250)

        # Guest Info Button
        btn_guest_info = Button(btn_frame, text="Guest Info",command=self.guest_info, font=("times new roman", 14, "bold"), bg="black", fg="gold", bd=3, relief=RAISED)
        btn_guest_info.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Booking Button
        btn_booking = Button(btn_frame, text="Booking", command=self.booking_cust, font=("times new roman", 14, "bold"), bg="black", fg="gold", bd=3, relief=RAISED)
        btn_booking.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        # Summary Button
        btn_summary = Button(btn_frame, text="Summary", command=self.summary_cust,font=("times new roman", 14, "bold"), bg="black", fg="gold", bd=3, relief=RAISED)
        btn_summary.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        
        # Inside Main Frame
        img3 = Image.open(r"E:\git_database\logo.jpeg")  
        img3 = img3.resize((1310, 590), Image.LANCZOS)
        self.photoimg3 = ImageTk.PhotoImage(img3)
        
        lbimg1 = Label(main_frame, image=self.photoimg3, bd=4, relief=RIDGE)
        lbimg1.place(x=225, y=0, width=1310, height=590)
    
    def guest_info(self):
        print("Opening Guest Info window...")
        self.new_window=Toplevel(self.root)
        self.app=Info(self.new_window, self.conn)
        
    def booking_cust(self):
        print("Opening Booking window...")
        self.new_window = Toplevel(self.root)
        self.app = Booking(self.new_window, self.conn)
    
    def summary_cust(self):
        print("Opening Booking window...")
        self.new_window = Toplevel(self.root)
        self.app = Summary(self.new_window, self.conn)
    
    

if __name__ == "__main__":
    conn = sqlite3.connect("guest_info.db")
    root = Tk()
    obj = Infantry_Mess(root, conn)
    root.mainloop()
