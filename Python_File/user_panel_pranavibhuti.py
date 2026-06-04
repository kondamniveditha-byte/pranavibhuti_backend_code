"""
Mobile-styled User/Admin Panel using Tkinter
Provides a simple mobile-like UI (narrow tall window) for login and role-based panels.
Falls back to console-based prompts when Tkinter is unavailable.

Run: python user_panel_pranavibhuti.py
"""
from __future__ import annotations
import sys
import os
from typing import Optional, Dict, List, Callable

try:
    import tkinter as tk
    from tkinter import messagebox
except Exception:
    tk = None
    messagebox = None

# Sample data
USERS: List[Dict] = [
    {"username": "user1", "password": "pass123", "name": "Aisha Sharma", "email": "aisha@example.com", "role": "user", "appointments": ["Dental - Jul 10", "Eye - Aug 5"], "notes": "Allergies: pollen"},
    {"username": "user2", "password": "pass456", "name": "Ravi Patel", "email": "ravi@example.com", "role": "user", "appointments": ["Checkup - Jun 20"], "notes": "BP normal"},
]

ADMINS: List[Dict] = [
    {"username": "admin", "password": "admin123", "name": "Priya Mehta", "email": "priya.admin@example.com", "role": "admin"}
]


def find_account(username: str, password: str, role: str) -> Optional[Dict]:
    pool = ADMINS if role == "admin" else USERS
    for a in pool:
        if a["username"] == username and a["password"] == password:
            return a
    return None


def console_app():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=== Mobile-style Healthcare App (Console) ===")
        print("1. Login as User")
        print("2. Login as Admin")
        print("3. Exit")
        choice = input("Choose: ").strip()
        if choice == '1':
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            user = find_account(username, password, 'user')
            if user:
                user_panel_console(user)
            else:
                print("Login failed.")
                input("Press Enter...")
        elif choice == '2':
            username = input("Admin username: ").strip()
            password = input("Password: ").strip()
            admin = find_account(username, password, 'admin')
            if admin:
                admin_panel_console(admin)
            else:
                print("Admin login failed.")
                input("Press Enter...")
        elif choice == '3':
            break


def user_panel_console(user: Dict):
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"User Panel - {user['name']}")
        print("1. View Appointments")
        print("2. View/Edit Notes")
        print("3. Logout")
        c = input("Choose: ").strip()
        if c == '1':
            print("Appointments:")
            for appt in user.get('appointments', []):
                print('-', appt)
            input("Enter to continue...")
        elif c == '2':
            print("Notes:")
            print(user.get('notes',''))
            new = input("New notes (leave empty to keep): ").strip()
            if new:
                user['notes'] = new
                print("Saved")
            input("Enter to continue...")
        else:
            break


def admin_panel_console(admin: Dict):
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Admin Panel - {admin['name']}")
        print("1. List users")
        print("2. Add user")
        print("3. Remove user")
        print("4. Logout")
        c = input("Choose: ").strip()
        if c == '1':
            for u in USERS:
                print(u['username'], '-', u['name'], '-', u['email'])
            input("Enter to continue...")
        elif c == '2':
            uname = input("Username: ").strip()
            if any(u['username'] == uname for u in USERS):
                print("Exists")
                input("Enter to continue...")
                continue
            pwd = input("Password: ").strip()
            name = input("Full name: ").strip()
            email = input("Email: ").strip()
            USERS.append({"username": uname, "password": pwd, "name": name, "email": email, "role": "user", "appointments": [], "notes": ""})
            print("Added")
            input("Enter to continue...")
        elif c == '3':
            uname = input("Username to remove: ").strip()
            found = next((u for u in USERS if u['username']==uname), None)
            if found:
                USERS.remove(found)
                print("Removed")
            else:
                print("Not found")
            input("Enter to continue...")
        else:
            break


def run_tk_mobile_ui():
    if tk is None:
        print("Tkinter not available — using console.")
        console_app()
        return

    root = tk.Tk()
    width, height = 360, 700
    root.geometry(f"{width}x{height}")
    root.title("PRANAVIBHUTI")
    root.resizable(False, False)

    HEADER_BG = '#0b3b66'
    ACCENT = '#0a84ff'
    CARD_BG = '#ffffff'
    FG = '#222222'
    SECONDARY = '#f2f6ff'
    INPUT_BG = '#f5f7fb'

    root.configure(bg=HEADER_BG)

    container = tk.Frame(root, bg=HEADER_BG)
    container.pack(fill='both', expand=True)

    header = tk.Frame(container, bg=HEADER_BG)
    header.pack(fill='x', pady=(20, 6))
    header_title = tk.Label(header, text="PRANAVIBHUTI", bg=HEADER_BG, fg='white', font=("Helvetica", 20, 'bold'))
    header_title.pack()
    header_subtitle = tk.Label(header, text="Your Complete Health Companion", bg=HEADER_BG, fg='lightgrey', font=("Helvetica", 9))
    header_subtitle.pack()

    card = tk.Frame(container, bg=CARD_BG, bd=0)
    card.place(relx=0.05, rely=0.18, relwidth=0.9, relheight=0.75)

    footer = tk.Frame(container, bg=HEADER_BG)
    footer.pack(side='bottom', pady=12)

    def clear_card():
        for w in card.winfo_children():
            w.destroy()

    def set_header(title: str, subtitle: str):
        header_title.config(text=title)
        header_subtitle.config(text=subtitle)

    def create_action_button(text: str, command: Callable[[], None], width: int = 20):
        return tk.Button(card, text=text, bg=ACCENT, fg='white', width=width, relief='flat', command=command)

    def show_login_screen():
        clear_card()
        set_header("PRANAVIBHUTI", "Your Complete Health Companion")

        tk.Label(card, text="Welcome Back", bg=CARD_BG, fg=FG, font=("Helvetica", 16, 'bold')).pack(pady=(18, 6))
        tk.Label(card, text="Login with your mobile number", bg=CARD_BG, fg='grey', font=("Helvetica", 9)).pack()

        phone_frame = tk.Frame(card, bg=CARD_BG)
        phone_frame.pack(pady=12)
        tk.Button(phone_frame, text="IN +91", bg='#eef6ff', relief='flat').pack(side='left', padx=(10, 6))
        phone_var = tk.StringVar()
        tk.Entry(phone_frame, textvariable=phone_var, width=20, bd=1, relief='solid', bg=INPUT_BG).pack(side='left')

        def send_otp():
            num = phone_var.get().strip()
            if not num or not num.isdigit():
                messagebox.showwarning("Invalid", "Enter a valid mobile number")
                return
            messagebox.showinfo("OTP Sent", f"OTP sent to +91 {num}")
            show_secondary_login()

        create_action_button("Send OTP", send_otp).pack(pady=6)

        tk.Label(card, text="OR CONTINUE WITH", bg=CARD_BG, fg='grey', font=("Helvetica", 8)).pack(pady=(8, 4))
        social_frame = tk.Frame(card, bg=CARD_BG)
        social_frame.pack(pady=(0, 10))
        tk.Button(social_frame, text="Biometric", width=12, relief='groove').pack(side='left', padx=6)
        tk.Button(social_frame, text="Digi Yatra", width=12, relief='groove').pack(side='left', padx=6)

        tk.Label(card, text="Need help?", bg=CARD_BG, fg='grey', font=("Helvetica", 8)).pack(pady=(8, 0))
        tk.Button(card, text="Login with Username", bg=SECONDARY, fg=FG, width=20, relief='flat', command=show_secondary_login).pack(pady=4)

    def show_secondary_login():
        sec = tk.Toplevel(root)
        sec.geometry('320x280')
        sec.title('Login')
        sec.resizable(False, False)

        tk.Label(sec, text='Login Options', font=("Helvetica", 14, 'bold')).pack(pady=12)
        tk.Label(sec, text='Use username/password to continue', fg='grey').pack()

        tk.Label(sec, text='Username', anchor='w').pack(fill='x', padx=16, pady=(12, 0))
        uentry = tk.Entry(sec, bd=1, relief='solid', bg=INPUT_BG)
        uentry.pack(fill='x', padx=16)

        tk.Label(sec, text='Password', anchor='w').pack(fill='x', padx=16, pady=(10, 0))
        pentry = tk.Entry(sec, show='*', bd=1, relief='solid', bg=INPUT_BG)
        pentry.pack(fill='x', padx=16)

        def try_login():
            u = uentry.get().strip()
            p = pentry.get().strip()
            acc = find_account(u, p, 'user') or find_account(u, p, 'admin')
            if acc:
                sec.destroy()
                if acc['role'] == 'user':
                    show_user_dashboard(acc)
                else:
                    show_admin_dashboard(acc)
            else:
                messagebox.showerror('Login failed', 'Invalid credentials')

        tk.Button(sec, text='Login', bg=ACCENT, fg='white', width=20, relief='flat', command=try_login).pack(pady=16)

    def user_action_bar(user: Dict, parent: tk.Frame):
        action_frame = tk.Frame(parent, bg=CARD_BG)
        action_frame.pack(pady=10)
        tk.Button(action_frame, text='Appointments', width=12, bg=SECONDARY, fg=FG, relief='flat', command=lambda: show_user_appointments(user)).pack(side='left', padx=4)
        tk.Button(action_frame, text='Profile', width=12, bg=SECONDARY, fg=FG, relief='flat', command=lambda: show_user_profile(user)).pack(side='left', padx=4)
        tk.Button(action_frame, text='Logout', width=12, bg=SECONDARY, fg=FG, relief='flat', command=show_login_screen).pack(side='left', padx=4)

    def show_user_dashboard(user: Dict):
        clear_card()
        set_header(f"Hello, {user['name']}", "Your personalised health dashboard")

        tk.Label(card, text="Upcoming Appointments", bg=CARD_BG, fg=FG, font=("Helvetica", 12, 'bold')).pack(pady=(12, 6), anchor='w', padx=16)
        if user.get('appointments'):
            for appt in user['appointments']:
                tk.Label(card, text=f"• {appt}", bg=CARD_BG, fg='grey').pack(anchor='w', padx=24)
        else:
            tk.Label(card, text="No upcoming appointments.", bg=CARD_BG, fg='grey').pack(anchor='w', padx=24)

        stat_frame = tk.Frame(card, bg=CARD_BG)
        stat_frame.pack(fill='x', pady=12, padx=16)
        stat_card = tk.Frame(stat_frame, bg=SECONDARY, bd=0, relief='ridge')
        stat_card.pack(side='left', fill='both', expand=True, padx=(0, 6))
        tk.Label(stat_card, text='Health Notes', bg=SECONDARY, fg=FG, font=("Helvetica", 10, 'bold')).pack(pady=(10, 4))
        tk.Label(stat_card, text=user.get('notes', 'No notes yet'), bg=SECONDARY, fg='grey', wraplength=140, justify='left').pack(padx=8, pady=(0, 10))

        stat_card2 = tk.Frame(stat_frame, bg=SECONDARY, bd=0, relief='ridge')
        stat_card2.pack(side='left', fill='both', expand=True, padx=(6, 0))
        tk.Label(stat_card2, text='Appointments', bg=SECONDARY, fg=FG, font=("Helvetica", 10, 'bold')).pack(pady=(10, 4))
        tk.Label(stat_card2, text=f"{len(user.get('appointments', []))} scheduled", bg=SECONDARY, fg='grey').pack(padx=8, pady=(0, 10))

        tk.Label(card, text="Quick Actions", bg=CARD_BG, fg=FG, font=("Helvetica", 12, 'bold')).pack(pady=(6, 8), anchor='w', padx=16)
        user_action_bar(user, card)

        tk.Button(card, text='View Full Profile', width=24, bg=ACCENT, fg='white', relief='flat', command=lambda: show_user_profile(user)).pack(pady=10)

    def show_user_appointments(user: Dict):
        clear_card()
        set_header("Appointments", "Manage your upcoming visits")

        appointment_frame = tk.Frame(card, bg=CARD_BG)
        appointment_frame.pack(fill='both', expand=True, padx=12, pady=12)
        listbox = tk.Listbox(appointment_frame, width=40, height=8, bd=0, relief='ridge')
        listbox.pack(side='top', fill='both', expand=True)
        for appt in user.get('appointments', []):
            listbox.insert('end', appt)

        tk.Label(appointment_frame, text='Add a new appointment', bg=CARD_BG, fg='grey').pack(pady=(10, 0), anchor='w')
        new_appt_var = tk.StringVar()
        tk.Entry(appointment_frame, textvariable=new_appt_var, bd=1, relief='solid', bg=INPUT_BG).pack(fill='x', pady=4)

        def add_appointment():
            value = new_appt_var.get().strip()
            if value:
                user.setdefault('appointments', []).append(value)
                listbox.insert('end', value)
                new_appt_var.set('')
                messagebox.showinfo('Added', 'Appointment added successfully')
            else:
                messagebox.showwarning('Missing', 'Enter appointment details')

        tk.Button(appointment_frame, text='Add Appointment', bg=ACCENT, fg='white', command=add_appointment).pack(pady=8)
        tk.Button(card, text='Back to Dashboard', bg=SECONDARY, fg=FG, width=20, relief='flat', command=lambda: show_user_dashboard(user)).pack(pady=6)

    def show_user_profile(user: Dict):
        clear_card()
        set_header("Profile", "Your personal details")

        profile_frame = tk.Frame(card, bg=CARD_BG)
        profile_frame.pack(fill='both', expand=True, padx=16, pady=12)

        tk.Label(profile_frame, text='Name', bg=CARD_BG).grid(row=0, column=0, sticky='w', pady=(0, 4))
        name_var = tk.StringVar(value=user.get('name', ''))
        tk.Entry(profile_frame, textvariable=name_var, bd=1, relief='solid', bg=INPUT_BG).grid(row=0, column=1, sticky='ew', pady=(0, 4))

        tk.Label(profile_frame, text='Email', bg=CARD_BG).grid(row=1, column=0, sticky='w', pady=(0, 4))
        email_var = tk.StringVar(value=user.get('email', ''))
        tk.Entry(profile_frame, textvariable=email_var, bd=1, relief='solid', bg=INPUT_BG).grid(row=1, column=1, sticky='ew', pady=(0, 4))

        tk.Label(profile_frame, text='Health Notes', bg=CARD_BG).grid(row=2, column=0, sticky='nw', pady=(0, 4))
        notes_text = tk.Text(profile_frame, width=28, height=6, bd=1, relief='solid', bg=INPUT_BG)
        notes_text.grid(row=2, column=1, sticky='ew', pady=(0, 4))
        notes_text.insert('1.0', user.get('notes', ''))

        profile_frame.columnconfigure(1, weight=1)

        def save_profile():
            user['name'] = name_var.get().strip() or user['name']
            user['email'] = email_var.get().strip() or user['email']
            user['notes'] = notes_text.get('1.0', 'end').strip()
            messagebox.showinfo('Saved', 'Profile updated successfully')
            show_user_dashboard(user)

        tk.Button(card, text='Save Profile', bg=ACCENT, fg='white', width=24, relief='flat', command=save_profile).pack(pady=10)
        tk.Button(card, text='Back to Dashboard', bg=SECONDARY, fg=FG, width=24, relief='flat', command=lambda: show_user_dashboard(user)).pack()

    def show_admin_dashboard(admin: Dict):
        clear_card()
        set_header(f"Admin Dashboard", f"Welcome {admin['name']}")

        summary_frame = tk.Frame(card, bg=CARD_BG)
        summary_frame.pack(fill='x', padx=16, pady=12)
        tk.Label(summary_frame, text=f"Total Users: {len(USERS)}", bg=CARD_BG, fg=FG, font=("Helvetica", 12, 'bold')).pack(anchor='w')
        total_appointments = sum(len(u.get('appointments', [])) for u in USERS)
        tk.Label(summary_frame, text=f"Open Appointments: {total_appointments}", bg=CARD_BG, fg='grey').pack(anchor='w', pady=(4, 0))

        tk.Label(card, text='User Management', bg=CARD_BG, fg=FG, font=("Helvetica", 12, 'bold')).pack(pady=(10, 6), anchor='w', padx=16)
        tk.Button(card, text='Manage Users', bg=ACCENT, fg='white', width=24, relief='flat', command=lambda: show_admin_user_management(admin)).pack(pady=4)
        tk.Button(card, text='View Reports', bg=SECONDARY, fg=FG, width=24, relief='flat').pack(pady=4)
        tk.Button(card, text='Logout', bg=SECONDARY, fg=FG, width=24, relief='flat', command=show_login_screen).pack(pady=16)

    def show_admin_user_management(admin: Dict):
        clear_card()
        set_header('User Management', 'Add or remove patients')

        listbox = tk.Listbox(card, width=42, height=8, bd=1, relief='solid')
        listbox.pack(padx=12, pady=(12, 6))

        def refresh_users():
            listbox.delete(0, 'end')
            for u in USERS:
                listbox.insert('end', f"{u['username']} — {u['name']}")

        refresh_users()

        form_frame = tk.Frame(card, bg=CARD_BG)
        form_frame.pack(fill='x', padx=12, pady=6)
        tk.Label(form_frame, text='Username', bg=CARD_BG).grid(row=0, column=0, sticky='w')
        username_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=username_var, bd=1, relief='solid', bg=INPUT_BG).grid(row=0, column=1, sticky='ew', padx=6)
        tk.Label(form_frame, text='Password', bg=CARD_BG).grid(row=1, column=0, sticky='w', pady=(8, 0))
        password_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=password_var, bd=1, relief='solid', bg=INPUT_BG, show='*').grid(row=1, column=1, sticky='ew', padx=6, pady=(8, 0))
        form_frame.columnconfigure(1, weight=1)

        def add_user():
            user_name = username_var.get().strip()
            user_password = password_var.get().strip()
            if not user_name or not user_password:
                messagebox.showwarning('Missing', 'Username and password are required')
                return
            if any(u['username'] == user_name for u in USERS):
                messagebox.showerror('Exists', 'That user already exists')
                return
            USERS.append({
                'username': user_name,
                'password': user_password,
                'name': user_name,
                'email': '',
                'role': 'user',
                'appointments': [],
                'notes': ''
            })
            username_var.set('')
            password_var.set('')
            refresh_users()
            messagebox.showinfo('Added', 'New user added')

        def remove_user():
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning('Select', 'Please select a user to remove')
                return
            idx = selection[0]
            user_item = USERS[idx]
            if messagebox.askyesno('Confirm', f"Remove {user_item['username']}?"):
                USERS.pop(idx)
                refresh_users()

        btn_frame = tk.Frame(card, bg=CARD_BG)
        btn_frame.pack(pady=8)
        tk.Button(btn_frame, text='Add User', bg=ACCENT, fg='white', width=12, relief='flat', command=add_user).pack(side='left', padx=6)
        tk.Button(btn_frame, text='Remove Selected', bg=SECONDARY, fg=FG, width=14, relief='flat', command=remove_user).pack(side='left', padx=6)
        tk.Button(card, text='Back to Dashboard', bg=SECONDARY, fg=FG, width=24, relief='flat', command=lambda: show_admin_dashboard(admin)).pack(pady=12)

    show_login_screen()
    root.mainloop()


if __name__ == '__main__':
    # Prefer GUI mobile-like interface; console fallback if tkinter unavailable.
    if tk is None:
        console_app()
    else:
        run_tk_mobile_ui()
