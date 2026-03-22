import sys
import csv
from PyQt6.QtWidgets import QApplication
import json
import tkinter as tk
from product_detail_window1 import cart
from login_page import WelcomePage
from product_window1 import ProductWindow
from admin_page import AdminPage


class Product:
    def __init__(self, name,description, price, product_id, quantity):
        self.name = name
        self.price = price
        self.description = description
        self.product_id = product_id
        self.quantity = quantity


class Electronics(Product):
    def __init__(self, name,description, price, product_id, quantity, warranty_period):
        super().__init__(name,description,price, product_id, quantity)
        self.warranty = warranty_period

class Clothing(Product):
    def __init__(self, name,description,price, product_id, quantity, size, color):
        super().__init__(name,description,price, product_id, quantity)
        self.size_options = size
        self.color_options = color

class Groceries(Product):
    def __init__(self, name, price,description, product_id, quantity, expiration_date):
        super().__init__(name, price,description, product_id, quantity)
        self.expiry = expiration_date

class Main:
    def __init__(self,products):
        self.product = products
        self.login()

    def login(self):
        root = tk.Tk()
        app1 = WelcomePage(root)
        root.mainloop()
        try:
            self.username = app1.username
        except:
            return

        try:
            filename = f"cart_{self.username}.csv" 
            with open(filename, mode="r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    cart.append(row)
        except FileNotFoundError:
            pass 

        if app1.user_type not in ['Admin', 'Customer']:
            #print("Error: Invalid user type selected.")
            return 
        elif app1.user_type == 'Admin':
            self.admin_page()
        elif app1.user_type == 'Customer':
            self.consumer_page()

    
    def admin_page(self):
        try:
            root1 = tk.Tk()
            app2 = AdminPage(root1,self.username)
            root1.mainloop()
        except Exception as e:
            print(f"Error: Failed to open Admin Page: {str(e)}")

    def consumer_page(self):
        if not self.product:
            print("Error: No products available to display for the customer.")
            return 
        customer_window = ProductWindow(self.product,self.username)
        customer_window.show()
        sys.exit(app.exec())

def load_json(file_path):
    try:
        with open(file_path, mode="r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return None

def store_data(product):
    item = []
    for category,i in product.items():
        for prod in i:
            try:
                p_name = prod['name']
                p_description = prod['description']
                p_price = prod['price']
                p_product_id = prod['product_id']  
                p_quantity = 0

                if category=='electronics':
                    p_warranty_period = prod['warranty']
                    item.append(Electronics(p_name,p_description,p_price,p_product_id,p_quantity,p_warranty_period))
                    

                if category=='clothing':
                    p_size_options = prod['size_options']
                    p_color_options = prod['color_options']
                    item.append(Clothing(p_name,p_description,p_price,p_product_id,p_quantity,p_size_options,p_color_options))

                if category=='groceries':
                    p_expiry_date = prod['expiry']
                    item.append(Groceries(p_name,p_description,p_price,p_product_id,p_quantity,p_expiry_date))
            except Exception as e:
                print(f"Unexpected error while processing product '{prod.get('name', 'Unnamed')}': {str(e)}")

    return item             

if __name__ == '__main__':
    app = QApplication(sys.argv)

    electronics = load_json('electronics.json')
    groceries = load_json('groceries.json')
    clothing = load_json('clothing.json')

    all_products = {**electronics, **groceries, **clothing}

    products = store_data(all_products)

    window = Main(products) 


