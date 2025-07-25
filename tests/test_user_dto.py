# Unit tests for UserDTO
import pytest
from datetime import datetime
from dto.user_dto import UserDTO

class TestUserDTO:
    """Test cases for UserDTO"""
    
    def test_user_dto_creation(self):
        """Test UserDTO creation with all fields"""
        # Arrange
        user_dto = UserDTO(
            id=1,
            name="Test User",
            email="test@example.com",
            password="password123",
            role="user",
            created_at=datetime.now()
        )
        
        # Assert
        assert user_dto.id == 1
        assert user_dto.name == "Test User"
        assert user_dto.email == "test@example.com"
        assert user_dto.password == "password123"
        assert user_dto.role == "user"
        assert isinstance(user_dto.created_at, datetime)
        
    def test_user_dto_default_values(self):
        """Test UserDTO with default values"""
        # Arrange
        user_dto = UserDTO()
        
        # Assert
        assert user_dto.id is None
        assert user_dto.name == ""
        assert user_dto.email == ""
        assert user_dto.password == ""
        assert user_dto.role == "user"
        assert user_dto.created_at is None
        
    def test_user_dto_to_dict(self):
        """Test converting UserDTO to dictionary"""
        # Arrange
        created_at = datetime.now()
        user_dto = UserDTO(
            id=1,
            name="Test User",
            email="test@example.com",
            password="password123",
            role="user",
            created_at=created_at
        )
        
        # Act
        user_dict = user_dto.to_dict()
        
        # Assert
        expected_dict = {
            'id': 1,
            'name': "Test User",
            'email': "test@example.com",
            'password': "password123",
            'role': "user",
            'created_at': created_at
        }
        assert user_dict == expected_dict
        
    def test_user_dto_from_dict(self):
        """Test creating UserDTO from dictionary"""
        # Arrange
        created_at = datetime.now()
        user_data = {
            'id': 1,
            'name': "Test User",
            'email': "test@example.com",
            'password': "password123",
            'role': "user",
            'created_at': created_at
        }
        
        # Act
        user_dto = UserDTO.from_dict(user_data)
        
        # Assert
        assert user_dto.id == 1
        assert user_dto.name == "Test User"
        assert user_dto.email == "test@example.com"
        assert user_dto.password == "password123"
        assert user_dto.role == "user"
        assert user_dto.created_at == created_at
        
    def test_user_dto_from_dict_partial(self):
        """Test creating UserDTO from partial dictionary"""
        # Arrange
        user_data = {
            'name': "Test User",
            'email': "test@example.com"
        }
        
        # Act
        user_dto = UserDTO.from_dict(user_data)
        
        # Assert
        assert user_dto.id is None
        assert user_dto.name == "Test User"
        assert user_dto.email == "test@example.com"
        assert user_dto.password == ""
        assert user_dto.role == "user"  # Default value
        assert user_dto.created_at is None
        
    def test_user_dto_from_dict_empty(self):
        """Test creating UserDTO from empty dictionary"""
        # Arrange
        user_data = {}
        
        # Act
        user_dto = UserDTO.from_dict(user_data)
        
        # Assert
        assert user_dto.id is None
        assert user_dto.name == ""
        assert user_dto.email == ""
        assert user_dto.password == ""
        assert user_dto.role == "user"
        assert user_dto.created_at is None
