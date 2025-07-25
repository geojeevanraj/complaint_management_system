from abc import ABC, abstractmethod
from typing import List, Optional

from dao.base_dao import BaseDAO


class CommentDAO(BaseDAO):
    """Abstract interface for Comment data access operations"""

    @abstractmethod
    def find_by_complaint_id(self, complaint_id: int) -> List[dict]:
        """Find comments by complaint ID"""
        pass

    @abstractmethod
    def find_by_user_id(self, user_id: int) -> List[dict]:
        """Find comments by user ID"""
        pass
