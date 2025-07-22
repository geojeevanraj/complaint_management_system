"""
Query Users - Simple script to view all users in the database
"""

import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def view_all_users():
    """Display all users in the database"""
    try:
        from config.database import db_config
        
        print("=" * 60)
        print("ALL USERS IN THE DATABASE")
        print("=" * 60)
        
        # SQL command to see all users
        query = "SELECT id, name, email, role, created_at FROM users ORDER BY id"
        
        print(f"Executing SQL: {query}")
        print("-" * 60)
        
        results = db_config.execute_query(query)
        
        if not results:
            print("No users found in the database.")
            print("\nTo create users, you can:")
            print("1. Run: python create_demo_data.py")
            print("2. Or register users through the application: python app.py")
        else:
            print(f"Found {len(results)} user(s):")
            print()
            print(f"{'ID':<5} {'Name':<20} {'Email':<30} {'Role':<10} {'Created At':<20}")
            print("-" * 85)
            
            for row in results:
                user_id = row[0]
                name = row[1]
                email = row[2]
                role = row[3]
                created_at = str(row[4]) if row[4] else 'N/A'
                
                print(f"{user_id:<5} {name:<20} {email:<30} {role:<10} {created_at:<20}")
        
        print("\n" + "=" * 60)
        
    except Exception as e:
        print(f"Error querying users: {e}")
        print("\nMake sure:")
        print("1. MySQL server is running")
        print("2. Database 'complaint_system' exists")
        print("3. Tables are created")
        print("\nYou can run: python setup_mysql_database.py")

def show_sql_commands():
    """Show common SQL commands for user management"""
    print("\n" + "=" * 60)
    print("USEFUL SQL COMMANDS FOR USER MANAGEMENT")
    print("=" * 60)
    
    commands = [
        ("View all users:", "SELECT * FROM users;"),
        ("View specific user by email:", "SELECT * FROM users WHERE email = 'user@example.com';"),
        ("View users by role:", "SELECT * FROM users WHERE role = 'admin';"),
        ("Count users by role:", "SELECT role, COUNT(*) FROM users GROUP BY role;"),
        ("View recently created users:", "SELECT * FROM users ORDER BY created_at DESC LIMIT 10;"),
        ("Update user role:", "UPDATE users SET role = 'staff' WHERE email = 'user@example.com';"),
        ("Delete user:", "DELETE FROM users WHERE email = 'user@example.com';"),
    ]
    
    for description, command in commands:
        print(f"\n{description}")
        print(f"  {command}")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    view_all_users()
    show_sql_commands()
