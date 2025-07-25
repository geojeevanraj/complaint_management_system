"""
MySQL Database Setup Script
This script will create the complaint_system database and tables
"""

import os

import pyodbc
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def get_mysql_drivers():
    """Get available MySQL ODBC drivers"""
    drivers = pyodbc.drivers()
    print("All available drivers:")
    for driver in drivers:
        print(f"  - {driver}")

    mysql_drivers = [d for d in drivers if "mysql" in d.lower()]
    print(f"\nMySQL drivers found: {len(mysql_drivers)}")
    for driver in mysql_drivers:
        print(f"  * {driver}")

    return mysql_drivers


def create_database():
    """Create the complaint_system database"""
    # Database connection parameters
    server = os.getenv("DB_SERVER", "localhost")
    username = os.getenv("DB_USER", "root")
    password = os.getenv("DB_PASSWORD", "")
    port = os.getenv("DB_PORT", "3306")

    # Find MySQL driver
    mysql_drivers = get_mysql_drivers()
    if not mysql_drivers:
        print("❌ No MySQL ODBC drivers found!")
        return False

    driver = mysql_drivers[0]  # Use the first available MySQL driver
    print(f"Using driver: {driver}")

    # Connection string without database (to create the database)
    connection_string = (
        f"DRIVER={{{driver}}};"
        f"SERVER={server};"
        f"PORT={port};"
        f"UID={username};"
        f"PWD={password};"
    )

    try:
        print("Connecting to MySQL server...")
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        # Create database
        print("Creating database 'complaint_system'...")
        cursor.execute("CREATE DATABASE IF NOT EXISTS complaint_system")
        conn.commit()

        print("✅ Database 'complaint_system' created successfully!")

        cursor.close()
        conn.close()
        return True

    except pyodbc.Error as e:
        print(f"❌ Error creating database: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure MySQL server is running")
        print("2. Check your MySQL credentials")
        print("3. Ensure you have permission to create databases")
        return False


def create_tables():
    """Create the application tables"""
    # Import after database creation
    import sys

    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    try:
        from config.database import db_config

        print("Creating application tables...")
        db_config.create_tables()
        return True
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False


def main():
    """Main setup function"""
    print("=" * 60)
    print("MySQL Database Setup for Complaint Management System")
    print("=" * 60)

    # Step 1: Create database
    if create_database():
        print("\n" + "=" * 40)
        print("Step 1: Database Creation - ✅ SUCCESS")
        print("=" * 40)

        # Step 2: Create tables
        print("\nStep 2: Creating application tables...")
        if create_tables():
            print("=" * 40)
            print("Step 2: Table Creation - ✅ SUCCESS")
            print("=" * 40)

            print("\n🎉 Database setup completed successfully!")
            print("\nYou can now run the application with:")
            print("python app.py")

        else:
            print("=" * 40)
            print("Step 2: Table Creation - ❌ FAILED")
            print("=" * 40)
    else:
        print("=" * 40)
        print("Step 1: Database Creation - ❌ FAILED")
        print("=" * 40)
        print("Please fix the database connection issues before proceeding.")


if __name__ == "__main__":
    main()
