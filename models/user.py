import hashlib
from datetime import datetime
from typing import Any, Dict, List, Optional

from config.database import db_config


class BaseModel:
    """Base model class with common database operations"""

    def __init__(self):
        self.db = db_config

    def hash_password(self, password: str) -> str:
        """Hash password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()


class User(BaseModel):
    """User model for handling user-related database operations"""

    def __init__(self):
        super().__init__()

    def create(self, name: str, email: str, password: str, role: str = "user") -> bool:
        """Create a new user"""
        try:
            hashed_password = self.hash_password(password)
            query = """
                INSERT INTO users (name, email, password, role)
                VALUES (?, ?, ?, ?)
            """
            self.db.execute_non_query(query, (name, email, hashed_password, role))
            return True
        except Exception as e:
            print(f"Error creating user: {e}")
            return False

    def authenticate(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate user login"""
        try:
            hashed_password = self.hash_password(password)
            query = "SELECT id, name, email, role FROM users WHERE email = ? AND password = ?"
            results = self.db.execute_query(query, (email, hashed_password))

            if results:
                row = results[0]
                return {"id": row[0], "name": row[1], "email": row[2], "role": row[3]}
            return None
        except Exception as e:
            print(f"Error authenticating user: {e}")
            return None

    def find_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Find user by ID"""
        try:
            query = "SELECT id, name, email, role FROM users WHERE id = ?"
            results = self.db.execute_query(query, (user_id,))

            if results:
                row = results[0]
                return {"id": row[0], "name": row[1], "email": row[2], "role": row[3]}
            return None
        except Exception as e:
            print(f"Error finding user: {e}")
            return None

    def find_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Find user by email"""
        try:
            query = "SELECT id, name, email, role FROM users WHERE email = ?"
            results = self.db.execute_query(query, (email,))

            if results:
                row = results[0]
                return {"id": row[0], "name": row[1], "email": row[2], "role": row[3]}
            return None
        except Exception as e:
            print(f"Error finding user by email: {e}")
            return None

    def get_staff_members(self) -> List[Dict[str, Any]]:
        """Get all staff members"""
        try:
            query = "SELECT id, name, email FROM users WHERE role = 'staff'"
            results = self.db.execute_query(query)

            staff_list = []
            for row in results:
                staff_list.append({"id": row[0], "name": row[1], "email": row[2]})
            return staff_list
        except Exception as e:
            print(f"Error getting staff members: {e}")
            return []

    def update_password(
        self, user_id: int, old_password: str, new_password: str
    ) -> bool:
        """Update user password"""
        try:
            # First verify old password
            query = "SELECT password FROM users WHERE id = ?"
            results = self.db.execute_query(query, (user_id,))

            if not results or results[0][0] != self.hash_password(old_password):
                return False

            # Update with new password
            hashed_new_password = self.hash_password(new_password)
            update_query = "UPDATE users SET password = ? WHERE id = ?"
            self.db.execute_non_query(update_query, (hashed_new_password, user_id))
            return True
        except Exception as e:
            print(f"Error updating password: {e}")
            return False
