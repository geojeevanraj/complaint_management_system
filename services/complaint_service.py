from typing import List, Optional, Dict, Any
from dao.dao_factory import dao_factory
from dto.complaint_dto import ComplaintDTO

class ComplaintService:
    """Service layer for Complaint operations using DAO pattern"""
    
    def __init__(self):
        self.complaint_dao = dao_factory.get_complaint_dao()
    
    def create_complaint(self, user_id: int, category: str, description: str) -> bool:
        """Create a new complaint"""
        complaint_data = {
            'user_id': user_id,
            'category': category,
            'description': description,
            'status': 'Pending'
        }
        return self.complaint_dao.create(complaint_data)
    
    def find_complaint_by_id(self, complaint_id: int) -> Optional[dict]:
        """Find complaint by ID"""
        return self.complaint_dao.find_by_id(complaint_id)
    
    def find_all_complaints(self) -> List[dict]:
        """Find all complaints"""
        return self.complaint_dao.find_all()
    
    def find_complaints_by_user_id(self, user_id: int) -> List[dict]:
        """Find complaints by user ID"""
        return self.complaint_dao.find_by_user_id(user_id)
    
    def find_complaints_by_status(self, status: str) -> List[dict]:
        """Find complaints by status"""
        return self.complaint_dao.find_by_status(status)
    
    def find_complaints_by_category(self, category: str) -> List[dict]:
        """Find complaints by category"""
        return self.complaint_dao.find_by_category(category)
    
    def find_complaints_by_user_and_category(self, user_id: int, category: str) -> List[dict]:
        """Find complaints by user ID and category"""
        return self.complaint_dao.find_by_user_and_category(user_id, category)
    
    def update_complaint(self, complaint_id: int, category: str, description: str, status: str, assigned_to: Optional[int] = None) -> bool:
        """Update complaint information"""
        complaint_data = {
            'category': category,
            'description': description,
            'status': status,
            'assigned_to': assigned_to
        }
        return self.complaint_dao.update(complaint_id, complaint_data)
    
    def update_complaint_status(self, complaint_id: int, status: str) -> bool:
        """Update complaint status"""
        return self.complaint_dao.update_status(complaint_id, status)
    
    def assign_complaint(self, complaint_id: int, staff_id: int) -> bool:
        """Assign complaint to staff member"""
        return self.complaint_dao.assign_complaint(complaint_id, staff_id)
    
    def delete_complaint(self, complaint_id: int) -> bool:
        """Delete a complaint"""
        return self.complaint_dao.delete(complaint_id)
    
    def get_statistics(self) -> dict:
        """Get complaint statistics"""
        try:
            all_complaints = self.find_all_complaints()
            
            stats = {
                'total_complaints': len(all_complaints),
                'pending_complaints': len([c for c in all_complaints if c['status'] == 'Pending']),
                'in_progress_complaints': len([c for c in all_complaints if c['status'] == 'In Progress']),
                'resolved_complaints': len([c for c in all_complaints if c['status'] == 'Resolved']),
                'closed_complaints': len([c for c in all_complaints if c['status'] == 'Closed'])
            }
            
            # Add category statistics
            categories = {}
            for complaint in all_complaints:
                category = complaint['category']
                categories[category] = categories.get(category, 0) + 1
            
            stats['category_breakdown'] = categories
            return stats
        except Exception as e:
            print(f"Error getting statistics: {e}")
            return {}
    
    def find_assigned_complaints(self, staff_id: int) -> List[dict]:
        """Find complaints assigned to a specific staff member"""
        try:
            all_complaints = self.find_all_complaints()
            assigned_complaints = [c for c in all_complaints if c.get('assigned_to') == staff_id]
            return assigned_complaints
        except Exception as e:
            print(f"Error finding assigned complaints: {e}")
            return []
    
    def search_by_category(self, category: str, user_id: int = None, is_admin: bool = False) -> List[dict]:
        """Search complaints by category with user filtering"""
        if is_admin or user_id is None:
            return self.find_complaints_by_category(category)
        else:
            return self.find_complaints_by_user_and_category(user_id, category)
    
    def export_to_list(self, user_id: int = None, is_admin: bool = False) -> List[dict]:
        """Export complaints to list format"""
        if is_admin or user_id is None:
            return self.find_all_complaints()
        else:
            return self.find_complaints_by_user_id(user_id)
