import streamlit as st
import pandas as pd
import os
from datetime import datetime

DATA_FILE = 'data/inventory.csv'
SALES_FILE = 'data/sales.csv'

def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=['id', 'name', 'quantity', 'price'])

def save_data(data):
    data.to_csv(DATA_FILE, index=False)

def add_product(name, quantity, price):
    data = load_data()
    new_id = len(data) + 1
    new_product = pd.DataFrame([[new_id, name, quantity, price]], columns=data.columns)
    data = pd.concat([data, new_product], ignore_index=True)
    save_data(data)

def edit_product(product_id, name, quantity, price):
    data = load_data()
    data.loc[data['id'] == product_id, ['name', 'quantity', 'price']] = name, quantity, price
    save_data(data)

def delete_product(product_id):
    data = load_data()
    data = data[data['id'] != product_id]
    save_data(data)

def low_stock_alert(threshold):
    data = load_data()
    low_stock = data[data['quantity'] < threshold]
    return low_stock

def show_products():
    data = load_data()
    if not data.empty:
        st.write("Existing Products:")
        st.dataframe(data)
    else:
        st.warning("No products found in the inventory.")

def track_sales(product_id, quantity, price):
    if os.path.exists(SALES_FILE):
        sales_data = pd.read_csv(SALES_FILE)
    else:
        sales_data = pd.DataFrame(columns=['id', 'name', 'quantity', 'price', 'date'])
    
    product_data = load_data()
    product_name = product_data.loc[product_data['id'] == product_id, 'name'].values[0]
    
    new_sale = pd.DataFrame([[product_id, product_name, quantity, price, datetime.now().strftime('%Y-%m-%d')]], 
                            columns=sales_data.columns)
    sales_data = pd.concat([sales_data, new_sale], ignore_index=True)
    sales_data.to_csv(SALES_FILE, index=False)

def generate_sales_report():
    if os.path.exists(SALES_FILE):
        sales_data = pd.read_csv(SALES_FILE)
        if not sales_data.empty:
            st.write("Sales Report:")
            st.dataframe(sales_data)
        else:
            st.warning("No sales data found.")
    else:
        st.warning("No sales data found.")

st.title("Inventory Management System")

username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type='password')

if username == "admin" and password == "password":
    st.sidebar.success("Logged in as admin")

    action = st.selectbox("Select an action:", 
                           ["Add Product", "Edit Product", "Delete Product", 
                            "Show Existing Products", "Low Stock Alert", "Track Sales", "Generate Sales Report"])

    if action == "Add Product":
        st.header("Add Product")
        name = st.text_input("Product Name")
        quantity = st.number_input("Quantity", min_value=1)
        price = st.number_input("Price", min_value=0.0)
        
        if st.button("Add Product"):
            add_product(name, quantity, price)
            st.success("Product added successfully!")

    elif action == "Edit Product":
        st.header("Edit Product")
        product_id = st.number_input("Product ID", min_value=1)
        new_name = st.text_input("New Product Name")
        new_quantity = st.number_input("New Quantity", min_value=1)
        new_price = st.number_input("New Price", min_value=0.0)
        
        if st.button("Edit Product"):
            edit_product(product_id, new_name, new_quantity, new_price)
            st.success("Product updated successfully!")

    elif action == "Delete Product":
        st.header("Delete Product")
        delete_id = st.number_input("Product ID to Delete", min_value=1)
        
        if st.button("Delete Product"):
            delete_product(delete_id)
            st.success("Product deleted successfully!")

    elif action == "Show Existing Products":
        st.header("Show Existing Products")
        if st.button("Show Products"):
            show_products()

    elif action == "Low Stock Alert":
        st.header("Low Stock Alert")
        threshold = st.number_input("Threshold", min_value=0)
        
        if st.button("Check Low Stock"):
            low_stock = low_stock_alert(threshold)
            if not low_stock.empty:
                st.write("Low Stock Products:")
                st.dataframe(low_stock)
            else:
                st.success("No low stock products.")

    elif action == "Track Sales":
        st.header("Track Sales")
        product_id = st.number_input("Product ID", min_value=1)
        quantity = st.number_input("Quantity", min_value=1)
        price = st.number_input("Price", min_value=0.0)
        
        if st.button("Track Sale"):
            track_sales(product_id, quantity, price)
            st.success("Sale tracked successfully!")

    elif action == "Generate Sales Report":
        st.header("Sales Report")
        if st.button("Generate Report"):
            generate_sales_report()

else:
    st.warning("Please enter valid credentials.")