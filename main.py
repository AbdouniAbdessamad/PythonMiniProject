import tkinter as tk
from tkinter import ttk, messagebox
from pymongo import MongoClient
from datetime import datetime

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['product_database']
collection = db['products']

# Function to add a product
def add_product():
    name = name_entry.get()
    price = price_entry.get()
    date_added = datetime.now().strftime("%Y-%m-%d")  # Get the current date

    if name:  # Only name is required, price is optional
        product = {"name": name, "date_added": date_added}  # Include date_added in the product document
        if price:
            product["price"] = price
        collection.insert_one(product)
        messagebox.showinfo("Success", "Product added successfully!")
        clear_entries()
        show_products()
    else:
        messagebox.showerror("Error", "Please enter product name.")

# Function to show all products
def show_products():
    try:
        products = collection.find({})
        products_listbox.delete(0, tk.END)
        for product in products:
            name = product.get('name', 'XXXXXXXXXX')
            price = product.get('price', 'XXXXXXXXXXX')
            date_added = product.get('date_added', 'XXXX-XX-XX')
            products_listbox.insert(tk.END, f"{date_added} - {name} - ${price}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Function to edit a product
def edit_product():
    selected_product = products_listbox.curselection()
    if selected_product:
        selected_product_index = selected_product[0]
        new_price = edit_price_entry.get()
        new_name = edit_name_entry.get()
        product = collection.find()[selected_product_index]
        product_id = product['_id']

        # Update both name and price if entries are not empty
        update_query = {}
        if new_price:
            update_query["price"] = new_price
        if new_name:
            update_query["name"] = new_name
        
        if update_query:
            collection.update_one({"_id": product_id}, {"$set": update_query})
            messagebox.showinfo("Success", "Product updated successfully!")
            edit_window.destroy()
            show_products()
        else:
            messagebox.showwarning("Warning", "No changes were made.")
    else:
        messagebox.showerror("Error", "Please select a product to edit.")

# Function to delete a product
def delete_product():
    selected_product = products_listbox.curselection()
    if selected_product:
        selected_product_index = selected_product[0]
        product = collection.find()[selected_product_index]
        product_id = product['_id']

        collection.delete_one({"_id": product_id})
        messagebox.showinfo("Success", "Product deleted successfully!")
        show_products()
    else:
        messagebox.showerror("Error", "Please select a product to delete.")

# Function to clear entry fields
def clear_entries():
    name_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)

# GUI Setup
root = tk.Tk()
root.title("Save bought products and calculate your expenses")

# Colors
background_color = "#f0f0f0"
button_color_add = "#4CAF50"  # Green color for Add button
button_color_delete = "#FF5733"  # Red color for Delete button
button_color_edit = "#3498DB"  # Blue color for Edit button
text_color = "#333"  # Dark gray color for text

root.configure(bg=background_color)

# Labels
name_label = ttk.Label(root, text="Product Name:", background=background_color, foreground=text_color)
name_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

price_label = ttk.Label(root, text="Price (dh):", background=background_color, foreground=text_color)
price_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

# Entry fields
name_entry = ttk.Entry(root, width=30)
name_entry.grid(row=0, column=1, padx=10, pady=5)

price_entry = ttk.Entry(root, width=30)
price_entry.grid(row=1, column=1, padx=10, pady=5)

# Buttons
add_button = ttk.Button(root, text="Add Product", command=add_product, style="Add.TButton")
add_button.grid(row=2, column=0, columnspan=2, pady=10)

delete_button = ttk.Button(root, text="Delete Product", command=delete_product, style="Delete.TButton")
delete_button.grid(row=3, column=0, columnspan=2, pady=5)

edit_button = ttk.Button(root, text="Edit Product", command=lambda: open_edit_window(), style="Edit.TButton")
edit_button.grid(row=4, column=0, columnspan=2, pady=5)

# Listbox to display products
products_listbox = tk.Listbox(root, width=50, font=("Helvetica", 12))
products_listbox.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

# Function to open edit window
def open_edit_window():
    global edit_window
    edit_window = tk.Toplevel(root)
    edit_window.title("Edit Product")
    edit_window.geometry("300x150")
    edit_window.configure(bg=background_color)

    edit_name_label = ttk.Label(edit_window, text="New Name:", background=background_color, foreground=text_color)
    edit_name_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

    global edit_name_entry
    edit_name_entry = ttk.Entry(edit_window, width=30)
    edit_name_entry.grid(row=0, column=1, padx=10, pady=5)

    edit_price_label = ttk.Label(edit_window, text="New Price (dh):", background=background_color, foreground=text_color)
    edit_price_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

    global edit_price_entry
    edit_price_entry = ttk.Entry(edit_window, width=30)
    edit_price_entry.grid(row=1, column=1, padx=10, pady=5)

    edit_confirm_button = ttk.Button(edit_window, text="Update", command=edit_product, style="Add.TButton")
    edit_confirm_button.grid(row=2, column=0, columnspan=2, pady=5)

# Style
style = ttk.Style()
style.theme_use('clam')
style.configure("Add.TButton", background=button_color_add, foreground="white")
style.configure("Delete.TButton", background=button_color_delete, foreground="white")
style.configure("Edit.TButton", background=button_color_edit, foreground="white")

# Function to calculate the sum of all prices
def calculate_total():
    total = 0
    products = collection.find({})
    for product in products:
        if 'price' in product:
            total += float(product['price'])
    messagebox.showinfo("Total", f"The total sum of all prices is {total:.2f}dh")

# Function to calculate the sum of prices for products added today
def calculate_total_today():
    total = 0
    today = datetime.now().strftime("%Y-%m-%d")
    products = collection.find({"date_added": today})
    for product in products:
        if 'price' in product:
            total += float(product['price'])
    messagebox.showinfo("Total Today", f"The total sum of prices for products added today is {total:.2f}dh")

def calculate_total_this_month():
    total = 0
    
# Add buttons to calculate the sum of all prices and sum of prices for products added today
calculate_button = ttk.Button(root, text="Calculate Total", command=calculate_total, style="Calculate.TButton")
calculate_button.grid(row=6, column=0, pady=10)

#style for calculate today's expense button
calculate_button_today = ttk.Button(root, text="Calculate Total Today", command=calculate_total_today, style="Calculate.TButton")
calculate_button_today.grid(row=6, column=1, pady=10)

# Style for calculate buttons
style.configure("Calculate.TButton", background="#FFC300", foreground="black")


# Style for calculate button
style.configure("Calculate.TButton", background="#FFC300", foreground="black")

# Call show_products() initially to populate the listbox
show_products()

root.mainloop()
