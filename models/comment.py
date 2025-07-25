from datetime import datetime
from typing import Any, Dict, List, Optional

from config.database import db_config


class Comment:
    """Comment model for handling complaint comments"""

    def __init__(self):
        self.db = db_config

    def create(self, complaint_id: int, staff_id: int, comment: str) -> bool:
        """Add a comment to a complaint"""
        try:
            # First check if the complaint is assigned to this staff member
            check_query = "SELECT id FROM complaints WHERE id = ? AND assigned_to = ?"
            results = self.db.execute_query(check_query, (complaint_id, staff_id))

            if not results:
                return False

            # Add the comment
            query = """
                INSERT INTO complaint_comments (complaint_id, staff_id, comment) 
                VALUES (?, ?, ?)
            """
            self.db.execute_non_query(query, (complaint_id, staff_id, comment))
            return True
        except Exception as e:
            print(f"Error creating comment: {e}")
            return False

    def find_by_complaint_id(self, complaint_id: int) -> List[Dict[str, Any]]:
        """Get all comments for a specific complaint"""
        try:
            query = """
                SELECT cc.id, cc.comment, cc.created_at, u.name as staff_name
                FROM complaint_comments cc
                JOIN users u ON cc.staff_id = u.id
                WHERE cc.complaint_id = ?
                ORDER BY cc.created_at ASC
            """
            results = self.db.execute_query(query, (complaint_id,))

            comments = []
            for row in results:
                comment = {
                    "id": row[0],
                    "comment": row[1],
                    "created_at": row[2],
                    "staff_name": row[3],
                }
                comments.append(comment)
            return comments
        except Exception as e:
            print(f"Error finding comments: {e}")
            return []
