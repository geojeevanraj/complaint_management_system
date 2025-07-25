from typing import List, Optional, Dict, Any
from dao.dao_factory import dao_factory
from dto.user_dto import UserDTO

class UserService:
    """Service layer for User operations using DAO pattern"""
    
    def __init__(self):
        self.user_dao = dao_factory.get_user_dao()
    
    def create_user(self, name: str, email: str, password: str, role: str = 'user') -> bool:
        """Create a new user"""
        user_data = {
            'name': name,
            'email': email,
            'password': password,
            'role': role
        }
        return self.user_dao.create(user_data)
    
    def authenticate_user(self, email: str, password: str) -> Optional[dict]:
        """Authenticate user login"""
        return self.user_dao.authenticate(email, password)
    
    def find_user_by_id(self, user_id: int) -> Optional[dict]:
        """Find user by ID"""
        return self.user_dao.find_by_id(user_id)
    
    def find_user_by_email(self, email: str) -> Optional[dict]:
        """Find user by email"""
        return self.user_dao.find_by_email(email)
    
    def find_all_users(self) -> List[dict]:
        """Find all users"""
        return self.user_dao.find_all()
    
    def find_users_by_role(self, role: str) -> List[dict]:
        """Find users by role"""
        return self.user_dao.find_by_role(role)
    
    def update_user(self, user_id: int, name: str, email: str, role: str) -> bool:
        """Update user information"""
        user_data = {
            'name': name,
            'email': email,
            'role': role
        }
        return self.user_dao.update(user_id, user_data)
    
    def update_password(self, user_id: int, new_password: str) -> bool:
        """Update user password"""
        return self.user_dao.update_password(user_id, new_password)
    
    def delete_user(self, user_id: int) -> bool:
        """Delete a user"""
        return self.user_dao.delete(user_id)
