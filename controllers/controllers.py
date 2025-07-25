from services.user_service import UserService
from services.complaint_service import ComplaintService
from services.comment_service import CommentService
from views.views import UserView, ComplaintView

class UserController:
    """Controller for user-related operations"""
    
    def __init__(self):
        self.user_service = UserService()
        self.user_view = UserView()
    
    def register(self):
        """Handle user registration"""
        try:
            name = self.user_view.get_user_input("Name")
            email = self.user_view.get_user_input("Email")
            password = self.user_view.get_user_input("Password")
            role = self.user_view.get_user_input("Role (user/admin/staff)") or 'user'
            
            if not all([name, email, password]):
                self.user_view.display_error("All fields are required")
                return False
            
            # Check if user already exists
            existing_user = self.user_service.find_user_by_email(email)
            if existing_user:
                self.user_view.display_error("User with this email already exists")
                return False
            
            if self.user_service.create_user(name, email, password, role):
                self.user_view.display_success("User registered successfully")
                return True
            else:
                self.user_view.display_error("Failed to register user")
                return False
        except Exception as e:
            self.user_view.display_error(f"Registration error: {e}")
            return False
    
    def login(self):
        """Handle user login"""
        try:
            email = self.user_view.get_user_input("Email")
            password = self.user_view.get_user_input("Password")
            
            if not all([email, password]):
                self.user_view.display_error("Email and password are required")
                return None
            
            user = self.user_service.authenticate_user(email, password)
            if user:
                self.user_view.display_success(f"Welcome {user['name']} ({user['role']})")
                return user
            else:
                self.user_view.display_error("Invalid credentials")
                return None
        except Exception as e:
            self.user_view.display_error(f"Login error: {e}")
            return None
    
    def change_password(self, user_id: int):
        """Handle password change"""
        try:
            old_password = self.user_view.get_user_input("Old Password")
            new_password = self.user_view.get_user_input("New Password")
            
            if not all([old_password, new_password]):
                self.user_view.display_error("Both passwords are required")
                return False
            
            # First verify old password by getting user and checking authentication
            user = self.user_service.find_user_by_id(user_id)
            if user and self.user_service.authenticate_user(user['email'], old_password):
                if self.user_service.update_password(user_id, new_password):
                    self.user_view.display_success("Password updated successfully")
                    return True
                else:
                    self.user_view.display_error("Failed to update password")
                    return False
            else:
                self.user_view.display_error("Old password is incorrect")
                return False
        except Exception as e:
            self.user_view.display_error(f"Password change error: {e}")
            return False
    
    def list_staff(self):
        """List all staff members"""
        try:
            staff_members = self.user_service.find_users_by_role('staff')
            self.user_view.display_staff_list(staff_members)
            return staff_members
        except Exception as e:
            self.user_view.display_error(f"Error listing staff: {e}")
            return []

class ComplaintController:
    """Controller for complaint-related operations"""
    
    def __init__(self):
        self.complaint_service = ComplaintService()
        self.comment_service = CommentService()
        self.user_service = UserService()
        self.complaint_view = ComplaintView()
    
    def register_complaint(self, user_id: int):
        """Handle complaint registration"""
        try:
            complaint_data = self.complaint_view.get_complaint_input()
            
            if not all([complaint_data['category'], complaint_data['description']]):
                self.complaint_view.display_error("Category and description are required")
                return False
            
            if self.complaint_service.create_complaint(user_id, complaint_data['category'], complaint_data['description']):
                self.complaint_view.display_success("Complaint registered successfully")
                return True
            else:
                self.complaint_view.display_error("Failed to register complaint")
                return False
        except Exception as e:
            self.complaint_view.display_error(f"Registration error: {e}")
            return False
    
    def view_user_complaints(self, user_id: int):
        """View complaints for a specific user"""
        try:
            complaints = self.complaint_service.find_complaints_by_user_id(user_id)
            self.complaint_view.display_complaint_list(complaints)
            return complaints
        except Exception as e:
            self.complaint_view.display_error(f"Error viewing complaints: {e}")
            return []
    
    def view_all_complaints(self):
        """View all complaints (admin function)"""
        try:
            complaints = self.complaint_service.find_all_complaints()
            self.complaint_view.display_complaint_list(complaints, show_user=True)
            return complaints
        except Exception as e:
            self.complaint_view.display_error(f"Error viewing all complaints: {e}")
            return []
    
    def view_complaint_details(self, complaint_id: int):
        """View detailed complaint information"""
        try:
            complaint = self.complaint_service.find_complaint_by_id(complaint_id)
            comments = self.comment_service.find_comments_by_complaint_id(complaint_id)
            self.complaint_view.display_complaint_details(complaint, comments)
            return complaint
        except Exception as e:
            self.complaint_view.display_error(f"Error viewing complaint details: {e}")
            return None
    
    def update_complaint_status(self, complaint_id: int):
        """Update complaint status (admin function)"""
        try:
            status = self.complaint_view.get_status_input()
            
            if status not in ['Pending', 'In Progress', 'Resolved']:
                self.complaint_view.display_error("Invalid status")
                return False
            
            if self.complaint_service.update_complaint_status(complaint_id, status):
                self.complaint_view.display_success("Complaint status updated")
                return True
            else:
                self.complaint_view.display_error("Failed to update complaint status")
                return False
        except Exception as e:
            self.complaint_view.display_error(f"Status update error: {e}")
            return False
    
    def assign_complaint(self, complaint_id: int):
        """Assign complaint to staff member"""
        try:
            staff_email = self.complaint_view.get_user_input("Enter staff email to assign")
            staff = self.user_service.find_user_by_email(staff_email)
            
            if not staff or staff['role'] != 'staff':
                self.complaint_view.display_error("Staff member not found")
                return False
            
            if self.complaint_service.assign_complaint(complaint_id, staff['id']):
                self.complaint_view.display_success("Complaint assigned to staff")
                return True
            else:
                self.complaint_view.display_error("Failed to assign complaint")
                return False
        except Exception as e:
            self.complaint_view.display_error(f"Assignment error: {e}")
            return False
    
    def view_assigned_complaints(self, staff_id: int):
        """View complaints assigned to staff member"""
        try:
            complaints = self.complaint_service.find_assigned_complaints(staff_id)
            self.complaint_view.display_complaint_list(complaints, show_user=True)
            return complaints
        except Exception as e:
            self.complaint_view.display_error(f"Error viewing assigned complaints: {e}")
            return []
    
    def update_assigned_complaint_status(self, staff_id: int, complaint_id: int):
        """Update status of assigned complaint"""
        try:
            status = self.complaint_view.get_status_input()
            
            if status not in ['Pending', 'In Progress', 'Resolved']:
                self.complaint_view.display_error("Invalid status")
                return False
            
            if self.complaint_service.update_complaint_status(complaint_id, status):
                self.complaint_view.display_success("Complaint status updated")
                return True
            else:
                self.complaint_view.display_error("Complaint not found or not assigned to you")
                return False
        except Exception as e:
            self.complaint_view.display_error(f"Status update error: {e}")
            return False
    
    def delete_complaint(self, complaint_id: int, user_id: int = None, is_admin: bool = False):
        """Delete a complaint"""
        try:
            if self.complaint_service.delete_complaint(complaint_id):
                self.complaint_view.display_success("Complaint deleted successfully")
                return True
            else:
                self.complaint_view.display_error("Complaint not found or you do not have permission")
                return False
        except Exception as e:
            self.complaint_view.display_error(f"Deletion error: {e}")
            return False
    
    def search_complaints_by_category(self, user_id: int = None, is_admin: bool = False):
        """Search complaints by category"""
        try:
            category = self.complaint_view.get_search_category()
            if is_admin:
                complaints = self.complaint_service.find_complaints_by_category(category)
            else:
                complaints = self.complaint_service.find_complaints_by_user_and_category(user_id, category)
            self.complaint_view.display_complaint_list(complaints, show_user=is_admin)
            return complaints
        except Exception as e:
            self.complaint_view.display_error(f"Search error: {e}")
            return []
    
    def view_complaints_by_status(self):
        """View complaints by status"""
        try:
            status = self.complaint_view.get_filter_status()
            complaints = self.complaint_service.find_complaints_by_status(status)
            self.complaint_view.display_complaint_list(complaints, show_user=True)
            return complaints
        except Exception as e:
            self.complaint_view.display_error(f"Filter error: {e}")
            return []
    
    def export_complaints_to_csv(self, user_id: int = None, is_admin: bool = False, filename: str = "complaints_export.csv"):
        """Export complaints to CSV"""
        try:
            if is_admin:
                complaints = self.complaint_service.find_all_complaints()
            else:
                complaints = self.complaint_service.find_complaints_by_user_id(user_id)
            if self.complaint_view.export_complaints_to_csv(complaints, filename):
                return True
            return False
        except Exception as e:
            self.complaint_view.display_error(f"Export error: {e}")
            return False
    
    def view_complaint_statistics(self):
        """View complaint statistics"""
        try:
            stats = self.complaint_service.get_statistics()
            self.complaint_view.display_complaint_statistics(stats)
            return stats
        except Exception as e:
            self.complaint_view.display_error(f"Statistics error: {e}")
            return None
    
    def add_comment_to_complaint(self, staff_id: int, complaint_id: int):
        """Add comment to complaint"""
        try:
            comment = self.complaint_view.get_comment_input()
            
            if not comment:
                self.complaint_view.display_error("Comment cannot be empty")
                return False
            
            if self.comment_service.create_comment(complaint_id, staff_id, comment):
                self.complaint_view.display_success("Comment added to complaint")
                return True
            else:
                self.complaint_view.display_error("Failed to add comment or complaint not assigned to you")
                return False
        except Exception as e:
            self.complaint_view.display_error(f"Comment error: {e}")
            return False
