from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class BaseDAO(ABC):
    """Abstract base class for Data Access Objects"""

    @abstractmethod
    def create(self, entity_data: Dict[str, Any]) -> bool:
        """Create a new entity"""
        pass

    @abstractmethod
    def find_by_id(self, entity_id: int) -> Optional[Dict[str, Any]]:
        """Find entity by ID"""
        pass

    @abstractmethod
    def find_all(self) -> List[Dict[str, Any]]:
        """Find all entities"""
        pass

    @abstractmethod
    def update(self, entity_id: int, entity_data: Dict[str, Any]) -> bool:
        """Update an entity"""
        pass

    @abstractmethod
    def delete(self, entity_id: int) -> bool:
        """Delete an entity"""
        pass
