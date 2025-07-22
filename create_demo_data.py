"""
Demo Data Script
Run this script to populate the database with sample data for testing
"""

import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.user import User
from models.complaint import Complaint

def create_demo_data():
    """Create demo users and complaints"""
    try:
        user_model = User()
        complaint_model = Complaint()
        
        print("Creating demo data...")
        
        # Create demo users
        demo_users = [
            ("John Admin", "admin@test.com", "admin123", "admin"),
            ("Jane Staff", "staff@test.com", "staff123", "staff"),
            ("Bob User", "user1@test.com", "user123", "user"),
            ("Alice User", "user2@test.com", "user123", "user"),
            ("Mike Staff", "staff2@test.com", "staff123", "staff")
        ]
        
        user_ids = {}
        for name, email, password, role in demo_users:
            if user_model.create(name, email, password, role):
                user = user_model.find_by_email(email)
                if user:
                    user_ids[email] = user['id']
                print(f"Created {role}: {name} ({email})")
            else:
                print(f"Failed to create user: {name}")
        
        # Create demo complaints
        demo_complaints = [
            ("user1@test.com", "Technical Issue", "My computer is not working properly"),
            ("user1@test.com", "Service Request", "Need help with software installation"),
            ("user2@test.com", "Bug Report", "Found a bug in the application"),
            ("user2@test.com", "Feature Request", "Would like to request a new feature"),
            ("user1@test.com", "Account Issue", "Cannot access my account"),
        ]
        
        for email, category, description in demo_complaints:
            if email in user_ids:
                if complaint_model.create(user_ids[email], category, description):
                    print(f"Created complaint: {category}")
                else:
                    print(f"Failed to create complaint: {category}")
        
        print("\nDemo data created successfully!")
        print("\nYou can now log in with:")
        print("Admin: admin@test.com / admin123")
        print("Staff: staff@test.com / staff123")
        print("User: user1@test.com / user123")
        print("User: user2@test.com / user123")
        
    except Exception as e:
        print(f"Error creating demo data: {e}")

if __name__ == "__main__":
    create_demo_data()
