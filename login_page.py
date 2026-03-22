import tkinter as tk
from tkinter import messagebox
import json
import os


class WelcomePage:
    def __init__(self,root):
        self.user_type = 'NA'
        self.root = root
        root.title("Welcome")

        
        label_welcome = tk.Label(self.root, text="Welcome to E-Commerce Cart!", font=("Arial", 20))
        label_welcome.pack(pady=30)

        
        button_admin = tk.Button(self.root, text="Admin", width=15, height=2, command=lambda: self.select_user("Admin"))
        button_admin.pack(pady=10)

        button_customer = tk.Button(self.root, text="Customer", width=15, height=2, command=lambda: self.select_user("Customer"))
        button_customer.pack(pady=10)
    
    def load_user_data(self):
        file_name = "users.json"
        if os.path.exists(file_name):
            with open(file_name, 'r') as file:
                return json.load(file)
        return {"consumer": [], "admin": []}

    
    def save_user_data(self,username, password, user_type):
        user_data = self.load_user_data()
        
        
        if user_type == "Admin":
            user_data["admin"].append({"username": username, "password": password})
        elif user_type == "Customer":
            user_data["consumer"].append({"username": username, "password": password})
        
        
        with open("users.json", 'w') as file:
            json.dump(user_data, file, indent=4)

    
    def select_user(self,user_type):
        self.user_type = user_type
        self.root.withdraw()  
        self.show_login_page(user_type)  

    # Function to show the login page
    def show_login_page(self,user_type):
        self.login_page = tk.Toplevel(self.root)  
        self.login_page.title(f"{user_type} Login")

        
        self.label_username = tk.Label(self.login_page, text="Username:")
        self.label_username.grid(row=0, column=0, padx=20, pady=10)

        self.entry_username = tk.Entry(self.login_page)
        self.entry_username.grid(row=0, column=1, padx=20, pady=10)

        self.label_password = tk.Label(self.login_page, text="Password:")
        self.label_password.grid(row=1, column=0, padx=20, pady=10)

        self.entry_password = tk.Entry(self.login_page, show="*")
        self.entry_password.grid(row=1, column=1, padx=20, pady=10)

       
        def login():
            username = self.entry_username.get()
            self.username = username
            password = self.entry_password.get()

            if username == "" or password == "":
                messagebox.showerror("Error", "Please fill in both fields")
            else:
                user_data = self.load_user_data()
                user_found = False
                    
                if user_type == "Admin":
                    user_list = user_data["admin"]
                elif user_type == "Customer":
                    user_list = user_data["consumer"]
                    
                    
                for user in user_list:
                    if user["username"] == username and user["password"] == password:
                        user_found = True
                        messagebox.showinfo("Login", f"Welcome {username}! You are logged in as {user_type}.")
                        self.login_page.destroy()  
                        self.root.quit()  
                        break

                if not user_found:
                    messagebox.showerror("Login Error", "Invalid username or password.")

           
        def register():
            username = self.entry_username.get()
            self.username = username
            password = self.entry_password.get()

            if username == "" or password == "":
                messagebox.showerror("Error", "Please fill in both fields")
            else:
                user_data = self.load_user_data()
                user_exists = False
               
                if user_type == "Admin":
                    user_list = user_data["admin"]
                elif user_type == "Customer":
                    user_list = user_data["consumer"]
                
                for user in user_list:
                    if user["username"] == username:
                        user_exists = True
                        break
                if user_exists:
                    messagebox.showerror("Registration Error", "Username already exists.")
                else:
                    self.save_user_data(username, password, user_type)
                    messagebox.showinfo("Registration", f"User {username} has been registered as {user_type}.")
                    self.login_page.destroy()  
                    self.root.quit()  
        
        button_login = tk.Button(self.login_page, text="Login", command=login)
        button_login.grid(row=2, column=0, padx=20, pady=10)

        button_register = tk.Button(self.login_page, text="Register", command=register)
        button_register.grid(row=2, column=1, padx=20, pady=10)

        self.login_page.protocol("WM_DELETE_WINDOW", self.root.quit)