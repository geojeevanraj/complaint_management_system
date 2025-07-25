from abc import ABC, abstractmethod
from typing import List, Optional

from dao.base_dao import BaseDAO


class UserDAO(BaseDAO):
    """Abstract interface for User data access operations"""

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[dict]:
        """Find user by email"""
        pass

    @abstractmethod
    def authenticate(self, email: str, password: str) -> Optional[dict]:
        """Authenticate user login"""
        pass

    @abstractmethod
    def update_password(self, user_id: int, new_password: str) -> bool:
        """Update user password"""
        pass

    @abstractmethod
    def find_by_role(self, role: str) -> List[dict]:
        """Find users by role"""
        pass
