"""
Complaint Management System - MVC Architecture with MySQL ODBC
Main Application Entry Point
"""

from config.database import db_config
from controllers.controllers import UserController, ComplaintController
from views.views import UserView, ComplaintView

class ComplaintManagementApp:
    """Main application class that orchestrates the complaint management system"""
    
    def __init__(self):
        self.user_controller = UserController()
        self.complaint_controller = ComplaintController()
        self.user_view = UserView()
        self.complaint_view = ComplaintView()
        self.current_user = None
    
    def initialize_database(self):
        """Initialize database tables"""
        try:
            db_config.create_tables()
            print("Database initialized successfully.")
            return True
        except Exception as e:
            print(f"Failed to initialize database: {e}")
            return False
    
    def handle_user_menu(self):
        """Handle user menu operations"""
        while True:
            self.user_view.display_user_menu()
            choice = self.user_view.get_choice()
            
            if choice == '1':
                self.complaint_controller.register_complaint(self.current_user['id'])
            elif choice == '2':
                self.complaint_controller.view_user_complaints(self.current_user['id'])
            elif choice == '3':
                complaint_id = int(self.user_view.get_user_input("Enter Complaint ID"))
                self.complaint_controller.view_complaint_details(complaint_id)
            elif choice == '4':
                complaint_id = int(self.user_view.get_user_input("Enter Complaint ID to delete"))
                self.complaint_controller.delete_complaint(complaint_id, self.current_user['id'])
            elif choice == '5':
                self.user_controller.change_password(self.current_user['id'])
            elif choice == '6':
                self.complaint_controller.search_complaints_by_category(self.current_user['id'])
            elif choice == '7':
                self.complaint_controller.export_complaints_to_csv(self.current_user['id'])
            elif choice == '8':
                break
            else:
                self.user_view.display_error("Invalid choice")
    
    def handle_admin_menu(self):
        """Handle admin menu operations"""
        while True:
            self.user_view.display_admin_menu()
            choice = self.user_view.get_choice()
            
            if choice == '1':
                self.complaint_controller.view_all_complaints()
            elif choice == '2':
                complaint_id = int(self.user_view.get_user_input("Enter Complaint ID"))
                self.complaint_controller.update_complaint_status(complaint_id)
            elif choice == '3':
                complaint_id = int(self.user_view.get_user_input("Enter Complaint ID to assign"))
                self.complaint_controller.assign_complaint(complaint_id)
            elif choice == '4':
                self.user_controller.list_staff()
            elif choice == '5':
                self.complaint_controller.view_complaints_by_status()
            elif choice == '6':
                self.complaint_controller.search_complaints_by_category(is_admin=True)
            elif choice == '7':
                self.complaint_controller.export_complaints_to_csv(is_admin=True)
            elif choice == '8':
                self.complaint_controller.view_complaint_statistics()
            elif choice == '9':
                break
            else:
                self.user_view.display_error("Invalid choice")
    
    def handle_staff_menu(self):
        """Handle staff menu operations"""
        while True:
            self.user_view.display_staff_menu()
            choice = self.user_view.get_choice()
            
            if choice == '1':
                self.complaint_controller.view_assigned_complaints(self.current_user['id'])
            elif choice == '2':
                complaint_id = int(self.user_view.get_user_input("Enter Complaint ID"))
                self.complaint_controller.update_assigned_complaint_status(
                    self.current_user['id'], complaint_id)
            elif choice == '3':
                complaint_id = int(self.user_view.get_user_input("Enter Complaint ID"))
                self.complaint_controller.add_comment_to_complaint(
                    self.current_user['id'], complaint_id)
            elif choice == '4':
                break
            else:
                self.user_view.display_error("Invalid choice")
    
    def run(self):
        """Main application loop"""
        print("Starting Complaint Management System...")
        
        # Initialize database
        if not self.initialize_database():
            return
        
        try:
            while True:
                self.user_view.display_login_menu()
                choice = self.user_view.get_choice()
                
                if choice == '1':
                    self.user_controller.register()
                elif choice == '2':
                    user = self.user_controller.login()
                    if user:
                        self.current_user = user
                        
                        if user['role'] == 'user':
                            self.handle_user_menu()
                        elif user['role'] == 'admin':
                            self.handle_admin_menu()
                        elif user['role'] == 'staff':
                            self.handle_staff_menu()
                        
                        self.current_user = None
                elif choice == '3':
                    print("Thank you for using the Complaint Management System!")
                    break
                else:
                    self.user_view.display_error("Invalid choice")
        
        except KeyboardInterrupt:
            print("\nApplication interrupted by user.")
        except Exception as e:
            print(f"Application error: {e}")
        finally:
            # Close database connection
            db_config.close_connection()
            print("Application terminated.")

def main():
    """Application entry point"""
    app = ComplaintManagementApp()
    app.run()

if __name__ == "__main__":
    main()
