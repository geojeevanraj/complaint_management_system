"""
ODBC Driver and MySQL Connection Test Script
Run this script to diagnose ODBC and MySQL connectivity issues
"""

import os

import pyodbc
from dotenv import load_dotenv

load_dotenv()


def test_odbc_drivers():
    """Test available ODBC drivers"""
    print("=== ODBC Driver Test ===")

    try:
        drivers = pyodbc.drivers()
        print(f"Found {len(drivers)} ODBC drivers:")

        mysql_drivers = []
        for driver in drivers:
            print(f"  - {driver}")
            if "mysql" in driver.lower():
                mysql_drivers.append(driver)

        print(f"\nMySQL-related drivers found: {len(mysql_drivers)}")
        for driver in mysql_drivers:
            print(f"  * {driver}")

        if not mysql_drivers:
            print("\n❌ NO MySQL ODBC drivers found!")
            print("Please install MySQL Connector/ODBC from:")
            print("https://dev.mysql.com/downloads/connector/odbc/")
            return False
        else:
            print("\n✅ MySQL ODBC drivers are available!")
            return True

    except Exception as e:
        print(f"Error checking ODBC drivers: {e}")
        return False


def test_mysql_connection():
    """Test MySQL database connection"""
    print("\n=== MySQL Connection Test ===")

    # Get connection parameters
    server = os.getenv("DB_SERVER", "localhost")
    database = os.getenv("DB_NAME", "complaint_system")
    username = os.getenv("DB_USER", "root")
    password = os.getenv("DB_PASSWORD", "")
    port = os.getenv("DB_PORT", "3306")

    print(f"Server: {server}")
    print(f"Database: {database}")
    print(f"Username: {username}")
    print(f"Port: {port}")
    print(f"Password: {'***' if password else '(empty)'}")

    # Try different MySQL drivers
    drivers_to_try = [
        "{MySQL ODBC 8.0 Driver}",
        "{MySQL ODBC 8.0 Unicode Driver}",
        "{MySQL ODBC 8.0 ANSI Driver}",
        "{MySQL ODBC 5.3 Unicode Driver}",
        "{MySQL ODBC 5.3 ANSI Driver}",
        "MySQL ODBC 8.0 Driver",
        "MySQL ODBC 8.0 Unicode Driver",
    ]

    available_drivers = pyodbc.drivers()

    for driver in drivers_to_try:
        driver_name = driver.strip("{}")
        if driver in available_drivers or driver_name in available_drivers:
            print(f"\nTrying driver: {driver}")

            connection_string = (
                f"DRIVER={driver};"
                f"SERVER={server};"
                f"PORT={port};"
                f"DATABASE={database};"
                f"UID={username};"
                f"PWD={password};"
            )

            try:
                print("Attempting connection...")
                conn = pyodbc.connect(connection_string)

                # Test the connection
                cursor = conn.cursor()
                cursor.execute("SELECT VERSION()")
                version = cursor.fetchone()[0]
                cursor.close()
                conn.close()

                print(f"✅ Connection successful!")
                print(f"MySQL Version: {version}")
                print(f"Working driver: {driver}")
                return True

            except pyodbc.Error as e:
                print(f"❌ Connection failed: {e}")
                continue
            except Exception as e:
                print(f"❌ Unexpected error: {e}")
                continue

    print("\n❌ Could not establish MySQL connection with any driver!")
    return False


def test_database_exists():
    """Test if the database exists"""
    print("\n=== Database Existence Test ===")

    server = os.getenv("DB_SERVER", "localhost")
    username = os.getenv("DB_USER", "root")
    password = os.getenv("DB_PASSWORD", "")
    port = os.getenv("DB_PORT", "3306")

    drivers_to_try = [
        "{MySQL ODBC 8.0 Driver}",
        "{MySQL ODBC 8.0 Unicode Driver}",
        "MySQL ODBC 8.0 Driver",
    ]

    available_drivers = pyodbc.drivers()

    for driver in drivers_to_try:
        if driver in available_drivers or driver.strip("{}") in available_drivers:
            connection_string = (
                f"DRIVER={driver};"
                f"SERVER={server};"
                f"PORT={port};"
                f"UID={username};"
                f"PWD={password};"
            )

            try:
                print(f"Connecting to MySQL server (without specific database)...")
                conn = pyodbc.connect(connection_string)
                cursor = conn.cursor()

                # Check if database exists
                cursor.execute("SHOW DATABASES")
                databases = [row[0] for row in cursor.fetchall()]

                target_db = os.getenv("DB_NAME", "complaint_system")
                if target_db in databases:
                    print(f"✅ Database '{target_db}' exists!")
                else:
                    print(f"❌ Database '{target_db}' does not exist!")
                    print(f"Available databases: {', '.join(databases)}")
                    print(f"\nTo create the database, run:")
                    print(f"CREATE DATABASE {target_db};")

                cursor.close()
                conn.close()
                return target_db in databases

            except pyodbc.Error as e:
                print(f"Error connecting to MySQL server: {e}")
                continue

    print("Could not connect to MySQL server!")
    return False


def main():
    """Run all tests"""
    print("MySQL ODBC Connection Diagnostic Tool")
    print("=" * 50)

    # Test 1: Check ODBC drivers
    drivers_ok = test_odbc_drivers()

    if not drivers_ok:
        print("\n⚠️  Install MySQL ODBC driver first!")
        return

    # Test 2: Check database existence
    db_exists = test_database_exists()

    # Test 3: Test full connection
    connection_ok = test_mysql_connection()

    print("\n" + "=" * 50)
    print("SUMMARY:")
    print(f"ODBC Drivers: {'✅ OK' if drivers_ok else '❌ MISSING'}")
    print(f"Database: {'✅ EXISTS' if db_exists else '❌ MISSING'}")
    print(f"Connection: {'✅ OK' if connection_ok else '❌ FAILED'}")

    if not db_exists:
        print("\n💡 TO FIX: Create the database first:")
        print("1. Connect to MySQL as root")
        print("2. Run: CREATE DATABASE complaint_system;")

    if drivers_ok and db_exists and connection_ok:
        print("\n🎉 Everything looks good! You can run the application now.")
    else:
        print("\n⚠️  Please fix the issues above before running the application.")


if __name__ == "__main__":
    main()
