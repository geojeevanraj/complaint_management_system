from typing import List, Optional, Dict, Any
from dao.dao_factory import dao_factory
from dto.comment_dto import CommentDTO

class CommentService:
    """Service layer for Comment operations using DAO pattern"""
    
    def __init__(self):
        self.comment_dao = dao_factory.get_comment_dao()
    
    def create_comment(self, complaint_id: int, staff_id: int, comment: str) -> bool:
        """Create a new comment"""
        comment_data = {
            'complaint_id': complaint_id,
            'user_id': staff_id,  # Using user_id field for staff_id
            'comment': comment
        }
        return self.comment_dao.create(comment_data)
    
    def find_comment_by_id(self, comment_id: int) -> Optional[dict]:
        """Find comment by ID"""
        return self.comment_dao.find_by_id(comment_id)
    
    def find_all_comments(self) -> List[dict]:
        """Find all comments"""
        return self.comment_dao.find_all()
    
    def find_comments_by_complaint_id(self, complaint_id: int) -> List[dict]:
        """Find comments by complaint ID"""
        return self.comment_dao.find_by_complaint_id(complaint_id)
    
    def find_comments_by_user_id(self, user_id: int) -> List[dict]:
        """Find comments by user ID"""
        return self.comment_dao.find_by_user_id(user_id)
    
    def update_comment(self, comment_id: int, comment: str) -> bool:
        """Update comment"""
        comment_data = {
            'comment': comment
        }
        return self.comment_dao.update(comment_id, comment_data)
    
    def delete_comment(self, comment_id: int) -> bool:
        """Delete a comment"""
        return self.comment_dao.delete(comment_id)
