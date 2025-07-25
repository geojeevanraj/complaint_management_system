import os
from typing import Optional

from dotenv import load_dotenv

load_dotenv()

# Check if we should skip database operations entirely (for CI/testing)
SKIP_DB_CONNECTION = os.getenv("SKIP_DB_CONNECTION", "false").lower() == "true"
CI_ENVIRONMENT = os.getenv("CI_ENVIRONMENT", "false").lower() == "true"

# Try to import pyodbc, but handle gracefully if not available
try:
    if not SKIP_DB_CONNECTION and not CI_ENVIRONMENT:
        import pyodbc
    else:
        pyodbc = None
except ImportError:
    pyodbc = None


class DatabaseConfig:
    """Database configuration and connection management"""

    def __init__(self):
        self.server = os.getenv("DB_SERVER", "localhost")
        self.database = os.getenv("DB_NAME", "complaint_system")
        self.username = os.getenv("DB_USER", "root")
        self.password = os.getenv("DB_PASSWORD", "")
        self.port = os.getenv("DB_PORT", "3306")

        self.possible_drivers = [
            os.getenv("DB_DRIVER", "{MySQL ODBC 9.3 Unicode Driver}"),
            "{MySQL ODBC 9.3 Unicode Driver}",
            "{MySQL ODBC 9.3 ANSI Driver}",
            "{MySQL ODBC 8.0 Unicode Driver}",
            "{MySQL ODBC 8.0 ANSI Driver}",
            "{MySQL ODBC 8.0 Driver}",
            "{MySQL ODBC 5.3 Unicode Driver}",
            "{MySQL ODBC 5.3 ANSI Driver}",
            "{MySQL ODBC 5.1 Driver}",
            "MySQL ODBC 9.3 Unicode Driver",
            "MySQL ODBC 9.3 ANSI Driver",
            "MySQL ODBC 8.0 Driver",
            "MySQL ODBC 8.0 Unicode Driver",
            "MySQL ODBC 8.0 ANSI Driver",
            # Common Linux/Ubuntu driver names
            "MySQL",
            "MariaDB",
            "{MySQL}",
            "{MariaDB}",
            "MySQL ODBC Driver",
            "libmyodbc",
        ]

        self.driver = None
        self.connection_string = None
        self._connection = None

        # Skip driver detection in test environments if requested
        if pyodbc is None or SKIP_DB_CONNECTION or CI_ENVIRONMENT:
            print("ℹ️ Database operations skipped (CI environment or pyodbc not available)")
            return
            
        if os.getenv("SKIP_DB_DRIVER_CHECK", "false").lower() != "true":
            self._find_available_driver()

    def _find_available_driver(self):
        """Find an available MySQL ODBC driver"""
        if pyodbc is None:
            print("ℹ️ pyodbc not available, skipping driver detection")
            return
            
        available_drivers = pyodbc.drivers()

        print("Available ODBC drivers:")
        for driver in available_drivers:
            print(f"  - {driver}")

        for driver in self.possible_drivers:
            driver_name = driver.strip("{}")
            if driver in available_drivers or driver_name in available_drivers:
                self.driver = driver
                break

        if not self.driver:
            print("\nERROR: No MySQL ODBC driver found!")
            print("Please install MySQL Connector/ODBC from:")
            print("https://dev.mysql.com/downloads/connector/odbc/")
            print("\nAlternatively, you can:")
            print("1. Install MySQL Workbench (includes ODBC driver)")
            print("2. Use the Windows MySQL Installer")
            raise Exception("MySQL ODBC driver not found")

        print(f"\nUsing MySQL ODBC driver: {self.driver}")

        self.connection_string = (
            f"DRIVER={self.driver};"
            f"SERVER={self.server};"
            f"PORT={self.port};"
            f"DATABASE={self.database};"
            f"UID={self.username};"
            f"PWD={self.password};"
            f"charset=utf8mb4;"
        )

        print(
            f"Connection string: {self.connection_string.replace(self.password, '***')}"
        )

    def get_connection(self):
        """Get database connection"""
        if pyodbc is None or SKIP_DB_CONNECTION or CI_ENVIRONMENT:
            print("ℹ️ Database connection skipped (CI environment or pyodbc not available)")
            return None
            
        try:
            if self._connection is None or not self._connection:
                if not self.connection_string:
                    raise Exception("Database connection string not configured")

                print("Attempting to connect to MySQL database...")
                self._connection = pyodbc.connect(self.connection_string)
                self._connection.autocommit = False
                print("Database connection established successfully!")
            return self._connection
        except pyodbc.Error as e:
            error_msg = f"Database connection error: {e}"
            print(error_msg)
            print("\nTroubleshooting steps:")
            print("1. Ensure MySQL server is running")
            print("2. Check database credentials in .env file")
            print("3. Verify MySQL ODBC driver is installed")
            print("4. Ensure database 'complaint_system' exists")
            print("5. Check firewall settings")
            raise
        except Exception as e:
            print(f"Connection configuration error: {e}")
            raise

    def close_connection(self):
        """Close database connection"""
        if self._connection:
            self._connection.close()
            self._connection = None

    def execute_query(self, query: str, params: tuple = None):
        """Execute a SELECT query and return results"""
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            results = cursor.fetchall()
            return results
        except pyodbc.Error as e:
            print(f"Query execution error: {e}")
            raise
        finally:
            if cursor:
                cursor.close()

    def execute_non_query(self, query: str, params: tuple = None):
        """Execute INSERT, UPDATE, DELETE queries"""
        conn = None
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            conn.commit()
            affected_rows = cursor.rowcount
            return affected_rows
        except pyodbc.Error as e:
            if conn:
                conn.rollback()
            print(f"Non-query execution error: {e}")
            raise
        finally:
            if cursor:
                cursor.close()

    def create_tables(self):
        """Create database tables if they don't exist"""
        tables = [
            """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                role ENUM('user', 'admin', 'staff') DEFAULT 'user',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS complaints (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                category VARCHAR(255) NOT NULL,
                description TEXT NOT NULL,
                status ENUM('Pending', 'In Progress', 'Resolved') DEFAULT 'Pending',
                assigned_to INT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (assigned_to) REFERENCES users(id) ON DELETE SET NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS complaint_comments (
                id INT AUTO_INCREMENT PRIMARY KEY,
                complaint_id INT NOT NULL,
                staff_id INT NOT NULL,
                comment TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (complaint_id) REFERENCES complaints(id) ON DELETE CASCADE,
                FOREIGN KEY (staff_id) REFERENCES users(id) ON DELETE CASCADE
            )
            """,
        ]

        try:
            for table_sql in tables:
                self.execute_non_query(table_sql)
            print("Database tables created successfully.")
        except Exception as e:
            print(f"Error creating tables: {e}")


db_config = DatabaseConfig()
