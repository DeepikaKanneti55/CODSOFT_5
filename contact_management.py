import tkinter as tk
from tkinter import messagebox, simpledialog
import json

# Contact storage file
CONTACTS_FILE = "contacts.json"


# Load contacts from file
def load_contacts():
    try:
        with open(CONTACTS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


# Save contacts to file
def save_contacts(contacts):
    with open(CONTACTS_FILE, "w") as file:
        json.dump(contacts, file, indent=4)


# Add a new contact
def add_contact():
    name = simpledialog.askstring("Input", "Enter contact name:")
    phone = simpledialog.askstring("Input", "Enter contact phone number:")
    email = simpledialog.askstring("Input", "Enter contact email:")
    address = simpledialog.askstring("Input", "Enter contact address:")

    if name and phone:
        contacts[name] = {"phone": phone, "email": email, "address": address}
        save_contacts(contacts)
        update_contact_list()
    else:
        messagebox.showwarning("Input Error", "Name and phone number are required.")


# View all contacts
def view_contacts():
    contact_list.delete(0, tk.END)
    for name, details in contacts.items():
        contact_list.insert(
            tk.END,
            f"{name} - Phone: {details['phone']} - Email: {details.get('email', 'N/A')} - Address: {details.get('address', 'N/A')}",
        )


# Search for a contact
def search_contact():
    search_term = simpledialog.askstring("Input", "Enter contact name or phone number:")
    if search_term:
        contact_list.delete(0, tk.END)
        for name, details in contacts.items():
            if search_term.lower() in name.lower() or search_term in details["phone"]:
                contact_list.insert(
                    tk.END,
                    f"{name} - Phone: {details['phone']} - Email: {details.get('email', 'N/A')} - Address: {details.get('address', 'N/A')}",
                )
    else:
        messagebox.showwarning("Input Error", "Search term cannot be empty.")


# Update a contact
def update_contact():
    selected = contact_list.curselection()
    if selected:
        name = contact_list.get(selected[0]).split(" - ")[0]
        phone = simpledialog.askstring(
            "Input",
            f"Update phone number for {name}:",
            initialvalue=contacts[name]["phone"],
        )
        email = simpledialog.askstring(
            "Input",
            f"Update email for {name}:",
            initialvalue=contacts[name].get("email", ""),
        )
        address = simpledialog.askstring(
            "Input",
            f"Update address for {name}:",
            initialvalue=contacts[name].get("address", ""),
        )

        if phone:
            contacts[name] = {"phone": phone, "email": email, "address": address}
            save_contacts(contacts)
            update_contact_list()
        else:
            messagebox.showwarning("Input Error", "Phone number is required.")
    else:
        messagebox.showwarning("Selection Error", "No contact selected.")


# Delete a contact
def delete_contact():
    selected = contact_list.curselection()
    if selected:
        name = contact_list.get(selected[0]).split(" - ")[0]
        del contacts[name]
        save_contacts(contacts)
        update_contact_list()
    else:
        messagebox.showwarning("Selection Error", "No contact selected.")


# Update the contact list in the GUI
def update_contact_list():
    contact_list.delete(0, tk.END)
    for name, details in contacts.items():
        contact_list.insert(
            tk.END,
            f"{name} - Phone: {details['phone']} - Email: {details.get('email', 'N/A')} - Address: {details.get('address', 'N/A')}",
        )


# Main GUI setup
def main():
    global contacts, contact_list

    contacts = load_contacts()

    root = tk.Tk()
    root.title("Contact Management")

    # Set window size
    root.geometry("500x400")

    # Buttons
    tk.Button(root, text="Add Contact", command=add_contact).pack(pady=5)
    tk.Button(root, text="View Contacts", command=view_contacts).pack(pady=5)
    tk.Button(root, text="Search Contact", command=search_contact).pack(pady=5)
    tk.Button(root, text="Update Contact", command=update_contact).pack(pady=5)
    tk.Button(root, text="Delete Contact", command=delete_contact).pack(pady=5)

    # Listbox to display contacts
    contact_list = tk.Listbox(root, width=70, height=15)
    contact_list.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()
