# ecommerce-cart-system
Object-oriented e-commerce cart system in Python with product categorization, discount logic, and file-based persistence.
# E-Commerce Cart System 

## Description

This project is a **E-Commerce Cart system** that includes various functionalities such as managing products, an admin page, a shopping cart, and more. It allows users to log in as either **Admin** or **Customer** and access respective functionalities. Admins can add/create products, while customers can browse, view, and add products to their cart.

---

## Steps on how to start the application

- download and extract the zip file given and run "index.py" or type "python index.py" to start your application.
- Make sure these files are loaded correctly before starting the application - "electronics.json","clothing.json","groceries.json"

---

## Requirements

### Operating Systems Supported

- **Windows**
- **Linux**
- **MacOS**

### Prerequisite Software & Libraries

Before running the project, make sure you have the following installed:

1. **Python 3.8+**

   - Download Python: [https://www.python.org/downloads/](https://www.python.org/downloads/)

2. **Install required libraries**

   - After installing Python, you will need to install the following libraries. You can do this by running:

   ```bash
   pip install -r requirements.txt
   ```

   - or type "pip install PyQt6" and "python3-tk" if tkinter is not installed in your system.

---

## Features

- **Admin Page**: It is created to create/add products through admin portal. Once you successfully add the product in admin page, customers can access those products via customer page.
  ![ss6](./assets/6.png)
  ---you can't add a product without filling any of these information as it will result in a error.The type of item give you a choice whether the product belongs to electronics,clothing or groceries.
  ---once you select lets say "clothing", it will look something like this.
  ![ss7](./assets/7.png)
  ---note that we can add multiple size and color for a clothing product.even if you leave description empty , the system will assume it as "N/A" and move on.
  ![ss8](./assets//8.png)
  --- The product that we added in stored in the user data and can be accessed even after re-login. There is an option to remove the product as well.
  ![ss12](./assets/12.png)

---

- **Customer Page**: Customers can browse through various product categories (Electronics, Clothing, Groceries).The suffling of products is randomized everytime you open it.
  ![product_ss](./assets/customer_page.png)
  --here as shown in ss above , there are options to filter the products. We can either type-out the product or choose filter which filters electronics, groceries and clothing.
  ![ss1](./assets/1.png)
  ---on typing lets say "laptop", we get all laptops available in list.
  ![ss2](./assets/2.png)
  ---On clicking the product icon , we can view the product_details which has all informations such as name,price,description,warranty(if any),size and color(if any),expiry(if any)
  ![ss3](./assets/3.png)
  --the full name of product can be obtained by click on the name , and to view full discription you simply click on "view discription" button.
  --from here you can also add your product in the cart. To note that your cart history will always be saved even if you close the application. (note the cart is saved as per the username you logged in with.)
  ![ss4](./assets/4.png)
  --This is how the cart looks like and from here you can change the quantity of product you want , you can also choose to remove that product. it calculates the total price with an applicable discount. At last proceed to checkout and you will recieve your receipt.
  ![ss5](./assets/5.png)
  ---This is how the reciept window looks like and this reciept will be saved as txt file in same folder as application.

---

- **Login System**: Admins and customers can log in with their credentials to access the relevant features.We have kept the login system fairly simple and efficient.
  ![ss9](./assets/9.png)
  --Lets say we head towards the admin portal, the login page looks somewhat like this.
  ![ss10](./assets/10.png)
  --Registering would directly lead you to the admin portal, while for login you must have registered before and use the same username and password.
  ![ss11](./assets//11.png)

---

## List of APIs/database/Libraries used

- For libraries, we used json, uuid(for product_id), csv, PyQt6 and tkinter mainly.

- For extraction of product data, we took help of webscraping of website flipkart. The code for that file is not included in this zip folder as it has no significance with the application. We used library called beautiful Soap to make it possible.

## Classes and Modules made

- The code is mainly divided into 3 parts

  **1. Login Page**: There is only one class dedicated to this named as 'Welcome Page' and that class is then transferred to index.py (main file).

  **2. Admin Page**: There is again onlu one class dedicated to admin page named as 'Admin Page' and is transferred to index.py (main file).

  **3. Customer Page**: Customer Page is now divided into 3 parts.

  - **Product Window**: Its class name is "ProductWindow" which contributes in showcasing of product and filtering the products in Main Customer page.
  - **Product Details Window**: Its class name is "ProductDetailsWindow" which contributes on showcasing details of each individual products we click on.This class is imported into Product Window file.
  - **Cart Window**: Its class name is "Cart" which contains methods like checkout and change quanity of products. Gives visual representation of products we added in cart.After proceeding to checkout, its hands out reciept in a txt file. The cart is imported to "index.py" file.

- **index.py file**: This file contains main class of the application which is "Product" class where each product is assigned into object which attributes like name,price,description,product_id,quantity and some special attributed for categories such as

  - **electronics**-warranty
  - **groceries**-expiry
  - **clothing**- size and color

- **GUI file**: This file contributes in "gui category class" such as
  - background animation
  - texture of icons
  - word wrapping around the icons
  - Discount_calculator
  - Full_name view
  - Full_description view

## Work Done by each team member:

- **S Lekesh (IMT2024088) AND P Siddharth (BT2024207)**: they worked on GUI and backend of admin page of this application while also contributing ideas to overall of this project.
- **Sahil (IMT2024090) And Tharun (IMT2024009)**: They worked on GUI and backend of customer page of this application while also contributing in collection of database for products.
- **Tanisha (BT2024267)**: She worked on both GUI and Backend of Login page while also contributing in overall code and idea of this project.

