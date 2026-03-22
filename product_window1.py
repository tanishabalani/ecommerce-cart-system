from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox, QScrollArea, QLineEdit, QGridLayout
from PyQt6.QtCore import  QSize
import random
from product_detail_window1 import ProductDetailsWindow
from gui import WordWrapButton, BackgroundWidget
from cart_window1 import Cart

class ProductWindow(QMainWindow):
    def __init__(self, product, username):
        super().__init__()

        self.setWindowTitle("Product Store")
        self.setGeometry(100, 100, 800, 600)
        self.products = product
        self.username = username

        main_layout = QVBoxLayout()

        filter_layout = QHBoxLayout()
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["All", "Electronics", "Groceries", "Clothing"])
        self.filter_combo.currentTextChanged.connect(self.update_products)
        filter_layout.addWidget(QLabel("Filter:"))
        filter_layout.addWidget(self.filter_combo)

        self.filter_text = QLineEdit()
        self.filter_text.setPlaceholderText("Search products...")
        self.filter_text.textChanged.connect(self.update_products)
        filter_layout.addWidget(self.filter_text)
        main_layout.addLayout(filter_layout)

        self.product_scroll = QScrollArea()
        self.product_scroll.setWidgetResizable(True)

        self.bg_widget_scroll = BackgroundWidget()

        self.product_container = QWidget()

        self.product_layout = QGridLayout(self.product_container) 
        self.product_layout.setVerticalSpacing(50)  
        self.product_container.setLayout(self.product_layout)

        bg_layout = QVBoxLayout(self.bg_widget_scroll)  
        bg_layout.addWidget(self.product_container) 

        self.product_scroll.setWidget(self.bg_widget_scroll) 

        main_layout.addWidget(self.product_scroll)

        cart_button = QPushButton("View Cart")
        cart_button.clicked.connect(self.view_cart)
        main_layout.addWidget(cart_button)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.shuffled_products = {}
        self.update_products()

    def update_products(self):
        """Update the displayed products based on filter and search."""
        filter_text = self.filter_text.text().lower()
        filter_category = self.filter_combo.currentText().lower()

        for i in range(self.product_layout.count()):
            widget = self.product_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        if filter_category not in self.shuffled_products.keys():
            self.shuffled_products[filter_category] = self.get_shuffled_products(filter_category)

        filtered_products = [prod for prod in self.shuffled_products[filter_category] if filter_text in prod.name.lower()]

        window_width = self.width()  
        icon_size = 120 
        padding = 50  
        columns = max(1, ((window_width - padding) // (icon_size + padding))) 

        row = 0
        column = 0
        for product in filtered_products:
            product_button = WordWrapButton(self.truncated_name(product.name))
            product_button.setFixedSize(QSize(icon_size, icon_size))  

            product_button.clicked.connect(lambda checked, prod=product: self.show_product_details(prod))

            self.product_layout.addWidget(product_button, row, column)

            column += 1
            if column >= columns:  
                column = 0
                row += 1

        self.product_layout.setRowStretch(row, 1)  

    def get_shuffled_products(self, filter_category):
        """Get the shuffled products based on filter category."""
        filtered_products = []

        if filter_category == "all":
            filtered_products = [prod for prod in self.products]
            random.shuffle(filtered_products)
            return filtered_products

        elif filter_category == "electronics":
            electronics = list(filter(lambda x: type(x).__name__=='Electronics', self.products))
            random.shuffle(electronics)
            return electronics

        elif filter_category == "groceries":
            groceries = list(filter(lambda x: type(x).__name__=='Groceries', self.products))
            random.shuffle(groceries)
            return groceries

        elif filter_category == "clothing":
            clothing = list(filter(lambda x: type(x).__name__=='Clothing', self.products))
            random.shuffle(clothing)
            return clothing
        
        return []

    def show_product_details(self, product):
        """Show product details in a new window."""
        details_window = ProductDetailsWindow(product,self.username)
        details_window.exec()

    def view_cart(self):
        """Display cart and manage quantities."""
        cart_window = Cart(self.username)
        cart_window.exec()

    def truncated_name(self, name):
        """Return the first 5 words of the name followed by '...' if needed."""
        words = name.split()
        if len(words) > 5:
            return " ".join(words[:5]) + "..."
        return name

    def resizeEvent(self, event):
        """Handle window resizing to adjust layout accordingly."""
        self.update_products()
        super().resizeEvent(event)
