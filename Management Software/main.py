from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
#Messgebox
from tkinter import messagebox
#For Email Pattern Checking
import re
#Database
import db
#Google Auth
from kivyauth.google_auth import initialize_google, login_google, logout_google


class Login:

    def __init__(self):
        
        master = Tk()
        width = master.winfo_screenwidth()
        height = master.winfo_screenheight()
        master.geometry("%dx%d" % (width, height))
        master.config(bg="#FFF")
        master.title("Employee Management")
        photo = PhotoImage(file="employee.png")
        master.iconphoto(False, photo)
        display = PhotoImage(file="employees.png")
        Label(master, image=display, bg='white').place(x=0, y=80)

        def close():
            master.destroy()
            Register()

        def login():

            result = db.login(email.get(), password.get())

            if result:
                messagebox.showinfo("Success", "Login Successful!")
                master.destroy()
                Dashboard(email.get())
            else:
                messagebox.showerror("Error", "Invalid Username or Password")

        def forgot_password():

            def reset_password():
                update_query = db.reset_password(forgot_email.get(), question.get(), security_ans.get(), new_password.get())

                if update_query == 'updated':
                    messagebox.showinfo("Success", "Password Changed Successfully!")
                elif update_query == 'failed':
                    messagebox.showerror("Failed", "Failed to Change Password")
                else:
                    messagebox.showerror("Invalid", update_query)

            forgot_master = Toplevel(master, bg="white")
            forgot_master.geometry("300x350")
            forgot_master.title("Forgot Password")

            Label(forgot_master, text="Forgot Password", bg="white", font=12).place(x=90, y=10)

            forgot_email = StringVar()
            Label(forgot_master, text="Enter Email :", bg="white").place(x=60,y=50)
            Entry(forgot_master, textvariable=forgot_email, bg="lightgray", width=30).place(x=60, y=70, height=25)

            Label(forgot_master, text="Select Security Question :", bg="white").place(x=60,y=100)
            question = StringVar()
            combo = ttk.Combobox(forgot_master, width=27, textvariable=question, state="readonly")
            combo['values'] = ("What is the name of your first pet?","What was your first car?","What elementary school did you attend?","What is the name of the town where you were born?","Who was your childhood hero?")
            combo.set("Select Security Question")
            combo.place(x=60, y=120, height=25)

            security_ans = StringVar()
            Label(forgot_master, text="Enter Answer :", bg="white").place(x=60,y=150)
            Entry(forgot_master, textvariable=security_ans, bg="lightgray", width=30).place(x=60, y=170, height=25)

            new_password = StringVar()
            Label(forgot_master, text="Enter New Password :", bg="white").place(x=60,y=200)
            Entry(forgot_master, textvariable=new_password, bg="lightgray", width=30).place(x=60, y=220, height=25)

            Button(forgot_master, text="Reset Password", bg="#03045e", fg="white", command=reset_password).place(x=110, y=260)
            
        def on_initialize():
    
            def after_login(name, email, picture):
                
                result = db.google_login(email)

                if result:

                    mast = Toplevel()
                    mast.geometry("300x100+550+300")
                    mast.config(bg="#FFF")
                    p1 = PhotoImage(file="google.png")
                    mast.iconphoto(False, p1)

                    def go():
                        master.destroy()
                        Dashboard(email)
                    Label(mast, text=f"Logged in Successful as {email}", bg="white", pady=10).pack()
                    Button(mast, text="Go to Dashboard", command=go, pady=10, fg="white", bg="#03045e").pack()
                else:
                    messagebox.showerror("Failed", "Failed to Login")
                    
            def error_listener():
                messagebox.showerror("Error", "Failed to Login using Google")

            def login():
                login_google()


            client_id = open("client_id.txt")
            client_secret = open("client_secret.txt")
            initialize_google(after_login, error_listener, client_id.read(), client_secret.read())

            return login()

        Label(master, text="Employee Management", fg="black", bg="white", font=("Maiandra GD", 20)).place(x=900, y=160)
        Label(master, text="Login to Continue...", fg="black", bg="white", font=12).place(x=975, y=210)

        txt_photo = PhotoImage(file="textbox8.png")
        Label(master, image=txt_photo, bg="white").place(x=890, y=245)

        def on_email_focus(e):
            if email.get() == "Enter Email":
                login_email.delete(0, 'end')
                login_email['fg'] = "black"

        def on_email_focusout(e):
            if email.get() == "":
                login_email['fg'] = "grey"
                login_email.insert(0, "Enter Email")

        def go_to_password(e):
            login_password.focus_set()
                                                                                          
        #Label(master, text="Email :", fg="black", bg="white", font=12).place(x=880, y=262)
        email = StringVar()
        login_email = Entry(master, textvariable=email, fg="grey", bd=0, bg="white", font=12)
        login_email.place(x=930, y=263, width=240, height=30)
        login_email.insert(0, "Enter Email")
        login_email.bind('<FocusIn>', on_email_focus)
        login_email.bind('<FocusOut>', on_email_focusout)
        login_email.bind('<Return>', go_to_password)

        def on_password_focus(e):
            if password.get() == "Enter Password":
                login_password.delete(0, 'end')
                login_password['fg'] = "black"
                login_password['show'] = "*"

        def on_password_focusout(e):
            if password.get() == "":
                login_password['fg'] = "grey"
                login_password['show'] = ""
                login_password.insert(0, "Enter Password")

        def go_to_login(e):
            login()

        pass_photo = PhotoImage(file="textbox8.png")
        Label(master, image=pass_photo, bg="white").place(x=890, y=310)

        #ttk.Checkbutton(master, text="Show Password").place(x=957, y=365)
                                                                                          
        #Label(master, text="Password :", fg="black", bg="white", font=12).place(x=850, y=330)
        password = StringVar()
        login_password = Entry(master, textvariable=password, fg="grey", bd=0, bg="white", font=12)
        login_password.place(x=930, y=328, width=240, height=30)
        login_password.insert(0, "Enter Password")
        login_password.bind('<FocusIn>', on_password_focus)
        login_password.bind('<FocusOut>', on_password_focusout)
        login_password.bind('<Return>', go_to_login)

        Button(master, text="Forgot Password", fg="blue", bg="white", font=10, bd=0, cursor="hand2", command=forgot_password).place(x=1060, y=370)

        Button(master, text="LOGIN", fg="white", bg="#03045e", width=30, height=2, relief=RAISED, command=login).place(x=940, y=420)

        google = PhotoImage(file="google.png")
        ttk.Button(master, text="Signin using Google", image=google, compound=LEFT, width=32, command=on_initialize).place(x=940, y=470, height=43)

        Button(master, text="Not have Account Yet? Click Here!", fg="blue", bg="white", bd=0, cursor="hand2", command=close, font=6).place(x=926, y=540)


        mainloop()


class Dashboard():

    def __init__(self, mail):

        user_id = db.get_id(mail)
        
        master = Tk()
        master.config(bg="white")
        width = master.winfo_screenwidth()
        height = master.winfo_screenheight()
        master.geometry("%dx%d" % (width, height))
        master.title("Employee Management")
        p1 = PhotoImage(file="employee.png")
        master.iconphoto(False, p1)

        name_update = StringVar()
        age_update = StringVar()
        dob_update = StringVar()
        gender_update = StringVar()
        email_update = StringVar()
        mobile_update = StringVar()
        salary_update = StringVar()

        def exit():
            is_exit = messagebox.askyesno("Exit", "Are you sure want to Exit?")

            if is_exit:
                master.destroy()

        def single_data(event):
            selected_row = table_view.focus()
            data = table_view.item(selected_row)
            global row
            row = data['values']

            display = Toplevel()
            display.geometry("500x600+250+50")
            display.config(bg="#FFF")
            display.title("Employee Details")

            if row[9] == "None":
                img = Image.open("no_profile_picture.jpg")
                photo = ImageTk.PhotoImage(img)
            else:
                try:
                    img = Image.open(row[9])
                    resized_image = img.resize((200,200), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(resized_image)
                except:
                    img = Image.open('no_profile_picture.jpg')
                    resized_image = img.resize((200,200), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(resized_image)

            lbl = Label(display, image = photo, width=200, height=200, bg="white", borderwidth=1, relief="solid")
            lbl.image = photo
            lbl.pack(pady=30)

            Label(display, text=f"{row[1]}", bg="white", font=("Sitka Small", 16, "bold")).pack()

            Label(display, text=f"Age : {row[2]}", bg="white", font=("Sitka Small", 12)).pack()

            Label(display, text=f"Date of Birth : {row[3]}", bg="white", font=("Sitka Small", 12)).pack()

            Label(display, text=f"Email : {row[4]}", bg="white", font=("Sitka Small", 12)).pack()

            Label(display, text=f"Gender : {row[5]}", bg="white", font=("Sitka Small", 12)).pack()

            Label(display, text=f"Mobile Number : {row[6]}", bg="white", font=("Sitka Small", 12)).pack()

            Label(display, text=f"Salary : {row[7]}", bg="white", font=("Sitka Small", 12)).pack()

            Label(display, text=f"Address : {row[8]}", bg="white", font=("Sitka Small", 12)).pack()

        def getData(event):

            img_path = None

            selected_row = table_view.focus()
            data = table_view.item(selected_row)
            global row
            row = data['values']

            def update():
                status = db.update_employee(name_update.get(), age_update.get(), dob_update.get(), gender_update.get(), email_update.get(), mobile_update.get(), salary_update.get(), address_update.get(1.0, END), self.img_path, row[0])

                if status:
                    messagebox.showinfo("Success", "Employee Updated Successfully!")
                    display_all()
                    emp_frame.destroy()
                else:
                    messagebox.showerror("Error", "Failed to Update Employee")
                    emp_frame.destroy()

            def delete():
                msgbox = messagebox.askyesno("Delete?", "Are you sure want to Delete Employee")

                if msgbox == True:
                    result = db.delete_employee(row[0])
    
                    if result:
                        messagebox.showinfo("Success", "Employee Deleted Successfully!")
                        display_all()
                        emp_frame.destroy()
                    else:
                        messagebox.showerror("Failed", "Failed to Delete Employee!")
                        emp_frame.destroy()
                else:
                    print("Not Deleted")

            emp_frame = Toplevel(master, bg="white")
            emp_frame.geometry("800x450+250+100")
            emp_frame.title("Update Employee")
            p1 = PhotoImage(file="employee.png")
            emp_frame.iconphoto(False, p1)

            details_frame = Frame(emp_frame, bg="white")
            details_frame.place(x=90,y=80)

            if row[9] != "None":
                try:
                    img = Image.open(row[9])
                    resized_image = img.resize((100,100), Image.Resampling.LANCZOS)
                    add_photo =ImageTk.PhotoImage(resized_image)
                    lbl_placeholder = Label(details_frame, image=add_photo, width=100, height=100, bd=0)
                    lbl_placeholder.image = add_photo
                    lbl_placeholder.place(x=520, y=170)
                except:
                    img = Image.open('no_profile_picture.jpg')
                    resized_image = img.resize((100,100), Image.Resampling.LANCZOS)
                    add_photo =ImageTk.PhotoImage(resized_image)
                    lbl_placeholder = Label(details_frame, image=add_photo, width=100, height=100, bd=0)
                    lbl_placeholder.image = add_photo
                    lbl_placeholder.place(x=520, y=170)
            else:
                add_photo =PhotoImage(file='add_employee.png')
                lbl_placeholder = Label(details_frame, image=add_photo, width=100, height=100, bd=0)
                lbl_placeholder.image = add_photo
                lbl_placeholder.place(x=520, y=170)

            def pick_image():
                try:
                    path = filedialog.askopenfilename(filetypes=[("image files","*.jpg*"),
                                                           ("All files",
                                                            "*.*")])
                    img = Image.open(path)
                    self.img_path = path
                    resized_image = img.resize((100,100), Image.Resampling.LANCZOS)
                    picked_image = ImageTk.PhotoImage(resized_image)
                    lbl = Label(details_frame, image=picked_image, width=100, height=100, bd=0)
                    lbl.image = picked_image
                    lbl.place(x=520, y=170)
                except:
                    messagebox.showwarning("Invalid", "No Image Selected")

            Label(emp_frame, text="UPDATE EMPLOYEE", font=20, fg="black", bg="white", pady=20).place(x=350, y=20)

            btn = Button(details_frame, text="Update Photo", bg="lightgray", fg = "black", relief=RAISED, command=pick_image)
            btn.place(x=530, y=280)
            emp_frame.grab_set()
            
            Label(details_frame, text="Name :", font=14, fg="black", bg="white").grid(row=1, column=1, sticky="W", padx=10)
            
            Entry(details_frame, bd=2, width=30, textvariable=name_update, relief=RIDGE).grid(row=1, column=2, sticky="W", pady=10)

            Label(details_frame, text="Age :", font=14, fg="black", bg="white").grid(row=1, column=3, sticky="W", padx=10)
            
            Entry(details_frame, bd=2, width=30, textvariable=age_update, relief=RIDGE).grid(row=1, column=4, sticky="W", pady=10)

            Label(details_frame, text="Date of Birth :", font=14, fg="black", bg="white").grid(row=2, column=1, sticky="W", padx=10)
            
            Entry(details_frame, bd=2, width=30, textvariable=dob_update, relief=RIDGE).grid(row=2, column=2, sticky="W", pady=10)

            Label(details_frame, text="Gender :", font=14, fg="black", bg="white").grid(row=2, column=3, sticky="W", padx=10)
            
            gender_combo = ttk.Combobox(details_frame, width=25, textvariable=gender_update, state="readonly")
            gender_combo.grid(row=2, column=4, sticky="W", pady=10)
            gender_combo['values'] = ("Male", "Female")
            gender_combo.set("Select Gender")

            Label(details_frame, text="Email :", font=14, fg="black", bg="white").grid(row=5, column=1, sticky="W", padx=10)
            
            Entry(details_frame, bd=2, width=30, textvariable=email_update, relief=RIDGE).grid(row=5, column=2, sticky="W", pady=10)

            Label(details_frame, text="Mobile No :", font=14, fg="black", bg="white").grid(row=5, column=3, sticky="W", padx=10)
            
            Entry(details_frame, bd=2, width=30, textvariable=mobile_update, relief=RIDGE).grid(row=5, column=4, sticky="W", pady=10)

            Label(details_frame, text="Salary :", font=14, fg="black", bg="white").grid(row=6, column=1, sticky="W", padx=10)
            
            Entry(details_frame, bd=2, width=30, textvariable=salary_update, relief=RIDGE).grid(row=6, column=2, sticky="W", pady=10)

            Label(details_frame, text="Address :", font=14, fg="black", bg="white").grid(row=7, column=1, sticky="W", padx=10)
            
            address_update = Text(details_frame, bd=2, width=40, height=5, relief=RIDGE)
            address_update.grid(row=7, column=2, columnspan=4, sticky="W", pady=10)

            Button(details_frame, text="UPDATE EMPLOYEE", bg="#03045e", fg="white", width=20, height=2, relief=RAISED, command=update).grid(row=8, column=2, pady=15)

            Button(details_frame, text="DELETE EMPLOYEE", bg="red", fg="white", width=20, height=2, relief=RAISED, command=delete).grid(row=8, column=3, pady=15)

            name_update.set(row[1])
            age_update.set(row[2])
            dob_update.set(row[3])
            email_update.set(row[4])
            gender_update.set(row[5])
            mobile_update.set(row[6])
            salary_update.set(row[7])
            address_update.delete(1.0, END)
            address_update.insert(END, row[8])

        def display_all():

            id_value = db.get_id(mail)

            values = db.display_all(id_value)

            table_view.delete(*table_view.get_children())
            for row in values:
                table_view.insert("", END, values=row)


        def filter_employees():
            if search_title.get() == "Select":
                messagebox.showwarning("Required", "Select Search By is Required")
            elif search_value.get() == "":
                messagebox.showwarning("Required", "Enter Search text is Required")
            else:
                result = db.search_employee(search_title.get().lower(), search_value.get())

                table_view.delete(*table_view.get_children())
                for row in result:
                    table_view.insert("", END, values=row)

        #Add Employee Function
        def add_employee_frame():

            img_path = None

            def add_employee():

                if name.get() == "":
                    messagebox.showwarning("Required", "Name is Required")
                elif age == 0:
                    messagebox.showwarning("Required", "Age is Required")
                elif dob.get() == "":
                    messagebox.showwarning("Required", "Date of Birth is Required")
                elif gender.get() == "Select Gender":
                    messagebox.showwarning("Required", "Gender is Required")
                elif email.get() == "":
                    messagebox.showwarning("Required", "Email is Required")
                elif mobile.get() == "":
                    messagebox.showwarning("Required", "Mobile Number is Required")
                elif len(mobile.get()) != 10:
                    messagebox.showwarning("Not Valid!", "Enter Valid Mobile Number")
                elif address.get(1.0, END) == "":
                    messagebox.showwarning("Required", "Address is Required")
                else:
                    result = db.add_employee(name.get(), age.get(), dob.get(), gender.get(), email.get(), mobile.get(), salary.get(), address.get(1.0, END), self.img_path, user_id)

                    if result:
                        messagebox.showinfo("Success", "Employee Added Successfully!")
                        display_all()
                        emp_frame.destroy()
                    else:
                        messagebox.showerror("Failed", "Failed to add Employee!")
                        emp_frame.destroy()
            
            emp_frame = Toplevel(master, bg="white")
            emp_frame.geometry("800x450+250+100")
            emp_frame.title("Add Employee")
            p1 = PhotoImage(file="employee.png")
            emp_frame.iconphoto(False, p1)

            details_frame = Frame(emp_frame, bg="white")
            details_frame.place(x=90,y=80)

            add_photo =PhotoImage(file='add_employee.png')
            lbl_placeholder = Label(details_frame, image=add_photo, width=100, height=100, bd=0)
            lbl_placeholder.image = add_photo
            lbl_placeholder.place(x=500, y=170)

            #Pick Image Function
            def pick_image():
                try:
                    path = filedialog.askopenfilename(title="Select an Image", filetypes=(('image files','*.jpg'),('All files','*.*')))
                    img = Image.open(path)
                    self.img_path = path
                    resized_image = img.resize((100,100), Image.Resampling.LANCZOS)
                    picked_image = ImageTk.PhotoImage(resized_image)
                    lbl = Label(details_frame, image=picked_image, width=100, height=100, bd=0)
                    lbl.image = picked_image
                    lbl.place(x=500, y=170)
                except:
                    messagebox.showwarning("Nothing!", "No Image Selected")

            Label(emp_frame, text="ADD EMPLOYEE", font=20, fg="black", bg="white", pady=20).place(x=350, y=20)

            btn = Button(details_frame, text="Add Photo", bg="lightgray", fg = "black", relief=RAISED, command=pick_image)
            btn.place(x=515, y=280)
            emp_frame.grab_set()       

            Label(details_frame, text="Name :", font=14, fg="black", bg="white").grid(row=1, column=1, sticky="W", padx=10)
            name = StringVar()
            Entry(details_frame, bd=2, width=30, textvariable=name, relief=RIDGE).grid(row=1, column=2, sticky="W", pady=10)

            Label(details_frame, text="Age :", font=14, fg="black", bg="white").grid(row=1, column=3, sticky="W", padx=10)
            age = StringVar()
            Entry(details_frame, bd=2, width=30, textvariable=age, relief=RIDGE).grid(row=1, column=4, sticky="W", pady=10)

            Label(details_frame, text="Date of Birth :", font=14, fg="black", bg="white").grid(row=2, column=1, sticky="W", padx=10)
            dob = StringVar()
            Entry(details_frame, bd=2, width=30, textvariable=dob, relief=RIDGE).grid(row=2, column=2, sticky="W", pady=10)

            Label(details_frame, text="Gender :", font=14, fg="black", bg="white").grid(row=2, column=3, sticky="W", padx=10)
            gender = StringVar()
            gender_combo = ttk.Combobox(details_frame, width=25, textvariable=gender, state="readonly")
            gender_combo.grid(row=2, column=4, sticky="W", pady=10)
            gender_combo['values'] = ("Male", "Female")
            gender_combo.set("Select Gender")

            Label(details_frame, text="Email :", font=14, fg="black", bg="white").grid(row=5, column=1, sticky="W", padx=10)
            email = StringVar()
            Entry(details_frame, bd=2, width=30, textvariable=email, relief=RIDGE).grid(row=5, column=2, sticky="W", pady=10)

            Label(details_frame, text="Mobile No :", font=14, fg="black", bg="white").grid(row=5, column=3, sticky="W", padx=10)
            mobile = StringVar()
            Entry(details_frame, bd=2, width=30, textvariable=mobile, relief=RIDGE).grid(row=5, column=4, sticky="W", pady=10)

            Label(details_frame, text="Salary :", font=14, fg="black", bg="white").grid(row=6, column=1, sticky="W", padx=10)
            salary = StringVar()
            Entry(details_frame, bd=2, width=30, textvariable=salary, relief=RIDGE).grid(row=6, column=2, sticky="W", pady=10)

            Label(details_frame, text="Address :", font=14, fg="black", bg="white").grid(row=7, column=1, sticky="W", padx=10)
            
            address = Text(details_frame, bd=2, width=40, height=5, relief=RIDGE)
            address.grid(row=7, column=2, columnspan=4, sticky="W", pady=10)

            Button(details_frame, text="ADD EMPLOYEE", bg="#03045e", fg="white", width=20, height=2, relief=RAISED, command=add_employee).grid(row=8, columnspan=7, pady=15) 


        def signout():
            signout = messagebox.askquestion("Signout", "Are you sure want to logout")

            if signout == "yes":
                master.destroy()
                Login()


        def change_password():
            ch_frame = Toplevel(master, bg="white")
            ch_frame.geometry("400x400")
            ch_frame.resizable(False, False)
            ch_frame.title("Change Password")
            p1 = PhotoImage(file="employee.png")
            ch_frame.iconphoto(False, p1)

            def fun_password():

                if old_password.get() == "":
                    messagebox.showwarning("Required", "Old Password is Required")
                elif new_password.get() == "":
                    messagebox.showwarning("Required", "New Password is Required")
                elif confirm_new_password.get() == "":
                    messagebox.showwarning("Required", "Confirm your New Password")
                elif new_password.get() != confirm_new_password.get():
                    messagebox.showwarning("Error!", "New and Confirm Password is not equal")
                else:
                    result = db.change_password(mail, old_password.get(), new_password.get())

                    if result == "success":
                        messagebox.showinfo("Success", "Password Updated Successfully!")
                    else:
                        messagebox.showerror("Error!", result)
                

            Label(ch_frame, text="Change Password", bg="white", font=("Maiandra GD", 14), padx=10).place(x=115, y=50)

            txt_placeholder = PhotoImage(file="textbox.png")
            oldlbl = Label(ch_frame, image=txt_placeholder, bg="white")
            oldlbl.image=txt_placeholder
            oldlbl.place(x=100, y=100)

            def on_password_focus(e):
                if old_password.get() == "Enter Old Password":
                    old_password_entry.delete(0, 'end')
                    old_password_entry['fg'] = "black"
                    old_password_entry['show'] = "*"

            def on_password_focusout(e):
                if old_password.get() == "":
                    old_password_entry['fg'] = "grey"
                    old_password_entry['show'] = ""
                    old_password_entry.insert(0, "Enter Old Password")

            old_password = StringVar()
            old_password_entry = Entry(ch_frame, textvariable=old_password, bd=0, fg="grey", bg="#DBDDD0")
            old_password_entry.place(x=116, y=103, width=169, height=35)
            old_password_entry.insert(0, "Enter Old Password")
            old_password_entry.bind('<FocusIn>', on_password_focus)
            old_password_entry.bind('<FocusOut>', on_password_focusout)

            newlbl = Label(ch_frame, image=txt_placeholder, bg="white")
            newlbl.image=txt_placeholder
            newlbl.place(x=100, y=150)

            def on_newpass_focus(e):
                if new_password.get() == "Enter New Password":
                    new_password_entry.delete(0, 'end')
                    new_password_entry['fg'] = "black"

            def on_newpass_focusout(e):
                if new_password.get() == "":
                    new_password_entry['fg'] = "grey"
                    new_password_entry.insert(0, "Enter New Password")

            new_password = StringVar()
            new_password_entry = Entry(ch_frame, textvariable=new_password, bd=0, fg="grey", bg="#DBDDD0")
            new_password_entry.place(x=116, y=153, width=169, height=35)
            new_password_entry.insert(0, "Enter New Password")
            new_password_entry.bind('<FocusIn>', on_newpass_focus)
            new_password_entry.bind('<FocusOut>', on_newpass_focusout)

            newconlbl = Label(ch_frame, image=txt_placeholder, bg="white")
            newconlbl.image=txt_placeholder
            newconlbl.place(x=100, y=200)

            def on_newconpass_focus(e):
                if confirm_new_password.get() == "Confirm New Password":
                    confirm_password_entry.delete(0, 'end')
                    confirm_password_entry['fg'] = "black"

            def on_newconpass_focusout(e):
                if confirm_new_password.get() == "":
                    confirm_password_entry['fg'] = "grey"
                    confirm_password_entry.insert(0, "Confirm New Password")

            confirm_new_password = StringVar()
            confirm_password_entry = Entry(ch_frame, textvariable=confirm_new_password, bd=0, fg="grey", bg="#DBDDD0")
            confirm_password_entry.place(x=116, y=203, width=169, height=35)
            confirm_password_entry.insert(0, "Confirm New Password")
            confirm_password_entry.bind('<FocusIn>', on_newconpass_focus)
            confirm_password_entry.bind('<FocusOut>', on_newconpass_focusout)

            Button(ch_frame, text="RESET PASSWORD", fg="white", bg="#023e8a", width=20, height=2, command=fun_password, relief=RIDGE, bd=2).place(x=125, y=260)

            ch_frame.grab_set()


        Label(master, text="Employee Management", bg="white", font=("Engravers MT", 20)).pack(pady=50)

        Label(master, text=f"Welcome, {mail}", bg="white", font=("Maiandra GD", 12), padx=10).place(x=10, y=10)

        #Change Password Button
        Button(master, text="Change Password", bg="white", fg="blue", bd=0, command=change_password, cursor="hand2", font=("Palatino Linotype", 10)).place(x=1150, y=10)

        banner = Image.open("flowers.png")
        resized = banner.resize((1100, 100), Image.Resampling.LANCZOS)
        bnr = ImageTk.PhotoImage(resized)
        bn = Label(master, image=bnr, width=1100, bg='white')
        bn.image = bnr
        bn.place(x=20, y=100, height=100)

        #Signout Button
        Button(master, text="Sign Out", bg="white", fg="blue", bd=0, command=signout, cursor="hand2", font=("Palatino Linotype", 10)).place(x=1280, y=10)

        Button(master, text="Add Employees", bg="red", fg="white", relief=RAISED, width=20, height=3, command=add_employee_frame, bd=3, font=("Tahoma", 10, 'bold')).place(x=1155, y=150, height=40)

        search_frame = LabelFrame(master, bg="white", text="Search Employees", relief=RIDGE, font=("Lucida Fax", 10))
        search_frame.place(x=20, y=200, width=1310, height=70)
        Label(search_frame, text="Search By", font=("Lucida Fax", 12), fg="black", bg="white").place(x=10, y=8)

        search_title = StringVar()
        search_combo = ttk.Combobox(search_frame, textvariable=search_title, width=20, state="readonly", font=("Lucida Fax", 10))
        search_combo['values'] = ("Id", "Name", "Age", "Mobile", "Gender", "Email")
        search_combo.place(x=100, y=8, height=30)
        search_combo.set("Select")

        search_value = StringVar()
        Entry(search_frame, bg="white", width=50, relief=RIDGE, bd=2, textvariable=search_value, font=("Lucida Fax", 11)).place(x=300, y=8, height=30)

        Button(search_frame, text="SEARCH", fg="white", bg="#023e8a", width=20, relief=RAISED, command=filter_employees, font=("Tahoma", 10, 'bold')).place(x=770, y=4, height=40)

        Button(search_frame, text="RESET", fg="white", bg="#023e8a", width=20, relief=RAISED, command=display_all, font=("Tahoma", 10, 'bold')).place(x=950, y=4, height=40)

        tree_frame = Frame(master, bg="white")

        style = ttk.Style()
        style.configure("style.Treeview", font=("Sitka Small", 12), rowheight=30)
        style.configure("style.Treeview.Heading", font=("Sitka Small", 12), background='lightgreen', relief=FLAT)

        scrollbar = ttk.Scrollbar(tree_frame, orient=VERTICAL)

        table_view = ttk.Treeview(tree_frame, column=(1,2,3,4,5,6,7,8,9), style = "style.Treeview", yscrollcommand=scrollbar.set)

        scrollbar.pack(side=RIGHT, fill=Y)
        scrollbar.config(command=table_view.yview)

        table_view.heading("1", text="ID")
        table_view.column("1", width=30)
        table_view.heading("2", text="Name")
        table_view.column("2", width=130)
        table_view.heading("3", text="Age")
        table_view.column("3", width=30)
        table_view.heading("4", text="Date of Birth")
        table_view.column("4", width=110)
        table_view.heading("5", text="Email")
        table_view.column("5", width=200)
        table_view.heading("6", text="Gender")
        table_view.column("6", width=50)
        table_view.heading("7", text="Contact")
        table_view.column("7", width=110)
        table_view.heading("8", text="Salary")
        table_view.column("8", width=80)
        table_view.heading("9", text="Address")
        table_view['show'] = 'headings'
        #Right Click to Edit or Delete Employee
        table_view.bind("<ButtonRelease-3>", getData)
        #Single Click to View Employee
        table_view.bind("<Double-Button-1>", single_data)
        table_view.pack(fill=X)

        tree_frame.place(x=20, y=280, width=1328)

        display_all()

        Label(master, text="* Hint : Double Click to view employee and Right Click to Edit/Delete Employee", bg="white", fg='blue', font=12).place(x=20, y=620)

class Register:

    def __init__(self):
        master = Tk()
        width = master.winfo_screenwidth()
        height = master.winfo_screenheight()
        master.geometry("%dx%d" % (width, height))
        master.config(bg="#FFF")
        master.title("Employee Management")
        photo = PhotoImage(file="employee.png")
        master.iconphoto(False, photo)
        display = PhotoImage(file="emp_register.png")
        Label(master, image=display, bg='white').place(x=0, y=0)

        def register_to_login():
            master.destroy()
            Login()

        def register():
            pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            
            if len(email.get()) == 0:
                messagebox.showwarning("Required", "Email is Required")
            elif len(password.get()) == 0:
                messagebox.showwarning("Required", "Password is Required")
            elif len(security_ans.get()) == 0:
                messagebox.showwarning("Required", "Security Question is Required")
            elif re.fullmatch(pattern, email.get()) is None:
                messagebox.showwarning("Required", "Enter Valid Email!")
            else:
                result = db.register(email.get(), password.get(), question.get(), security_ans.get())

                if result == "success":
                    messagebox.showinfo("Success!", "Successfully Registered")
                else:
                    messagebox.showinfo("Failed", result)

        def check_user():
            cursor = db.connection.cursor()

            query = "SELECT * FROM users WHERE email=%s"

            cursor.execute(query, email.get())

            result = cursor.fetchall()

            if result:
                messagebox.showwarning("Exists", "Email Already Registered!")
            else:
                register()


        #Register Using Google
        def on_initialize():
            
            def after_login(name, email, picture):

                result = db.google_register(email)

                if result == "success":
                    mast = Toplevel()
                    mast.geometry("300x100+550+300")
                    p1 = PhotoImage(file="google.png")
                    mast.iconphoto(False, p1)

                    def go():
                        master.destroy()
                        Dashboard(email)
                    Label(mast, text=f"Registered Successfully as {email}").pack()
                    Button(mast, text="Go to Dashboard", command=go).pack()
                else:
                    messagebox.showerror("Failed", result)

            def error_listener():
                messagebox.showerror("Failed", "Failed to Login")

            def login():
                login_google()

                
            client_id = open("client_id.txt")
            client_secret = open("client_secret.txt")
            initialize_google(after_login, error_listener, client_id.read(), client_secret.read())

            return login()

        Label(master, text="Employee Management", fg="black", bg="white", font=("Maiandra GD", 20)).place(x=900, y=100)
        Label(master, text="Register to Manage Employees", fg="black", bg="white", font=12).place(x=930, y=150)

        txt_photo = PhotoImage(file="textbox8.png")
        Label(master, image=txt_photo, bg="white").place(x=890, y=195)

        def on_email_focus(e):
            if email.get() == "Enter Email":
                login_email.delete(0, 'end')
                login_email['fg'] = "black"

        def on_email_focusout(e):
            if email.get() == "":
                login_email['fg'] = "grey"
                login_email.insert(0, "Enter Email")

        def go_to_password(e):
            login_password.focus_set()

        email = StringVar()
        login_email = Entry(master, textvariable=email, fg="grey", bd=0, bg="white", font=12)
        login_email.place(x=930, y=213, width=240, height=30)
        login_email.insert(0, "Enter Email")
        login_email.bind('<FocusIn>', on_email_focus)
        login_email.bind('<FocusOut>', on_email_focusout)
        login_email.bind('<Return>', go_to_password)

        def on_password_focus(e):
            if password.get() == "Enter Password":
                login_password.delete(0, 'end')
                login_password['fg'] = "black"
                login_password['show'] = "*"

        def on_password_focusout(e):
            if password.get() == "":
                login_password['fg'] = "grey"
                login_password['show'] = ""
                login_password.insert(0, "Enter Password")

        def go_to_security_answer(e):
            combo.focus_set()

        Label(master, image=txt_photo, bg="white").place(x=890, y=255)

        password = StringVar()
        login_password = Entry(master, textvariable=password, fg="grey", bd=0, bg="white", font=12)
        login_password.place(x=930, y=273, width=240, height=30)
        login_password.insert(0, "Enter Password")
        login_password.bind('<FocusIn>', on_password_focus)
        login_password.bind('<FocusOut>', on_password_focusout)
        login_password.bind('<Return>', go_to_security_answer)

        Label(master, image=txt_photo, bg="white").place(x=890, y=315)

        def go_to_security(e):
            security_entry.focus_set()

        question = StringVar()
        style = ttk.Style()
        style.configure("TCombobox", bordercolor="white", background="white")
        combo = ttk.Combobox(master, style="TCombobox", width=26, textvariable=question, state="readonly", font=12)
        combo['values'] = ("What is the name of your first pet?","What was your first car?","What elementary school did you attend?","What is the name of the town where you were born?","Who was your childhood hero?")
        combo.set("Select Question")
        combo.place(x=921, y=333, height=30)
        combo.bind('<Return>', go_to_security)

        Label(master, image=txt_photo, bg="white").place(x=890, y=375)

        def on_secans_focus(e):
            if security_ans.get() == "Enter Security Answer":
                security_entry.delete(0, 'end')
                security_entry['fg'] = "black"

        def on_secans_focusout(e):
            if security_ans.get() == "":
                security_entry['fg'] = "grey"
                security_entry.insert(0, "Enter Security Answer")

        def go_to_checkuser(e):
            check_user()

        security_ans = StringVar()
        security_entry = Entry(master, textvariable=security_ans, fg="grey", bd=0, bg="white", font=12)
        security_entry.place(x=930, y=395, width=240, height=30)
        security_entry.insert(0, "Enter Security Answer")
        security_entry.bind('<FocusIn>', on_secans_focus)
        security_entry.bind('<FocusOut>', on_secans_focusout)
        security_entry.bind('<Return>', go_to_checkuser)

        Button(master, text="REGISTER", fg="white", bg="#023e8a", width=30, relief=RAISED, command=check_user).place(x=940, y=450, height=40)

        google = PhotoImage(file="google.png")
        ttk.Button(master, text="Signup using Google", image=google, compound=LEFT, width=32, command=on_initialize).place(x=940, y=510, height=45)

        Button(master, text="Already Have an Account? Click Here!", fg="blue", bg="white", font=6, bd=0, cursor="hand2", command=register_to_login).place(x=910, y=580)


        mainloop()


#Calling Login Class to Start
Login()
