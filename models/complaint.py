from datetime import datetime
from typing import Any, Dict, List, Optional

from config.database import db_config
from models.user import User


class Complaint:
    """Complaint model for handling complaint-related database operations"""

    def __init__(self):
        self.db = db_config
        self.user_model = User()

    def create(self, user_id: int, category: str, description: str) -> bool:
        """Create a new complaint"""
        try:
            query = """
                INSERT INTO complaints (user_id, category, description, status) 
                VALUES (?, ?, ?, 'Pending')
            """
            self.db.execute_non_query(query, (user_id, category, description))
            return True
        except Exception as e:
            print(f"Error creating complaint: {e}")
            return False

    def find_by_user_id(self, user_id: int) -> List[Dict[str, Any]]:
        """Get all complaints for a specific user"""
        try:
            query = """
                SELECT id, category, description, status, created_at, assigned_to 
                FROM complaints 
                WHERE user_id = ? 
                ORDER BY created_at DESC
            """
            results = self.db.execute_query(query, (user_id,))

            complaints = []
            for row in results:
                complaint = {
                    "id": row[0],
                    "category": row[1],
                    "description": row[2],
                    "status": row[3],
                    "created_at": row[4],
                    "assigned_to": row[5],
                }
                complaints.append(complaint)
            return complaints
        except Exception as e:
            print(f"Error finding user complaints: {e}")
            return []

    def find_all(self) -> List[Dict[str, Any]]:
        """Get all complaints with user information"""
        try:
            query = """
                SELECT c.id, c.category, c.description, c.status, c.created_at, 
                       c.user_id, u.name as user_name, c.assigned_to
                FROM complaints c
                JOIN users u ON c.user_id = u.id
                ORDER BY c.created_at DESC
            """
            results = self.db.execute_query(query)

            complaints = []
            for row in results:
                complaint = {
                    "id": row[0],
                    "category": row[1],
                    "description": row[2],
                    "status": row[3],
                    "created_at": row[4],
                    "user_id": row[5],
                    "user_name": row[6],
                    "assigned_to": row[7],
                }
                complaints.append(complaint)
            return complaints
        except Exception as e:
            print(f"Error finding all complaints: {e}")
            return []

    def find_by_id(self, complaint_id: int) -> Optional[Dict[str, Any]]:
        """Get complaint by ID with user information"""
        try:
            query = """
                SELECT c.id, c.category, c.description, c.status, c.created_at, 
                       c.user_id, u.name as user_name, c.assigned_to
                FROM complaints c
                JOIN users u ON c.user_id = u.id
                WHERE c.id = ?
            """
            results = self.db.execute_query(query, (complaint_id,))

            if results:
                row = results[0]
                complaint = {
                    "id": row[0],
                    "category": row[1],
                    "description": row[2],
                    "status": row[3],
                    "created_at": row[4],
                    "user_id": row[5],
                    "user_name": row[6],
                    "assigned_to": row[7],
                }

                # Get assigned staff name if available
                if complaint["assigned_to"]:
                    staff = self.user_model.find_by_id(complaint["assigned_to"])
                    complaint["assigned_staff_name"] = staff["name"] if staff else None

                return complaint
            return None
        except Exception as e:
            print(f"Error finding complaint: {e}")
            return None

    def update_status(self, complaint_id: int, status: str) -> bool:
        """Update complaint status"""
        try:
            query = "UPDATE complaints SET status = ? WHERE id = ?"
            affected_rows = self.db.execute_non_query(query, (status, complaint_id))
            return affected_rows > 0
        except Exception as e:
            print(f"Error updating complaint status: {e}")
            return False

    def assign_to_staff(self, complaint_id: int, staff_id: int) -> bool:
        """Assign complaint to staff member"""
        try:
            query = "UPDATE complaints SET assigned_to = ? WHERE id = ?"
            affected_rows = self.db.execute_non_query(query, (staff_id, complaint_id))
            return affected_rows > 0
        except Exception as e:
            print(f"Error assigning complaint: {e}")
            return False

    def find_assigned_complaints(self, staff_id: int) -> List[Dict[str, Any]]:
        """Get complaints assigned to a specific staff member"""
        try:
            query = """
                SELECT c.id, c.category, c.description, c.status, c.created_at,
                       c.user_id, u.name as user_name
                FROM complaints c
                JOIN users u ON c.user_id = u.id
                WHERE c.assigned_to = ?
                ORDER BY c.created_at DESC
            """
            results = self.db.execute_query(query, (staff_id,))

            complaints = []
            for row in results:
                complaint = {
                    "id": row[0],
                    "category": row[1],
                    "description": row[2],
                    "status": row[3],
                    "created_at": row[4],
                    "user_id": row[5],
                    "user_name": row[6],
                }
                complaints.append(complaint)
            return complaints
        except Exception as e:
            print(f"Error finding assigned complaints: {e}")
            return []

    def update_assigned_complaint_status(
        self, staff_id: int, complaint_id: int, status: str
    ) -> bool:
        """Update status of complaint assigned to specific staff"""
        try:
            query = """
                UPDATE complaints 
                SET status = ? 
                WHERE id = ? AND assigned_to = ?
            """
            affected_rows = self.db.execute_non_query(
                query, (status, complaint_id, staff_id)
            )
            return affected_rows > 0
        except Exception as e:
            print(f"Error updating assigned complaint status: {e}")
            return False

    def delete(
        self, complaint_id: int, user_id: int = None, is_admin: bool = False
    ) -> bool:
        """Delete a complaint"""
        try:
            if is_admin:
                query = "DELETE FROM complaints WHERE id = ?"
                params = (complaint_id,)
            else:
                query = "DELETE FROM complaints WHERE id = ? AND user_id = ?"
                params = (complaint_id, user_id)

            affected_rows = self.db.execute_non_query(query, params)
            return affected_rows > 0
        except Exception as e:
            print(f"Error deleting complaint: {e}")
            return False

    def search_by_category(
        self, category: str, user_id: int = None, is_admin: bool = False
    ) -> List[Dict[str, Any]]:
        """Search complaints by category"""
        try:
            if is_admin:
                query = """
                    SELECT c.id, c.category, c.description, c.status, c.created_at,
                           u.name as user_name
                    FROM complaints c
                    JOIN users u ON c.user_id = u.id
                    WHERE c.category LIKE ?
                    ORDER BY c.created_at DESC
                """
                params = (f"%{category}%",)
            else:
                query = """
                    SELECT id, category, description, status, created_at
                    FROM complaints
                    WHERE user_id = ? AND category LIKE ?
                    ORDER BY created_at DESC
                """
                params = (user_id, f"%{category}%")

            results = self.db.execute_query(query, params)

            complaints = []
            for row in results:
                if is_admin:
                    complaint = {
                        "id": row[0],
                        "category": row[1],
                        "description": row[2],
                        "status": row[3],
                        "created_at": row[4],
                        "user_name": row[5],
                    }
                else:
                    complaint = {
                        "id": row[0],
                        "category": row[1],
                        "description": row[2],
                        "status": row[3],
                        "created_at": row[4],
                    }
                complaints.append(complaint)
            return complaints
        except Exception as e:
            print(f"Error searching complaints by category: {e}")
            return []

    def find_by_status(self, status: str) -> List[Dict[str, Any]]:
        """Get complaints by status"""
        try:
            query = """
                SELECT c.id, c.category, c.description, c.status, c.created_at,
                       u.name as user_name
                FROM complaints c
                JOIN users u ON c.user_id = u.id
                WHERE c.status = ?
                ORDER BY c.created_at DESC
            """
            results = self.db.execute_query(query, (status,))

            complaints = []
            for row in results:
                complaint = {
                    "id": row[0],
                    "category": row[1],
                    "description": row[2],
                    "status": row[3],
                    "created_at": row[4],
                    "user_name": row[5],
                }
                complaints.append(complaint)
            return complaints
        except Exception as e:
            print(f"Error finding complaints by status: {e}")
            return []

    def get_statistics(self) -> Dict[str, int]:
        """Get complaint statistics"""
        try:
            stats = {}

            # Total complaints
            query = "SELECT COUNT(*) FROM complaints"
            result = self.db.execute_query(query)
            stats["total"] = result[0][0] if result else 0

            # Pending complaints
            query = "SELECT COUNT(*) FROM complaints WHERE status = 'Pending'"
            result = self.db.execute_query(query)
            stats["pending"] = result[0][0] if result else 0

            # In Progress complaints
            query = "SELECT COUNT(*) FROM complaints WHERE status = 'In Progress'"
            result = self.db.execute_query(query)
            stats["in_progress"] = result[0][0] if result else 0

            # Resolved complaints
            query = "SELECT COUNT(*) FROM complaints WHERE status = 'Resolved'"
            result = self.db.execute_query(query)
            stats["resolved"] = result[0][0] if result else 0

            return stats
        except Exception as e:
            print(f"Error getting complaint statistics: {e}")
            return {"total": 0, "pending": 0, "in_progress": 0, "resolved": 0}

    def export_to_list(
        self, user_id: int = None, is_admin: bool = False
    ) -> List[Dict[str, Any]]:
        """Export complaints to a list for CSV generation"""
        try:
            if is_admin:
                query = """
                    SELECT c.id, c.user_id, c.category, c.description, c.status, c.created_at
                    FROM complaints c
                    ORDER BY c.created_at DESC
                """
                params = None
            else:
                query = """
                    SELECT id, user_id, category, description, status, created_at
                    FROM complaints
                    WHERE user_id = ?
                    ORDER BY created_at DESC
                """
                params = (user_id,)

            results = self.db.execute_query(query, params)

            complaints = []
            for row in results:
                complaint = {
                    "id": str(row[0]),
                    "user_id": str(row[1]),
                    "category": row[2],
                    "description": row[3],
                    "status": row[4],
                    "created_at": str(row[5]),
                }
                complaints.append(complaint)
            return complaints
        except Exception as e:
            print(f"Error exporting complaints: {e}")
            return []
