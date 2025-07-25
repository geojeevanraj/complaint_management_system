from typing import Any, Dict, List, Optional

from config.database import db_config
from dao.complaint_dao import ComplaintDAO
from dto.complaint_dto import ComplaintDTO


class ComplaintDAOImpl(ComplaintDAO):
    """Concrete implementation of ComplaintDAO"""

    def __init__(self):
        self.db = db_config

    def create(self, entity_data: Dict[str, Any]) -> bool:
        """Create a new complaint"""
        try:
            complaint_dto = ComplaintDTO.from_dict(entity_data)
            query = """
                INSERT INTO complaints (user_id, category, description, status)
                VALUES (?, ?, ?, ?)
            """
            self.db.execute_non_query(
                query,
                (
                    complaint_dto.user_id,
                    complaint_dto.category,
                    complaint_dto.description,
                    complaint_dto.status,
                ),
            )
            return True
        except Exception as e:
            print(f"Error creating complaint: {e}")
            return False

    def find_by_id(self, entity_id: int) -> Optional[Dict[str, Any]]:
        """Find complaint by ID with user information"""
        try:
            query = """
                SELECT c.id, c.category, c.description, c.status, c.created_at,
                       c.user_id, u.name as user_name, c.assigned_to
                FROM complaints c
                JOIN users u ON c.user_id = u.id
                WHERE c.id = ?
            """
            results = self.db.execute_query(query, (entity_id,))

            if results:
                row = results[0]
                complaint_dto = ComplaintDTO(
                    id=row[0],
                    category=row[1],
                    description=row[2],
                    status=row[3],
                    created_at=row[4],
                    user_id=row[5],
                    user_name=row[6],
                    assigned_to=row[7],
                )
                return complaint_dto.to_dict()
            return None
        except Exception as e:
            print(f"Error finding complaint by ID: {e}")
            return None

    def find_all(self) -> List[Dict[str, Any]]:
        """Find all complaints with user information"""
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
                complaint_dto = ComplaintDTO(
                    id=row[0],
                    category=row[1],
                    description=row[2],
                    status=row[3],
                    created_at=row[4],
                    user_id=row[5],
                    user_name=row[6],
                    assigned_to=row[7],
                )
                complaints.append(complaint_dto.to_dict())
            return complaints
        except Exception as e:
            print(f"Error finding all complaints: {e}")
            return []

    def update(self, entity_id: int, entity_data: Dict[str, Any]) -> bool:
        """Update a complaint"""
        try:
            complaint_dto = ComplaintDTO.from_dict(entity_data)
            query = """
                UPDATE complaints
                SET category = ?, description = ?, status = ?, assigned_to = ?
                WHERE id = ?
            """
            self.db.execute_non_query(
                query,
                (
                    complaint_dto.category,
                    complaint_dto.description,
                    complaint_dto.status,
                    complaint_dto.assigned_to,
                    entity_id,
                ),
            )
            return True
        except Exception as e:
            print(f"Error updating complaint: {e}")
            return False

    def delete(self, entity_id: int) -> bool:
        """Delete a complaint"""
        try:
            query = "DELETE FROM complaints WHERE id = ?"
            self.db.execute_non_query(query, (entity_id,))
            return True
        except Exception as e:
            print(f"Error deleting complaint: {e}")
            return False

    def find_by_user_id(self, user_id: int) -> List[dict]:
        """Find complaints by user ID"""
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
                complaint_dto = ComplaintDTO(
                    id=row[0],
                    user_id=user_id,
                    category=row[1],
                    description=row[2],
                    status=row[3],
                    created_at=row[4],
                    assigned_to=row[5],
                )
                complaints.append(complaint_dto.to_dict())
            return complaints
        except Exception as e:
            print(f"Error finding user complaints: {e}")
            return []

    def find_by_status(self, status: str) -> List[dict]:
        """Find complaints by status"""
        try:
            query = """
                SELECT c.id, c.category, c.description, c.status, c.created_at,
                       c.user_id, u.name as user_name, c.assigned_to
                FROM complaints c
                JOIN users u ON c.user_id = u.id
                WHERE c.status = ?
                ORDER BY c.created_at DESC
            """
            results = self.db.execute_query(query, (status,))

            complaints = []
            for row in results:
                complaint_dto = ComplaintDTO(
                    id=row[0],
                    category=row[1],
                    description=row[2],
                    status=row[3],
                    created_at=row[4],
                    user_id=row[5],
                    user_name=row[6],
                    assigned_to=row[7],
                )
                complaints.append(complaint_dto.to_dict())
            return complaints
        except Exception as e:
            print(f"Error finding complaints by status: {e}")
            return []

    def find_by_category(self, category: str) -> List[dict]:
        """Find complaints by category"""
        try:
            query = """
                SELECT c.id, c.category, c.description, c.status, c.created_at,
                       c.user_id, u.name as user_name, c.assigned_to
                FROM complaints c
                JOIN users u ON c.user_id = u.id
                WHERE c.category = ?
                ORDER BY c.created_at DESC
            """
            results = self.db.execute_query(query, (category,))

            complaints = []
            for row in results:
                complaint_dto = ComplaintDTO(
                    id=row[0],
                    category=row[1],
                    description=row[2],
                    status=row[3],
                    created_at=row[4],
                    user_id=row[5],
                    user_name=row[6],
                    assigned_to=row[7],
                )
                complaints.append(complaint_dto.to_dict())
            return complaints
        except Exception as e:
            print(f"Error finding complaints by category: {e}")
            return []

    def assign_complaint(self, complaint_id: int, staff_id: int) -> bool:
        """Assign complaint to staff member"""
        try:
            query = "UPDATE complaints SET assigned_to = ? WHERE id = ?"
            self.db.execute_non_query(query, (staff_id, complaint_id))
            return True
        except Exception as e:
            print(f"Error assigning complaint: {e}")
            return False

    def update_status(self, complaint_id: int, status: str) -> bool:
        """Update complaint status"""
        try:
            query = "UPDATE complaints SET status = ? WHERE id = ?"
            self.db.execute_non_query(query, (status, complaint_id))
            return True
        except Exception as e:
            print(f"Error updating complaint status: {e}")
            return False

    def find_by_user_and_category(self, user_id: int, category: str) -> List[dict]:
        """Find complaints by user ID and category"""
        try:
            query = """
                SELECT id, category, description, status, created_at, assigned_to
                FROM complaints
                WHERE user_id = ? AND category = ?
                ORDER BY created_at DESC
            """
            results = self.db.execute_query(query, (user_id, category))

            complaints = []
            for row in results:
                complaint_dto = ComplaintDTO(
                    id=row[0],
                    user_id=user_id,
                    category=row[1],
                    description=row[2],
                    status=row[3],
                    created_at=row[4],
                    assigned_to=row[5],
                )
                complaints.append(complaint_dto.to_dict())
            return complaints
        except Exception as e:
            print(f"Error finding complaints by user and category: {e}")
            return []
