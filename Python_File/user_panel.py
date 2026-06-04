"""
User Panel Module
================
This module provides a clean interface to run the admin and user panel application.
It imports the necessary functions from User_admin.py and manages the panel display logic.
"""

from User_admin import display_panel_by_role, display_user_panel, display_admin_panel, find_account, clear_screen


def run_application():
    """
    Main entry point to run the admin and user panel application.
    This function displays a menu allowing users to select their role
    (Admin or User) and then displays the appropriate panel.
    """
    try:
        display_panel_by_role()
    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user. Exiting...")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Please restart the application.")


def display_panel_menu(user_type="user"):
    """
    Display the appropriate panel based on user type.
    
    Args:
        user_type (str): Type of user - "user" or "admin"
    
    Example:
        >>> display_panel_menu("user")  # Displays user login panel
        >>> display_panel_menu("admin") # Displays admin login panel
    """
    clear_screen()
    if user_type.lower() == "user":
        print("--- User Login ---")
        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()
        account = find_account(username, password, role="user")
        if account:
            display_user_panel(account)
        else:
            print("❌ User login failed. Check your credentials.")
    elif user_type.lower() == "admin":
        print("--- Admin Login ---")
        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()
        account = find_account(username, password, role="admin")
        if account:
            display_admin_panel(account)
        else:
            print("❌ Admin login failed. Check your credentials.")
    else:
        print("Invalid user type. Please specify 'user' or 'admin'.")


if __name__ == "__main__":
    # Run the application
    run_application()
