
from PyQt6.QtWidgets import  QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox, QDialog, QComboBox
from PyQt6.QtCore import Qt
from gui import FullDescriptionWindow,FullNameWindow
import csv

cart = []
class ProductDetailsWindow(QDialog):
    def __init__(self, product, username):
        super().__init__()
        self.username = username
        self.setWindowTitle(self.truncated_name(product.name))
        self.setGeometry(150, 150, 400, 300)

        layout = QVBoxLayout()

        name_label = QLabel(self.truncated_name(product.name)) 
        name_label.setStyleSheet("""
            font-family: 'Helvetica', Arial, sans-serif;
            font-size: 16px;
            font-weight: bold;
            color: #FFFFFF; /* Dark Gray for professional look */
            text-align: center;
            padding-bottom: 8px;
        """)
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_label.mousePressEvent = lambda event: self.show_full_name(product.name)

        layout.addWidget(name_label)

        layout.addWidget(QLabel(f"Price: ₹{product.price}"))
        description = product.description
        description_layout = QHBoxLayout()
        if len(description.split()) > 10:
            description_layout.addWidget(QLabel("Description:"))

            view_description_button = QPushButton("View Full Description")
            view_description_button.clicked.connect(lambda: self.show_full_description(description))
            description_layout.addWidget(view_description_button)
        else:
            description_layout.addWidget(QLabel(f"Description: {product.description}"))

        layout.addLayout(description_layout)    

        if type(product).__name__=='Electronics':
            layout.addWidget(QLabel(f"Warranty: {product.warranty}"))
        if type(product).__name__=='Groceries':
            layout.addWidget(QLabel(f"Expiry Date: {product.expiry}"))
        
        if type(product).__name__=='Clothing':
            self.size_combo = QComboBox()
            self.size_combo.addItems(product.size_options)
            layout.addWidget(QLabel("Size:"))
            layout.addWidget(self.size_combo)

        if type(product).__name__=='Clothing':
            self.color_combo = QComboBox()
            self.color_combo.addItems(product.color_options)
            layout.addWidget(QLabel("Color:"))
            layout.addWidget(self.color_combo)

        add_to_cart_button = QPushButton("Add to Cart")
        add_to_cart_button.clicked.connect(lambda: self.add_to_cart(product))
        layout.addWidget(add_to_cart_button)

        self.setLayout(layout)
    
    def show_full_description(self, description):
        """Open a new window to display the full description."""
        full_description_window = FullDescriptionWindow(description)
        full_description_window.exec()

    def show_full_name(self, full_name):
        """Open a new window showing the full name."""
        full_name_window = FullNameWindow(full_name)
        full_name_window.exec()    

    def truncated_name(self, name):
        """Return the first 5 words of the name followed by '...' if needed."""
        words = name.split()
        if len(words) > 5:
            return " ".join(words[:5]) + "..."
        return name    

    def add_to_cart(self, product):
        """Add selected product to cart with size and color."""
        size1 = self.size_combo.currentText() if hasattr(self, 'size_combo') else None
        color1 = self.color_combo.currentText() if hasattr(self, 'color_combo') else None
        
        if color1 and size1:
            existing_product = next((item for item in cart if item['product_id'] == product.product_id and item['size']==size1 and item['color']==color1), None)
        else:
            existing_product = next((item for item in cart if item['product_id'] == product.product_id), None)

        if existing_product:
        
            existing_product['quantity'] = int(existing_product['quantity']) + 1 
        else:
        
            product_copy = {}
            product_copy['name'] = product.name
            product_copy['price'] = product.price
            product_copy['description'] = product.description
            product_copy['product_id'] = product.product_id
            if type(product).__name__=='Electronics':
                product_copy['warranty'] = product.warranty

            if type(product).__name__=='Groceries':
                product_copy['expiry'] = product.expiry
            if size1:
                product_copy['size'] = size1
            if color1:
                product_copy['color'] = color1
            product_copy['quantity'] = 1
            cart.append(product_copy)
    
    
        self.save_cart_to_csv()
        self.accept() 

    def save_cart_to_csv(self):
        """Save cart to CSV for persistence."""
        filename = f"cart_{self.username}.csv" 
        with open(filename, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["name", "price", "description","product_id", "warranty", "expiry", "size", "color","quantity"])
            writer.writeheader()
            for item in cart:
                
                item_data = {key: item.get(key) for key in ["name", "price", "description","product_id", "warranty", "expiry", "size", "color","quantity"] if key in item}
                item_data['quantity'] = int(item_data.get('quantity', 1))
                writer.writerow(item_data)    
