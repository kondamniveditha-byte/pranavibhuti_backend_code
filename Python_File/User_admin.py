import os
import sys

try:
    import tkinter as tk
    from tkinter import messagebox
except ImportError:
    tk = None
    messagebox = None

users = [
    {
        "username": "user1",
        "password": "pass123",
        "name": "Aisha Sharma",
        "email": "aisha@example.com",
        "role": "user",
        "appointments": ["Dental checkup - July 10", "Eye exam - August 5"],
        "notes": "Allergies: pollen"
    },
    {
        "username": "user2",
        "password": "pass456",
        "name": "Ravi Patel",
        "email": "ravi@example.com",
        "role": "user",
        "appointments": ["General checkup - June 20"],
        "notes": "Blood pressure under control"
    }
]

admins = [
    {
        "username": "admin",
        "password": "admin123",
        "name": "Priya Mehta",
        "email": "priya.admin@example.com",
        "role": "admin"
    }
]


def clear_screen():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def pause():
    input("\nPress Enter to continue...")


def find_account(username, password, role):
    account_list = admins if role == "admin" else users
    for account in account_list:
        if account["username"] == username and account["password"] == password:
            return account
    return None


def display_user_panel(user):
    while True:
        clear_screen()
        print("=== User Panel ===")
        print(f"Welcome, {user['name']} ({user['email']})")
        print("1. View Profile")
        print("2. View Appointments")
        print("3. Update Notes")
        print("4. Logout")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            clear_screen()
            print("--- Profile ---")
            print(f"Name: {user['name']}")
            print(f"Email: {user['email']}")
            print(f"Notes: {user['notes']}")
            pause()
        elif choice == "2":
            clear_screen()
            print("--- Appointments ---")
            if user["appointments"]:
                for idx, appointment in enumerate(user["appointments"], start=1):
                    print(f"{idx}. {appointment}")
            else:
                print("No appointments scheduled.")
            pause()
        elif choice == "3":
            clear_screen()
            print("--- Update Notes ---")
            new_notes = input("Enter new notes or health summary: ").strip()
            if new_notes:
                user["notes"] = new_notes
                print("Notes updated successfully.")
            else:
                print("No changes made.")
            pause()
        elif choice == "4":
            break
        else:
            print("Invalid selection. Please choose 1-4.")
            pause()


def display_admin_panel(admin):
    while True:
        clear_screen()
        print("=== Admin Panel ===")
        print(f"Welcome, {admin['name']} ({admin['email']})")
        print("1. View All Users")
        print("2. Add New User")
        print("3. Remove User")
        print("4. Logout")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            clear_screen()
            print("--- All Users ---")
            for idx, user in enumerate(users, start=1):
                print(f"{idx}. {user['name']} ({user['email']})")
                print(f"   Username: {user['username']}")
                print(f"   Appointments: {len(user['appointments'])}")
                print(f"   Notes: {user['notes']}")
                print()
            pause()
        elif choice == "2":
            clear_screen()
            print("--- Add New User ---")
            username = input("Username: ").strip()
            existing = next((u for u in users if u["username"] == username), None)
            if existing:
                print("A user with that username already exists.")
                pause()
                continue
            password = input("Password: ").strip()
            name = input("Full name: ").strip()
            email = input("Email: ").strip()
            notes = input("Notes: ").strip()
            users.append({
                "username": username,
                "password": password,
                "name": name,
                "email": email,
                "role": "user",
                "appointments": [],
                "notes": notes
            })
            print("User added successfully.")
            pause()
        elif choice == "3":
            clear_screen()
            print("--- Remove User ---")
            username = input("Enter username to remove: ").strip()
            user_to_remove = next((u for u in users if u["username"] == username), None)
            if user_to_remove:
                users.remove(user_to_remove)
                print("User removed successfully.")
            else:
                print("User not found.")
            pause()
        elif choice == "4":
            break
        else:
            print("Invalid selection. Please choose 1-4.")
            pause()


def display_panel_by_role():
    """
    Function to display admin or user panel based on user input.
    This function prompts the user to select their role and then
    authenticates them before displaying the appropriate panel.
    """
    while True:
        clear_screen()
        print("=" * 40)
        print("     SELECT YOUR ROLE")
        print("=" * 40)
        print("1. Login as User")
        print("2. Login as Admin")
        print("3. Exit")
        print("=" * 40)

        choice = input("\nEnter your choice (1-3): ").strip()

        if choice == "1":
            clear_screen()
            print("--- User Login ---")
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()
            user = find_account(username, password, role="user")
            if user:
                display_user_panel(user)
            else:
                print("❌ Login failed. Check your username and password.")
                pause()
        elif choice == "2":
            clear_screen()
            print("--- Admin Login ---")
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()
            admin = find_account(username, password, role="admin")
            if admin:
                display_admin_panel(admin)
            else:
                print("❌ Admin login failed. Check your credentials.")
                pause()
        elif choice == "3":
            clear_screen()
            print("Thank you for using the Healthcare App. Goodbye! 👋")
            sys.exit(0)
        else:
            print("❌ Invalid choice. Please select 1, 2, or 3.")
            pause()


def main():
    while True:
        clear_screen()
        print("=== Healthcare App ===")
        print("1. Login as User")
        print("2. Login as Admin")
        print("3. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            clear_screen()
            print("--- User Login ---")
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            user = find_account(username, password, role="user")
            if user:
                display_user_panel(user)
            else:
                print("Login failed. Check your username and password.")
                pause()
        elif choice == "2":
            clear_screen()
            print("--- Admin Login ---")
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            admin = find_account(username, password, role="admin")
            if admin:
                display_admin_panel(admin)
            else:
                print("Admin login failed. Check your username and password.")
                pause()
        elif choice == "3":
            clear_screen()
            print("Exiting the app. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Please select 1-3.")
            pause()


def run_tkinter_ui():
    if tk is None:
        print("Tkinter is not available on this system. Falling back to console mode.")
        display_panel_by_role()
        return

    root = tk.Tk()
    root.title("Healthcare App")
    root.geometry("400x280")
    root.resizable(False, False)

    def clear_frame():
        for widget in root.winfo_children():
            widget.destroy()

    def show_role_selection():
        clear_frame()

        title = tk.Label(root, text="Healthcare App", font=("Arial", 18, "bold"))
        title.pack(pady=10)

        tk.Button(root, text="Login as User", width=20, command=lambda: show_login("user")).pack(pady=6)
        tk.Button(root, text="Login as Admin", width=20, command=lambda: show_login("admin")).pack(pady=6)
        tk.Button(root, text="Exit", width=20, command=root.quit).pack(pady=20)

    def show_login(role):
        clear_frame()
        header_text = "User Login" if role == "user" else "Admin Login"
        header = tk.Label(root, text=header_text, font=("Arial", 16, "bold"))
        header.pack(pady=10)

        username_label = tk.Label(root, text="Username:")
        username_label.pack(pady=(8, 0))
        username_entry = tk.Entry(root, width=30)
        username_entry.pack()

        password_label = tk.Label(root, text="Password:")
        password_label.pack(pady=(8, 0))
        password_entry = tk.Entry(root, show="*", width=30)
        password_entry.pack()

        def attempt_login():
            account = find_account(username_entry.get().strip(), password_entry.get().strip(), role=role)
            if account:
                if role == "user":
                    show_user_panel_gui(account)
                else:
                    show_admin_panel_gui(account)
            else:
                messagebox.showerror("Login Failed", "Invalid username or password.")

        tk.Button(root, text="Login", width=15, command=attempt_login).pack(pady=12)
        tk.Button(root, text="Back", width=15, command=show_role_selection).pack()

    def show_user_panel_gui(user):
        clear_frame()
        header = tk.Label(root, text=f"User Panel - {user['name']}", font=("Arial", 14, "bold"))
        header.pack(pady=10)

        tk.Label(root, text=f"Email: {user['email']}").pack(pady=(0, 6))
        tk.Label(root, text="Appointments:", font=("Arial", 10, "bold")).pack()
        for appointment in user["appointments"]:
            tk.Label(root, text=f"- {appointment}").pack(anchor="w", padx=20)

        tk.Label(root, text="Notes:", font=("Arial", 10, "bold")).pack(pady=(10, 0))
        notes_text = tk.Text(root, width=40, height=4)
        notes_text.pack()
        notes_text.insert("1.0", user["notes"])

        def save_notes():
            user["notes"] = notes_text.get("1.0", tk.END).strip()
            messagebox.showinfo("Saved", "Notes updated successfully.")

        tk.Button(root, text="Save Notes", width=15, command=save_notes).pack(pady=8)
        tk.Button(root, text="Logout", width=15, command=show_role_selection).pack()

    def show_admin_panel_gui(admin):
        clear_frame()
        header = tk.Label(root, text=f"Admin Panel - {admin['name']}", font=("Arial", 14, "bold"))
        header.pack(pady=10)

        user_list_frame = tk.Frame(root)
        user_list_frame.pack(pady=5)

        tk.Label(user_list_frame, text="Users:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w")
        user_listbox = tk.Listbox(user_list_frame, width=45, height=6)
        user_listbox.grid(row=1, column=0, padx=5, pady=4)

        def populate_users():
            user_listbox.delete(0, tk.END)
            for user in users:
                user_listbox.insert(tk.END, f"{user['username']} - {user['name']}")

        populate_users()

        add_frame = tk.Frame(root)
        add_frame.pack(pady=8)

        tk.Label(add_frame, text="New username:").grid(row=0, column=0, sticky="e")
        new_username = tk.Entry(add_frame, width=20)
        new_username.grid(row=0, column=1, padx=6)

        tk.Label(add_frame, text="Password:").grid(row=1, column=0, sticky="e")
        new_password = tk.Entry(add_frame, width=20, show="*")
        new_password.grid(row=1, column=1, padx=6)

        tk.Label(add_frame, text="Full name:").grid(row=2, column=0, sticky="e")
        new_name = tk.Entry(add_frame, width=20)
        new_name.grid(row=2, column=1, padx=6)

        tk.Label(add_frame, text="Email:").grid(row=3, column=0, sticky="e")
        new_email = tk.Entry(add_frame, width=20)
        new_email.grid(row=3, column=1, padx=6)

        def add_user_gui():
            username_value = new_username.get().strip()
            password_value = new_password.get().strip()
            name_value = new_name.get().strip()
            email_value = new_email.get().strip()
            if not username_value or not password_value or not name_value or not email_value:
                messagebox.showwarning("Missing Data", "All fields are required to add a new user.")
                return
            if any(u["username"] == username_value for u in users):
                messagebox.showerror("User Exists", "A user with that username already exists.")
                return
            users.append({
                "username": username_value,
                "password": password_value,
                "name": name_value,
                "email": email_value,
                "role": "user",
                "appointments": [],
                "notes": ""
            })
            populate_users()
            messagebox.showinfo("User Added", "New user has been added successfully.")
            new_username.delete(0, tk.END)
            new_password.delete(0, tk.END)
            new_name.delete(0, tk.END)
            new_email.delete(0, tk.END)

        def remove_selected_user():
            selection = user_listbox.curselection()
            if not selection:
                messagebox.showwarning("No Selection", "Select a user from the list to remove.")
                return
            index = selection[0]
            username_value = users[index]["username"]
            confirmed = messagebox.askyesno("Confirm Remove", f"Remove user '{username_value}'?")
            if confirmed:
                users.pop(index)
                populate_users()
                messagebox.showinfo("Removed", f"User '{username_value}' removed.")

        tk.Button(root, text="Add User", width=12, command=add_user_gui).pack(pady=4)
        tk.Button(root, text="Remove Selected User", width=18, command=remove_selected_user).pack(pady=2)
        tk.Button(root, text="Logout", width=12, command=show_role_selection).pack(pady=8)

    show_role_selection()
    root.mainloop()


if __name__ == "__main__":
    # Start the graphical application if possible
    run_tkinter_ui()
