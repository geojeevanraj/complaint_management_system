from typing import List, Optional, Dict, Any
from dao.comment_dao import CommentDAO
from dto.comment_dto import CommentDTO
from config.database import db_config

class CommentDAOImpl(CommentDAO):
    """Concrete implementation of CommentDAO"""
    
    def __init__(self):
        self.db = db_config
    
    def create(self, entity_data: Dict[str, Any]) -> bool:
        """Create a new comment"""
        try:
            comment_dto = CommentDTO.from_dict(entity_data)
            
            # First check if the complaint is assigned to this user (staff member)
            check_query = "SELECT id FROM complaints WHERE id = ? AND assigned_to = ?"
            results = self.db.execute_query(check_query, (comment_dto.complaint_id, comment_dto.user_id))
            
            if not results:
                return False
            
            # Add the comment
            query = """
                INSERT INTO complaint_comments (complaint_id, staff_id, comment) 
                VALUES (?, ?, ?)
            """
            self.db.execute_non_query(query, (
                comment_dto.complaint_id, 
                comment_dto.user_id, 
                comment_dto.comment
            ))
            return True
        except Exception as e:
            print(f"Error creating comment: {e}")
            return False
    
    def find_by_id(self, entity_id: int) -> Optional[Dict[str, Any]]:
        """Find comment by ID"""
        try:
            query = """
                SELECT cc.id, cc.complaint_id, cc.staff_id, cc.comment, cc.created_at, u.name as staff_name
                FROM complaint_comments cc
                JOIN users u ON cc.staff_id = u.id
                WHERE cc.id = ?
            """
            results = self.db.execute_query(query, (entity_id,))
            
            if results:
                row = results[0]
                comment_dto = CommentDTO(
                    id=row[0],
                    complaint_id=row[1],
                    user_id=row[2],
                    comment=row[3],
                    created_at=row[4],
                    user_name=row[5]
                )
                return comment_dto.to_dict()
            return None
        except Exception as e:
            print(f"Error finding comment by ID: {e}")
            return None
    
    def find_all(self) -> List[Dict[str, Any]]:
        """Find all comments"""
        try:
            query = """
                SELECT cc.id, cc.complaint_id, cc.staff_id, cc.comment, cc.created_at, u.name as staff_name
                FROM complaint_comments cc
                JOIN users u ON cc.staff_id = u.id
                ORDER BY cc.created_at DESC
            """
            results = self.db.execute_query(query)
            
            comments = []
            for row in results:
                comment_dto = CommentDTO(
                    id=row[0],
                    complaint_id=row[1],
                    user_id=row[2],
                    comment=row[3],
                    created_at=row[4],
                    user_name=row[5]
                )
                comments.append(comment_dto.to_dict())
            return comments
        except Exception as e:
            print(f"Error finding all comments: {e}")
            return []
    
    def update(self, entity_id: int, entity_data: Dict[str, Any]) -> bool:
        """Update a comment"""
        try:
            comment_dto = CommentDTO.from_dict(entity_data)
            query = "UPDATE complaint_comments SET comment = ? WHERE id = ?"
            self.db.execute_non_query(query, (comment_dto.comment, entity_id))
            return True
        except Exception as e:
            print(f"Error updating comment: {e}")
            return False
    
    def delete(self, entity_id: int) -> bool:
        """Delete a comment"""
        try:
            query = "DELETE FROM complaint_comments WHERE id = ?"
            self.db.execute_non_query(query, (entity_id,))
            return True
        except Exception as e:
            print(f"Error deleting comment: {e}")
            return False
    
    def find_by_complaint_id(self, complaint_id: int) -> List[dict]:
        """Find comments by complaint ID"""
        try:
            query = """
                SELECT cc.id, cc.complaint_id, cc.staff_id, cc.comment, cc.created_at, u.name as staff_name
                FROM complaint_comments cc
                JOIN users u ON cc.staff_id = u.id
                WHERE cc.complaint_id = ?
                ORDER BY cc.created_at ASC
            """
            results = self.db.execute_query(query, (complaint_id,))
            
            comments = []
            for row in results:
                comment_dto = CommentDTO(
                    id=row[0],
                    complaint_id=row[1],
                    user_id=row[2],
                    comment=row[3],
                    created_at=row[4],
                    user_name=row[5]
                )
                comments.append(comment_dto.to_dict())
            return comments
        except Exception as e:
            print(f"Error finding comments by complaint ID: {e}")
            return []
    
    def find_by_user_id(self, user_id: int) -> List[dict]:
        """Find comments by user ID"""
        try:
            query = """
                SELECT cc.id, cc.complaint_id, cc.staff_id, cc.comment, cc.created_at, u.name as staff_name
                FROM complaint_comments cc
                JOIN users u ON cc.staff_id = u.id
                WHERE cc.staff_id = ?
                ORDER BY cc.created_at DESC
            """
            results = self.db.execute_query(query, (user_id,))
            
            comments = []
            for row in results:
                comment_dto = CommentDTO(
                    id=row[0],
                    complaint_id=row[1],
                    user_id=row[2],
                    comment=row[3],
                    created_at=row[4],
                    user_name=row[5]
                )
                comments.append(comment_dto.to_dict())
            return comments
        except Exception as e:
            print(f"Error finding comments by user ID: {e}")
            return []
