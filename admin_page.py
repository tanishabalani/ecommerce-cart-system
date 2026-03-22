import tkinter as tk
from tkinter import ttk, messagebox
import json
import uuid
import os

class AdminPage:
    def __init__(self, root,username):
        self.root = root
        self.cart = []  
        self.username = username
        self.currency = "INR"  
        self.setup_ui()
        self.load_user_products() 

    def setup_ui(self):
        self.root.title("Admin Portal")
        self.root.geometry("1100x600")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        self.canvas = tk.Canvas(self.root, width=screen_width, height=screen_height)
        self.canvas.pack(fill="both", expand=False)

        self.canvas.config(bg="#ADD8E6") 

        self.canvas.create_text(300, 30, text="Admin Page (Add/remove products from this portal)", font=("Arial", 14, "bold"), fill="black")

        self.canvas.create_text(100, 90, text="Item Name:", font=("Arial", 12), fill="black")
        self.name_entry = self.create_entry(self.root, 200, 80)

        self.canvas.create_text(100, 130, text="Price (in INR):", font=("Arial", 12), fill="black")
        self.price_entry = self.create_entry(self.root, 200, 120)

        self.canvas.create_text(100, 170, text="Description:", font=("Arial", 12), fill="black")
        self.description_entry = self.create_entry(self.root, 200, 160)

        self.canvas.create_text(100, 240, text="Type of Item:", font=("Arial", 12), fill="black")
        self.type_of_item = ttk.Combobox(self.root, values=["Electronics", "Clothing", "Groceries"], state="readonly")
        self.canvas.create_window(270, 240, window=self.type_of_item)
        self.type_of_item.bind("<<ComboboxSelected>>", self.show_additional_fields)

        self.size_label = tk.Label(self.root, text="Size :", font=("Arial", 12), bg="lightblue")
        self.size_entry = self.create_entry(self.root, 250, 280)
        self.size_entry.place_forget()
        
        self.add_size_button = tk.Button(self.root, text="+", command=self.add_size, bg="white")

        self.color_label = tk.Label(self.root, text="Color:", font=("Arial", 12), bg="lightblue")
        self.color_entry = self.create_entry(self.root, 250, 320)
        self.color_entry.place_forget()

        self.add_color_button = tk.Button(self.root, text="+", command=self.add_color, bg="white")

        self.expiration_label = tk.Label(self.root, text="Expiry/best till:", font=("Arial", 12), bg="lightblue")
        self.expiration_entry = self.create_entry(self.root, 250, 360)
        self.expiration_entry.place_forget()

        self.warranty_label = tk.Label(self.root, text="Warranty (months):", font=("Arial", 12), bg="lightblue")
        self.warranty_entry = self.create_entry(self.root, 250, 400)
        self.warranty_entry.place_forget()

        self.add_button = tk.Button(self.root, text="Add Product", command=self.add_to_cart, bg="lightblue")
        self.canvas.create_window(300, 450, window=self.add_button)
       
        self.product_listbox = tk.Listbox(self.root, height=16, width=50, selectmode=tk.SINGLE)
        self.canvas.create_window(800, 220, window=self.product_listbox)

        self.remove_button = tk.Button(self.root, text="Remove Selected Product", command=self.remove_product, bg="lightblue")
        self.canvas.create_window(800, 450, window=self.remove_button)



        self.root.protocol("WM_DELETE_WINDOW", self.root.quit)

        self.sizes = []
        self.colors = []

    def create_entry(self, parent,x ,y):
        entry = tk.Entry(parent, font=("Arial", 12), bd=2, relief="solid", width=25)
        entry.place(x=x, y=y)
        entry.config(bg="white", highlightthickness=2, highlightbackground="lightblue", highlightcolor="lightblue")
        return entry

    def add_size(self):
        size = self.size_entry.get().strip()
        if size:
            self.sizes.append(size)
            self.size_entry.delete(0, tk.END)
            self.update_size_list()

    def add_color(self):
        color = self.color_entry.get()
        if color:
            self.colors.append(color)
            self.color_entry.delete(0, tk.END)
            self.update_color_list()

    def update_size_list(self):
        size_list = ', '.join(self.sizes)
        self.size_label.config(text=f"Size : {size_list}")

    def update_color_list(self):
        color_list = ', '.join(self.colors)
        self.color_label.config(text=f"Color : {color_list}")

    def show_additional_fields(self, event=None):
        item_type = self.type_of_item.get()
        
        self.size_label.place_forget()
        self.size_entry.place_forget()
        self.add_size_button.place_forget()
        self.color_label.place_forget()
        self.color_entry.place_forget()
        self.add_color_button.place_forget()
        self.expiration_label.place_forget()
        self.expiration_entry.place_forget()
        self.warranty_label.place_forget()
        self.warranty_entry.place_forget()

        if item_type == "Electronics":
            self.warranty_label.place(x=100, y=400)
            self.warranty_entry.place(x=280, y=400)
        elif item_type == "Clothing":
            self.size_label.place(x=100, y=280)
            self.size_entry.place(x=250, y=280)
            self.add_size_button.place(x=550, y=280)
            self.color_label.place(x=100, y=320)
            self.color_entry.place(x=250, y=320)
            self.add_color_button.place(x=550, y=320)
        elif item_type == "Groceries":
            self.expiration_label.place(x=100, y=280)
            self.expiration_entry.place(x=250, y=280)

    def add_to_cart(self):
        try:
            item_name = self.name_entry.get()
            price = self.price_entry.get()
            description = self.description_entry.get().strip()  
            if not description:
                description = "No description available."
            item_type = self.type_of_item.get()

            if not item_name or not price or not description or not item_type:
                raise ValueError("Please fill all the required fields.")

            price = float(price)
            product_id = str(uuid.uuid4())  

            item_data = {
                "name": item_name,
                "price": price,
                "description": description,
                "product_id": product_id
            }

            if item_type == "Electronics":
                warranty = int(self.warranty_entry.get()) if self.warranty_entry.get() else 0
                item_data["warranty"] = str(warranty) + " Month(s)"
                self.save_product_to_json(item_data, "electronics")
            elif item_type == "Clothing":
                if not self.sizes: 
                    raise ValueError("Please add at least one size.")
                if not self.colors: 
                    raise ValueError("Please add at least one color.")
                item_data["size_options"] = self.sizes
                item_data["color_options"] = self.colors
                self.save_product_to_json(item_data, "clothing")
            elif item_type == "Groceries":
                expiration_date = self.expiration_entry.get()
                item_data["expiry"] = expiration_date
                self.save_product_to_json(item_data, "groceries")
            else:
                raise ValueError("Invalid item type.")

            self.clear_fields()

            messagebox.showinfo("Success", f"{item_name} added to cart and saved successfully.")
            self.root.protocol("WM_DELETE_WINDOW", self.root.quit)

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def save_product_to_json(self, item_data, category):
        try:
            with open(f'{category}.json', 'r', encoding='utf-8') as json_file:
                existing_data = json.load(json_file)
        except (FileNotFoundError, json.JSONDecodeError):
            existing_data = {f"{category}": []}

        existing_data[f"{category}"].append(item_data)

        with open(f'{category}.json', 'w', encoding='utf-8') as json_file:
            json.dump(existing_data, json_file, ensure_ascii=False, indent=4)

        try:
            user_file = f'{self.username}_products.json'
            if os.path.exists(user_file):
                with open(user_file, 'r', encoding='utf-8') as json_file:
                    existing_data1 = json.load(json_file)
            else:
                existing_data1 = {"products": []}

            existing_data1["products"].append(item_data)

            with open(user_file, 'w', encoding='utf-8') as json_file:
                json.dump(existing_data1, json_file, ensure_ascii=False, indent=4)

            self.load_user_products()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save product: {str(e)}")

    def clear_fields(self):
        self.name_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        self.type_of_item.set('')
        self.sizes.clear()
        self.colors.clear()
        self.size_label.config(text="Size :")
        self.color_label.config(text="Color :")
        self.expiration_entry.delete(0, tk.END)
        self.warranty_entry.delete(0, tk.END)
        self.show_additional_fields()  

    def load_user_products(self):
        """Load products for the logged-in user."""
        self.cart.clear()
        user_file = f'{self.username}_products.json'

        if os.path.exists(user_file):
            with open(user_file, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)
                for product in data.get("products", []):
                    self.cart.append(product)
                    self.product_listbox.insert(tk.END, f"{product['name']} - ₹{product['price']}")

    def update_user_products(self):
        """Update the user's product JSON file after modification."""
        user_file = f'{self.username}_products.json'
        if os.path.exists(user_file):
            with open(user_file, 'w', encoding='utf-8') as json_file:
                json.dump({"products": self.cart}, json_file, ensure_ascii=False, indent=4)   

    def remove_product(self):
        try:
            selected_index = self.product_listbox.curselection()
            if selected_index:
                product_to_remove = self.cart[selected_index[0]]
                self.cart.remove(product_to_remove)
                self.product_listbox.delete(selected_index)
                self.update_user_products()
                messagebox.showinfo("Success", "Product removed successfully.")
            else:
                messagebox.showerror("Error", "Please select a product to remove.")
                return None
        except Exception as e:
            messagebox.showerror("Error", f"Failed to remove product: {str(e)}")     

        try:
            categories = ["electronics", "clothing", "groceries"]
            
            product_removed = False

            for category in categories:
                with open(f"{category}.json", 'r', encoding='utf-8') as file:
                    data = json.load(file)
                products = data.get(category, [])
                
                updated_products = [product for product in products if product["product_id"] != product_to_remove['product_id']]
                
                if len(updated_products) != len(products):
                    data[category] = updated_products 
                    re_category = category 
                    product_removed = True
                    break
            
            if product_removed:
                with open(f"{re_category}.json", 'w', encoding='utf-8') as file:
                    json.dump(data, file, ensure_ascii=False, indent=4)
            else:
                print("nah")

        except Exception as e:
            print(f"Error: {str(e)}")     


