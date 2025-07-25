"""
Database Setup Script
Run this script to set up the database tables for the first time
"""

import os
import sys

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.database import db_config


def setup_database():
    """Set up the database tables"""
    try:
        print("Setting up database tables...")
        db_config.create_tables()
        print("Database setup completed successfully!")

        # Test the connection
        print("Testing database connection...")
        conn = db_config.get_connection()
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        print("Created tables:")
        for table in tables:
            print(f"  - {table[0]}")

        cursor.close()
        print("Database connection test successful!")

    except Exception as e:
        print(f"Error setting up database: {e}")
        print("\nPlease check:")
        print("1. MySQL server is running")
        print("2. Database credentials in .env file are correct")
        print("3. MySQL ODBC driver is installed")
        print("4. Database 'complaint_system' exists")
    finally:
        db_config.close_connection()


if __name__ == "__main__":
    setup_database()
