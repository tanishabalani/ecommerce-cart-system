from PyQt6.QtWidgets import  QWidget, QVBoxLayout,  QPushButton, QLabel,  QScrollArea, QDialog, QTextEdit
from PyQt6.QtCore import Qt, QRect, QTimer, QPointF
from PyQt6.QtGui import  QLinearGradient, QColor, QPainter, QBrush, QPen
import random
import math
from datetime import datetime

class BackgroundWidget(QWidget):
    """Custom widget to create an aesthetic background with slow moving bubbles."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAutoFillBackground(True)

        self.bubbles = []
        for _ in range(15): 
            bubble = {
                'position': QPointF(random.uniform(0, 1000), random.uniform(0, 1000)), 
                'size': random.uniform(30, 100),  
                'speed': random.uniform(0.2, 0.5), 
                'direction': QPointF(random.choice([1, -1]), random.choice([1, -1])), 
            }
            self.bubbles.append(bubble)

        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_bubbles)
        self.timer.start(20) 

    def paintEvent(self, event):
        painter = QPainter(self)

       
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(30, 30, 30))  
        gradient.setColorAt(1, QColor(50, 50, 50)) 
        painter.setBrush(gradient)
        painter.drawRect(self.rect())

       
        offset = self.mapToParent(QPointF(0, 0))

       
        for bubble in self.bubbles:
            
            pen = QPen()
            pen.setColor(QColor(0, 255, 255))  
            pen.setWidth(2)  
            pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
            painter.setPen(pen)

            
            gradient_fill = QLinearGradient(bubble['position'].x(), bubble['position'].y(),
                                            bubble['position'].x() + bubble['size'], bubble['position'].y())
            gradient_fill.setColorAt(0, QColor(0, 255, 255, 100)) 
            gradient_fill.setColorAt(1, QColor(0, 255, 255, 50))   
            painter.setBrush(QBrush(gradient_fill))

            
            adjusted_position = bubble['position'] - offset

          
            painter.drawEllipse(QRect(int(adjusted_position.x() - bubble['size'] / 2),
                                      int(adjusted_position.y() - bubble['size'] / 2),
                                      int(bubble['size']), int(bubble['size'])))

    def update_bubbles(self):
        """Update the position of the bubbles."""
        for bubble in self.bubbles:
            
            bubble['position'].setX(bubble['position'].x() + bubble['speed'] * bubble['direction'].x())
            bubble['position'].setY(bubble['position'].y() + bubble['speed'] * bubble['direction'].y())

            
            if bubble['position'].x() - bubble['size'] / 2 < 0 or bubble['position'].x() + bubble['size'] / 2 > self.width():
                bubble['direction'].setX(-bubble['direction'].x())  
            if bubble['position'].y() - bubble['size'] / 2 < 0 or bubble['position'].y() + bubble['size'] / 2 > self.height():
                bubble['direction'].setY(-bubble['direction'].y())  

            
            for other_bubble in self.bubbles:
                if bubble != other_bubble:
                    
                    distance = math.sqrt(
                        (bubble['position'].x() - other_bubble['position'].x()) ** 2 +
                        (bubble['position'].y() - other_bubble['position'].y()) ** 2
                    )
                    min_distance = (bubble['size'] + other_bubble['size']) / 2
                    if distance < min_distance:  
                        
                        bubble['direction'].setX(-bubble['direction'].x())
                        bubble['direction'].setY(-bubble['direction'].y())
                        other_bubble['direction'].setX(-other_bubble['direction'].x())
                        other_bubble['direction'].setY(-other_bubble['direction'].y())

        self.update()

class ScrollableBackgroundWidget(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.bg_widget = BackgroundWidget()
        self.setWidget(self.bg_widget)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setFixedSize(800, 600)  


class WordWrapButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(parent)

        self.label = QLabel(text, self)
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.setContentsMargins(0, 0, 0, 0)  

        self.setFixedSize(120, 120)  
        self.label.setFixedSize(self.size())

        self.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #000000, stop: 0.7 #808080, stop: 1 #555555);
                border: 2px solid #00FFFF;  /* Neon blue border */
                border-radius: 10px;
                color: white;
                font-weight: bold;
                padding: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #333333, stop: 0.7 #A9A9A9, stop: 1 #777777);
                border: 2px solid #00FFFF;  /* Neon blue stays on hover */
            }
            QLabel {
                color: white;
                font-weight: bold;
            }
            QLabel:hover {
                color: #00FFFF;  /* Neon blue color on hover */
            }
        """)


    def setText(self, text):
        """Set the text for both the QPushButton and QLabel inside the button."""
        
        super().setText(text)

        self.label.setText(text)

    def text(self):
        """Get text from the QLabel inside the button."""
        return self.label.text()
    
class FullDescriptionWindow(QDialog):
    def __init__(self, description):
        super().__init__()
        self.setWindowTitle("Full Product Description")
        self.setGeometry(200, 200, 400, 250)

        layout = QVBoxLayout()

        description_label = QLabel(description)
        description_label.setWordWrap(True)  
        description_label.setAlignment(Qt.AlignmentFlag.AlignTop)  
        layout.addWidget(description_label)

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)

        self.setLayout(layout)

class FullNameWindow(QDialog):
    def __init__(self, full_name):
        super().__init__()
        self.setWindowTitle("Full Product Name")
        self.setGeometry(200, 200, 400, 150)

        layout = QVBoxLayout()

        full_name_label = QLabel(full_name)
        full_name_label.setWordWrap(True)
        full_name_label.setStyleSheet("""
            font-family: 'Helvetica', Arial, sans-serif;
            font-size: 18px;
            font-weight: bold;
            color: #FFFFFF; /* Pure Bright White */
            text-align: center;
            padding: 10px;
        """)
        full_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(full_name_label)

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)

        self.setLayout(layout)   

class CartEmpty(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Empty Cart")
        self.setGeometry(200, 200, 400, 150)

        layout = QVBoxLayout()

        full_name_label = QLabel("Your cart is empty, to proceed for checkout please add some items.")
        full_name_label.setWordWrap(True)
        full_name_label.setStyleSheet("""
            font-family: 'Helvetica', Arial, sans-serif;
            font-size: 18px;
            font-weight: bold;
            color: #FFFFFF; /* Pure Bright White */
            text-align: center;
            padding: 10px;
        """)
        full_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(full_name_label)

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)

        self.setLayout(layout)  

class ReceiptWindow(QDialog):
    def __init__(self, receipt_filename, receipt_content):
        super().__init__()

        self.setWindowTitle("Receipt")
        self.setGeometry(150, 150, 600, 400)

        layout = QVBoxLayout()

        self.receipt_text = QTextEdit()
        self.receipt_text.setPlainText(receipt_content)
        self.receipt_text.setReadOnly(True)  
        layout.addWidget(self.receipt_text)

        self.file_path_label = QLabel(f"Receipt saved to: {receipt_filename}")
        layout.addWidget(self.file_path_label)

     
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)

        self.setLayout(layout)               

class DiscountCalculator:

    def calculate_discount(self,products):
        self.products = products
        """Calculate and apply the discount for all products."""
        sum1 = 0
        for product in self.products:
            sum1 += self.calculate_product_discount(product)
        n = len(self.products)
        return (sum1/n)

    def calculate_product_discount(self, product):
        """Calculate the discount for an individual product based on its attributes."""
        category_discount = self.get_category_discount(product)

        price_discount = self.get_price_discount(product)

        quantity_discount = self.get_quantity_discount(product)

        total_discount = category_discount+ price_discount+ quantity_discount
        return total_discount

    def get_category_discount(self, product):
        """Returns discount based on the product category."""
        if 'warranty' in product and product['warranty']:
            return 0.10 
        elif 'expiry' in product and product['expiry']:
            return 0.05  
        elif 'size' or 'color' in product:
            return 0.15  
        else:
            return 0.0  

    def get_price_discount(self, product):
        """Returns discount based on the price of the product."""
        if float(product['price']) >= 10000:
            return 0.10  
        elif float(product['price']) >= 5000:
            return 0.05  
        elif float(product['price'])>= 1000:
            return 0.03  
        else:
            return 0.02 

    def get_quantity_discount(self, product):
        """Returns additional discount based on the quantity purchased."""
        if int(product['quantity']) >= 20:
            return 0.05  
        elif int(product['quantity']) >= 10:
            return 0.02  
        else:
            return 0.0  
