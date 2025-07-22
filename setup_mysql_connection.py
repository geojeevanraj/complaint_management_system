"""
MySQL Connection Helper
This script helps you set up the MySQL connection with the correct credentials
"""

import getpass
import pyodbc
import os

def test_mysql_connection():
    """Test MySQL connection with user-provided credentials"""
    print("=" * 60)
    print("MySQL Connection Setup Helper")
    print("=" * 60)
    
    # Get connection details
    server = input("MySQL Server (default: localhost): ").strip() or "localhost"
    port = input("MySQL Port (default: 3306): ").strip() or "3306"
    username = input("MySQL Username (default: root): ").strip() or "root"
    password = getpass.getpass("MySQL Password: ")
    
    # Available MySQL drivers
    drivers = pyodbc.drivers()
    mysql_drivers = [d for d in drivers if 'mysql' in d.lower()]
    
    if not mysql_drivers:
        print("❌ No MySQL ODBC drivers found!")
        return False
    
    print(f"\nUsing driver: {mysql_drivers[0]}")
    
    # Test connection (without specifying database)
    connection_string = (
        f"DRIVER={{{mysql_drivers[0]}}};"
        f"SERVER={server};"
        f"PORT={port};"
        f"UID={username};"
        f"PWD={password};"
    )
    
    try:
        print("\nTesting MySQL connection...")
        conn = pyodbc.connect(connection_string)
        print("✅ MySQL connection successful!")
        
        # Check if database exists
        cursor = conn.cursor()
        cursor.execute("SHOW DATABASES LIKE 'complaint_system'")
        result = cursor.fetchone()
        
        if result:
            print("✅ Database 'complaint_system' already exists!")
        else:
            print("⚠️  Database 'complaint_system' does not exist.")
            create_db = input("Would you like to create it? (y/n): ").strip().lower()
            
            if create_db == 'y':
                cursor.execute("CREATE DATABASE complaint_system")
                print("✅ Database 'complaint_system' created successfully!")
        
        cursor.close()
        conn.close()
        
        # Update .env file
        env_content = f"""# Database Configuration for Complaint Management System
DB_SERVER={server}
DB_NAME=complaint_system
DB_USER={username}
DB_PASSWORD={password}
DB_DRIVER={{{mysql_drivers[0]}}}
DB_PORT={port}
"""
        
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print("\n✅ .env file updated with your MySQL credentials!")
        print("\nYou can now run:")
        print("python app.py")
        
        return True
        
    except pyodbc.Error as e:
        print(f"❌ MySQL connection failed: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure MySQL server is running")
        print("2. Check your username and password")
        print("3. Ensure the user has necessary privileges")
        return False

if __name__ == "__main__":
    test_mysql_connection()
