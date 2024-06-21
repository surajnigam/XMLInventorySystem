import xml.etree.ElementTree as ET
import os
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

INVENTORY_FILE = 'inventory.xml'

def load_inventory():
    if not os.path.exists(INVENTORY_FILE):
        root = ET.Element("inventory")
        tree = ET.ElementTree(root)
        tree.write(INVENTORY_FILE)
    tree = ET.parse(INVENTORY_FILE)
    return tree

def save_inventory(tree):
    tree.write(INVENTORY_FILE)

def list_items(listbox):
    listbox.delete(*listbox.get_children())
    tree = load_inventory()
    root = tree.getroot()
    for item in root.findall('item'):
        name = item.find('name').text
        quantity = item.find('quantity').text
        listbox.insert("", "end", values=(name, quantity))

def add_item(name, quantity):
    tree = load_inventory()
    root = tree.getroot()
    item = ET.Element('item')
    name_elem = ET.SubElement(item, 'name')
    name_elem.text = name
    quantity_elem = ET.SubElement(item, 'quantity')
    quantity_elem.text = str(quantity)
    root.append(item)
    save_inventory(tree)

def remove_item(name):
    tree = load_inventory()
    root = tree.getroot()
    for item in root.findall('item'):
        if item.find('name').text == name:
            root.remove(item)
            save_inventory(tree)
            return True
    return False

def on_add_button_click(treeview):
    name = simpledialog.askstring("Input", "Enter item name:")
    if name:
        quantity = simpledialog.askinteger("Input", "Enter item quantity:")
        if quantity is not None:
            add_item(name, quantity)
            list_items(treeview)
            messagebox.showinfo("Success", f"Added {name} with quantity {quantity}")

def on_remove_button_click(treeview):
    name = simpledialog.askstring("Input", "Enter item name to remove:")
    if name:
        if remove_item(name):
            list_items(treeview)
            messagebox.showinfo("Success", f"Removed {name}")
        else:
            messagebox.showerror("Error", f"Item {name} not found")

def main():
    root = tk.Tk()
    root.title("Inventory System")

    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Arial", 12, "bold"))
    style.configure("Treeview", font=("Arial", 10), rowheight=25)
    style.configure("TButton", font=("Arial", 10, "bold"), padding=6)

    frame = ttk.Frame(root, padding=10)
    frame.pack(fill=tk.BOTH, expand=True)

    treeview = ttk.Treeview(frame, columns=("Name", "Quantity"), show="headings")
    treeview.heading("Name", text="Name")
    treeview.heading("Quantity", text="Quantity")
    treeview.pack(fill=tk.BOTH, expand=True)

    button_frame = ttk.Frame(root, padding=10)
    button_frame.pack(fill=tk.X)

    add_button = ttk.Button(button_frame, text="Add Item", command=lambda: on_add_button_click(treeview))
    add_button.pack(side=tk.LEFT, padx=5)

    remove_button = ttk.Button(button_frame, text="Remove Item", command=lambda: on_remove_button_click(treeview))
    remove_button.pack(side=tk.LEFT, padx=5)

    list_items(treeview)

    root.mainloop()

if __name__ == '__main__':
    main()
