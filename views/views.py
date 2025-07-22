import csv
from typing import List, Dict, Any

class BaseView:
    """Base view class with common display methods"""
    
    def display_message(self, message: str):
        """Display a simple message"""
        print(message)
    
    def display_error(self, error: str):
        """Display an error message"""
        print(f"Error: {error}")
    
    def display_success(self, message: str):
        """Display a success message"""
        print(f"Success: {message}")

class UserView(BaseView):
    """View class for user-related displays"""
    
    def display_login_menu(self):
        """Display the main login menu"""
        print("\n=== Complaint Management System ===")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
    
    def display_user_menu(self):
        """Display user menu options"""
        print("\n=== User Menu ===")
        print("1. Register Complaint")
        print("2. View My Complaints")
        print("3. View Complaint Details")
        print("4. Delete Complaint")
        print("5. Change Password")
        print("6. Search Complaints by Category")
        print("7. Export My Complaints to CSV")
        print("8. Logout")
    
    def display_admin_menu(self):
        """Display admin menu options"""
        print("\n=== Admin Menu ===")
        print("1. View All Complaints")
        print("2. Update Complaint Status")
        print("3. Assign Complaint")
        print("4. List Staff")
        print("5. View Complaints by Status")
        print("6. Search Complaints by Category")
        print("7. Export All Complaints to CSV")
        print("8. View Complaint Statistics")
        print("9. Logout")
    
    def display_staff_menu(self):
        """Display staff menu options"""
        print("\n=== Staff Menu ===")
        print("1. View Assigned Complaints")
        print("2. Update Complaint Status")
        print("3. Add Comment to Complaint")
        print("4. Logout")
    
    def display_staff_list(self, staff_members: List[Dict[str, Any]]):
        """Display list of staff members"""
        print("\n=== Staff Members ===")
        if not staff_members:
            print("No staff members found.")
            return
        
        for staff in staff_members:
            print(f"ID: {staff['id']}, Name: {staff['name']}, Email: {staff['email']}")
    
    def get_user_input(self, prompt: str) -> str:
        """Get input from user"""
        return input(f"{prompt}: ").strip()
    
    def get_choice(self) -> str:
        """Get menu choice from user"""
        return input("Enter choice: ").strip()

class ComplaintView(BaseView):
    """View class for complaint-related displays"""
    
    def display_complaint_list(self, complaints: List[Dict[str, Any]], show_user: bool = False):
        """Display a list of complaints"""
        if not complaints:
            print("No complaints found.")
            return
        
        print("\n=== Complaints ===")
        for complaint in complaints:
            print(f"ID: {complaint['id']}")
            if show_user and 'user_name' in complaint:
                print(f"User: {complaint['user_name']}")
            print(f"Category: {complaint['category']}")
            print(f"Status: {complaint['status']}")
            print(f"Description: {complaint['description']}")
            print(f"Created: {complaint['created_at']}")
            if 'assigned_staff_name' in complaint and complaint['assigned_staff_name']:
                print(f"Assigned to: {complaint['assigned_staff_name']}")
            print("-" * 50)
    
    def display_complaint_details(self, complaint: Dict[str, Any], comments: List[Dict[str, Any]] = None):
        """Display detailed complaint information"""
        if not complaint:
            print("Complaint not found.")
            return
        
        print("\n=== Complaint Details ===")
        print(f"ID: {complaint['id']}")
        print(f"User: {complaint.get('user_name', 'N/A')}")
        print(f"Category: {complaint['category']}")
        print(f"Status: {complaint['status']}")
        print(f"Description: {complaint['description']}")
        print(f"Created At: {complaint['created_at']}")
        
        if complaint.get('assigned_staff_name'):
            print(f"Assigned To: {complaint['assigned_staff_name']}")
        
        # Display comments if provided
        if comments:
            print("\n=== Comments ===")
            for comment in comments:
                print(f"[{comment['created_at']}] {comment['staff_name']}: {comment['comment']}")
    
    def display_complaint_statistics(self, stats: Dict[str, int]):
        """Display complaint statistics"""
        print("\n=== Complaint Statistics ===")
        print(f"Total: {stats['total']}")
        print(f"Pending: {stats['pending']}")
        print(f"In Progress: {stats['in_progress']}")
        print(f"Resolved: {stats['resolved']}")
    
    def export_complaints_to_csv(self, complaints: List[Dict[str, Any]], filename: str = "complaints_export.csv"):
        """Export complaints to CSV file"""
        try:
            with open(filename, "w", newline='', encoding='utf-8') as csvfile:
                fieldnames = ["id", "user_id", "category", "description", "status", "created_at"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for complaint in complaints:
                    writer.writerow({k: str(complaint.get(k, "")) for k in fieldnames})
            
            print(f"Complaints exported to {filename}")
            return True
        except Exception as e:
            print(f"Error exporting complaints: {e}")
            return False
    
    def get_complaint_input(self) -> Dict[str, str]:
        """Get complaint input from user"""
        category = input("Complaint Category: ").strip()
        description = input("Description: ").strip()
        return {"category": category, "description": description}
    
    def get_status_input(self) -> str:
        """Get status input from user"""
        return input("Enter new status (Pending/In Progress/Resolved): ").strip()
    
    def get_comment_input(self) -> str:
        """Get comment input from user"""
        return input("Enter your comment: ").strip()
    
    def get_search_category(self) -> str:
        """Get category for searching"""
        return input("Enter category to search: ").strip()
    
    def get_filter_status(self) -> str:
        """Get status for filtering"""
        return input("Enter status to filter (Pending/In Progress/Resolved): ").strip()
