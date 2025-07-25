import hashlib
from typing import List, Optional, Dict, Any
from dao.user_dao import UserDAO
from dto.user_dto import UserDTO
from config.database import db_config

class UserDAOImpl(UserDAO):
    """Concrete implementation of UserDAO"""
    
    def __init__(self):
        self.db = db_config
    
    def _hash_password(self, password: str) -> str:
        """Hash password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create(self, entity_data: Dict[str, Any]) -> bool:
        """Create a new user"""
        try:
            user_dto = UserDTO.from_dict(entity_data)
            hashed_password = self._hash_password(user_dto.password)
            
            query = """
                INSERT INTO users (name, email, password, role) 
                VALUES (?, ?, ?, ?)
            """
            self.db.execute_non_query(query, (user_dto.name, user_dto.email, hashed_password, user_dto.role))
            return True
        except Exception as e:
            print(f"Error creating user: {e}")
            return False
    
    def find_by_id(self, entity_id: int) -> Optional[Dict[str, Any]]:
        """Find user by ID"""
        try:
            query = "SELECT id, name, email, role, created_at FROM users WHERE id = ?"
            results = self.db.execute_query(query, (entity_id,))
            
            if results:
                row = results[0]
                user_dto = UserDTO(
                    id=row[0],
                    name=row[1],
                    email=row[2],
                    role=row[3],
                    created_at=row[4]
                )
                return user_dto.to_dict()
            return None
        except Exception as e:
            print(f"Error finding user by ID: {e}")
            return None
    
    def find_all(self) -> List[Dict[str, Any]]:
        """Find all users"""
        try:
            query = "SELECT id, name, email, role, created_at FROM users ORDER BY created_at DESC"
            results = self.db.execute_query(query)
            
            users = []
            for row in results:
                user_dto = UserDTO(
                    id=row[0],
                    name=row[1],
                    email=row[2],
                    role=row[3],
                    created_at=row[4]
                )
                users.append(user_dto.to_dict())
            return users
        except Exception as e:
            print(f"Error finding all users: {e}")
            return []
    
    def update(self, entity_id: int, entity_data: Dict[str, Any]) -> bool:
        """Update a user"""
        try:
            user_dto = UserDTO.from_dict(entity_data)
            query = "UPDATE users SET name = ?, email = ?, role = ? WHERE id = ?"
            self.db.execute_non_query(query, (user_dto.name, user_dto.email, user_dto.role, entity_id))
            return True
        except Exception as e:
            print(f"Error updating user: {e}")
            return False
    
    def delete(self, entity_id: int) -> bool:
        """Delete a user"""
        try:
            query = "DELETE FROM users WHERE id = ?"
            self.db.execute_non_query(query, (entity_id,))
            return True
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False
    
    def find_by_email(self, email: str) -> Optional[dict]:
        """Find user by email"""
        try:
            query = "SELECT id, name, email, role, created_at FROM users WHERE email = ?"
            results = self.db.execute_query(query, (email,))
            
            if results:
                row = results[0]
                user_dto = UserDTO(
                    id=row[0],
                    name=row[1],
                    email=row[2],
                    role=row[3],
                    created_at=row[4]
                )
                return user_dto.to_dict()
            return None
        except Exception as e:
            print(f"Error finding user by email: {e}")
            return None
    
    def authenticate(self, email: str, password: str) -> Optional[dict]:
        """Authenticate user login"""
        try:
            hashed_password = self._hash_password(password)
            query = "SELECT id, name, email, role FROM users WHERE email = ? AND password = ?"
            results = self.db.execute_query(query, (email, hashed_password))
            
            if results:
                row = results[0]
                user_dto = UserDTO(
                    id=row[0],
                    name=row[1],
                    email=row[2],
                    role=row[3]
                )
                return user_dto.to_dict()
            return None
        except Exception as e:
            print(f"Error authenticating user: {e}")
            return None
    
    def update_password(self, user_id: int, new_password: str) -> bool:
        """Update user password"""
        try:
            hashed_password = self._hash_password(new_password)
            query = "UPDATE users SET password = ? WHERE id = ?"
            self.db.execute_non_query(query, (hashed_password, user_id))
            return True
        except Exception as e:
            print(f"Error updating password: {e}")
            return False
    
    def find_by_role(self, role: str) -> List[dict]:
        """Find users by role"""
        try:
            query = "SELECT id, name, email, role, created_at FROM users WHERE role = ? ORDER BY name"
            results = self.db.execute_query(query, (role,))
            
            users = []
            for row in results:
                user_dto = UserDTO(
                    id=row[0],
                    name=row[1],
                    email=row[2],
                    role=row[3],
                    created_at=row[4]
                )
                users.append(user_dto.to_dict())
            return users
        except Exception as e:
            print(f"Error finding users by role: {e}")
            return []
