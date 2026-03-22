import csv
from PyQt6.QtWidgets import QVBoxLayout, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QDialog, QSpinBox, QHeaderView
from PyQt6.QtCore import Qt
import time
from product_detail_window1 import cart
from gui import CartEmpty,DiscountCalculator,ReceiptWindow

class Cart(QDialog):
    def __init__(self,username):
        super().__init__()
        self.username = username
        self.setWindowTitle(f"{self.username}'s Cart")
        self.setGeometry(150, 150, 600, 500)

        layout = QVBoxLayout()

       
        self.cart_table = QTableWidget()
        self.cart_table.setColumnCount(5)
        self.cart_table.setHorizontalHeaderLabels(["Product", "Price", "Quantity", "Details", "Actions"])
        layout.addWidget(self.cart_table)

        
        self.total_label = QLabel("Total Price: ₹0.00")
        layout.addWidget(self.total_label)

        self.discount = DiscountCalculator()

       
        self.update_cart_table()

        
        checkout_button = QPushButton("Proceed to Checkout")
        checkout_button.clicked.connect(self.checkout)
        layout.addWidget(checkout_button)

        self.setLayout(layout)

        self.make_columns_resizable()

    def make_columns_resizable(self):
        """Adjust the column resizing behavior."""
        header = self.cart_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)  
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)  
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed) 

    def update_cart_table(self):
        """Update the cart table based on current cart."""
        self.cart_table.setRowCount(len(cart))
        total_price = 0  

        for i, product in enumerate(cart):
            
            self.cart_table.setItem(i, 0, self.create_non_editable_item(product["name"]))
            self.cart_table.setItem(i, 1, self.create_non_editable_item(f"₹{product['price']}"))

            
            quantity = product.get('quantity', 1)
            quantity_spinbox = QSpinBox()
            quantity_spinbox.setValue(int(quantity))
            quantity_spinbox.setMinimum(1)  
            quantity_spinbox.setMaximum(100)  
            quantity_spinbox.valueChanged.connect(lambda value, row=i: self.change_quantity(value, row)) 
            self.cart_table.setCellWidget(i, 2, quantity_spinbox)

            
            details = ""
            if 'warranty' in product and product['warranty']:
                details = f"Warranty: {product['warranty']}"
            elif 'expiry' in product and product['expiry']:
                details = f"Expiry: {product['expiry']}"
            elif 'size' or 'color' in product:
                details = f"Size: {product.get('size', 'N/A')}, Color: {product.get('color', 'N/A')}"
            self.cart_table.setItem(i, 3, self.create_non_editable_item(details))

            
            remove_button = QPushButton("Remove")
            remove_button.clicked.connect(lambda checked, row=i: self.remove_item(row))
            self.cart_table.setCellWidget(i, 4, remove_button)

            
            total_price += float(product['price']) * int(product.get('quantity', 1))

       
        if total_price == 0:
            discount = 0
        else:
            discount = self.discount.calculate_discount(cart)
        discounted_price = total_price * (1 - discount)

        
        self.total_label.setText(f"Total Price: ₹{total_price:.2f} \n Total Price after Discount: ₹{discounted_price:.2f} with a discount of: {discount*100:.2f}%")

    def change_quantity(self, value, row):
        """Change the quantity of a product in the cart."""
        cart[row]['quantity'] = value  
        self.update_cart_table()  
        self.save_cart_to_csv()

    def create_non_editable_item(self, text):
        """Create a non-editable QTableWidgetItem."""
        item = QTableWidgetItem(text)
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)  
        return item

    def remove_item(self, row):
        """Remove item from cart."""
        cart.pop(row)
        self.update_cart_table()  
        self.save_cart_to_csv()

    def checkout(self):
        """Proceed to checkout and apply discount logic."""
        if cart == []:
            cart_empty_window = CartEmpty()
            cart_empty_window.exec()
            return

        
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        receipt_filename = f"receipt_{timestamp}.txt"

        
        discount = self.discount.calculate_discount(cart)*100
        total_price = sum(float(product['price']) * int(product.get('quantity', 1)) for product in cart)
        discounted_price = total_price * (1 - discount / 100)

        receipt_content = "====================================\n"
        receipt_content += f"            {self.username}'s  RECEIPT\n"
        receipt_content += f"            Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        receipt_content += "====================================\n"

       
        receipt_content += "\nItemized Products:\n"
        for product in cart:
            product_name = product['name']
            quantity = int(product.get('quantity', 1))
            price = float(product['price'])
            item_total = price * quantity
            receipt_content += f"Product ID: {product['product_id']}\n"
            receipt_content += f"{product_name}\n"
            receipt_content += f"  Quantity: {quantity}\n"
            receipt_content += f"  Price per unit: Rs {price:.2f}\n"
            receipt_content += f"  Total: Rs {item_total:.2f}\n"
            receipt_content += "------------------------------------\n"

        # Discount and Total Price
        receipt_content += f"Discount Applied: {discount:.2f}%\n"
        receipt_content += f"Total Price: Rs {discounted_price:.2f}\n"
        receipt_content += "====================================\n"
        receipt_content += "Thank you for shopping with us!\n"
        receipt_content += "====================================\n"

        
        with open(receipt_filename, "w") as receipt_file:
            receipt_file.write(receipt_content)

        
        receipt_window = ReceiptWindow(receipt_filename, receipt_content)
        receipt_window.exec()

        
        cart.clear()
        self.save_cart_to_csv() 
        self.accept()

    def save_cart_to_csv(self):
        """Save cart to CSV for persistence."""
        filename = f"cart_{self.username}.csv" 
        with open(filename, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["name", "price", "description","product_id", "warranty", "expiry", "size", "color", "quantity"])
            writer.writeheader()
            for item in cart:
                item_data = {key: item.get(key) for key in ["name", "price", "description","product_id", "warranty", "expiry", "size", "color", "quantity"] if key in item}
                item_data['quantity'] = int(item_data.get('quantity', 1))
                writer.writerow(item_data)