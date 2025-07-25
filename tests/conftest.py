# Test configuration for pytest
import os
import sys
from unittest.mock import Mock

import pytest

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture
def mock_db_config():
    """Mock database configuration for testing"""
    mock_db = Mock()
    mock_db.execute_query.return_value = []
    mock_db.execute_non_query.return_value = True
    return mock_db


@pytest.fixture
def sample_user_data():
    """Sample user data for testing"""
    return {
        "id": 1,
        "name": "Test User",
        "email": "test@example.com",
        "role": "user",
        "created_at": "2025-07-23 10:00:00",
    }


@pytest.fixture
def sample_complaint_data():
    """Sample complaint data for testing"""
    return {
        "id": 1,
        "user_id": 1,
        "category": "Technical Issue",
        "description": "Login not working",
        "status": "Pending",
        "created_at": "2025-07-23 10:00:00",
        "assigned_to": None,
        "user_name": "Test User",
    }


@pytest.fixture
def sample_comment_data():
    """Sample comment data for testing"""
    return {
        "id": 1,
        "complaint_id": 1,
        "user_id": 2,
        "comment": "Looking into this issue",
        "created_at": "2025-07-23 10:30:00",
        "user_name": "Staff Member",
    }


# Test database configuration
TEST_DB_CONFIG = {
    "host": os.getenv("TEST_DB_HOST", "localhost"),
    "port": os.getenv("TEST_DB_PORT", "3307"),
    "database": os.getenv("TEST_DB_NAME", "complaint_system_test"),
    "user": os.getenv("TEST_DB_USER", "root"),
    "password": os.getenv("TEST_DB_PASSWORD", "test_password"),
}
