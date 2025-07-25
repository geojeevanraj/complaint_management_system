# Complaint Management System - MVC Architecture

A comprehensive complaint management system built using the Model-View-Controller (MVC) architecture pattern with MySQL database connectivity via ODBC.

## Features

- **User Management**: Registration, authentication, and role-based access control (User, Admin, Staff)
- **Complaint Management**: Create, view, update, delete, and assign complaints
- **Role-Based Access**: Different interfaces and permissions for users, administrators, and staff
- **Commenting System**: Staff can add comments to assigned complaints
- **Search & Filter**: Search complaints by category and filter by status
- **Export Functionality**: Export complaints to CSV format
- **Statistics Dashboard**: View complaint statistics and metrics

## Architecture

The application follows the MVC (Model-View-Controller) pattern:

```
complaint/
├── models/              # Data models and database operations
│   ├── __init__.py
│   ├── user.py         # User model
│   ├── complaint.py    # Complaint model
│   └── comment.py      # Comment model
├── views/              # User interface and display logic
│   ├── __init__.py
│   └── views.py        # View classes for different interfaces
├── controllers/        # Business logic and application flow
│   ├── __init__.py
│   └── controllers.py  # Controller classes
├── config/             # Configuration and database setup
│   ├── __init__.py
│   └── database.py     # Database configuration and connection
├── app.py              # Main application entry point
├── main.py             # Original monolithic version (for reference)
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
└── README.md           # This file
```

## Prerequisites

1. **Python 3.7+**
2. **MySQL Server** (8.0 or later recommended)
3. **MySQL ODBC Driver** (8.0 or later)
4. **Python packages** (see requirements.txt)

## Installation

### 1. Clone/Download the Project

```bash
git clone <repository-url>
cd complaint
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install MySQL ODBC Driver

#### Windows:
- Download and install MySQL Connector/ODBC from [MySQL official website](https://dev.mysql.com/downloads/connector/odbc/)
- The driver name should be `{MySQL ODBC 8.0 Driver}` (default in the configuration)

#### Linux:
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install mysql-connector-odbc

# CentOS/RHEL
sudo yum install mysql-connector-odbc
```

#### macOS:
```bash
# Using Homebrew
brew install mysql-connector-odbc
```

### 4. Set Up MySQL Database

1. Create a MySQL database:
```sql
CREATE DATABASE complaint_system;
```

2. Create a MySQL user (optional, you can use root):
```sql
CREATE USER 'complaint_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON complaint_system.* TO 'complaint_user'@'localhost';
FLUSH PRIVILEGES;
```

### 5. Configure Environment Variables

1. Copy the environment template:
```bash
copy .env.example .env  # Windows
# or
cp .env.example .env    # Linux/macOS
```

2. Edit `.env` file with your database credentials:
```env
DB_SERVER=localhost
DB_NAME=complaint_system
DB_USER=root
DB_PASSWORD=your_password_here
DB_DRIVER={MySQL ODBC 8.0 Driver}
DB_PORT=3306
```

## Usage

### Running the Application

```bash
python app.py
```

### First Time Setup

1. Run the application - it will automatically create the required database tables
2. Register an admin user:
   - Choose option 1 (Register)
   - Enter name, email, password
   - For role, enter `admin`
3. Register staff users with role `staff`
4. Regular users can register with role `user` or leave it empty (defaults to `user`)

### User Roles and Permissions

#### Regular Users
- Register and submit complaints
- View their own complaints
- Update their own complaint details
- Delete their own complaints
- Change password
- Search their complaints by category
- Export their complaints to CSV

#### Staff Members
- View complaints assigned to them
- Update status of assigned complaints
- Add comments to assigned complaints
- Change password

#### Administrators
- View all complaints in the system
- Update any complaint status
- Assign complaints to staff members
- View complaint statistics
- Search all complaints by category
- Filter complaints by status
- Export all complaints to CSV
- List staff members
- All user permissions

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('user', 'admin', 'staff') DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Complaints Table
```sql
CREATE TABLE complaints (
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
);
```

### Complaint Comments Table
```sql
CREATE TABLE complaint_comments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    complaint_id INT NOT NULL,
    staff_id INT NOT NULL,
    comment TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (complaint_id) REFERENCES complaints(id) ON DELETE CASCADE,
    FOREIGN KEY (staff_id) REFERENCES users(id) ON DELETE CASCADE
);
```

## Troubleshooting

### Common Issues

1. **ODBC Driver Not Found**
   - Ensure MySQL ODBC Driver is installed
   - Check the driver name in your system's ODBC Data Source Administrator
   - Update the `DB_DRIVER` in your `.env` file if needed

2. **Database Connection Failed**
   - Verify MySQL server is running
   - Check database credentials in `.env` file
   - Ensure the database exists
   - Check firewall settings

3. **Import Errors**
   - Ensure you're running the application from the project root directory
   - Check that all required packages are installed: `pip install -r requirements.txt`

### Checking ODBC Drivers

#### Windows:
- Open "ODBC Data Source Administrator" from Control Panel
- Check the "Drivers" tab for MySQL ODBC drivers

#### Linux:
```bash
odbcinst -q -d
```

#### macOS:
```bash
odbcinst -q -d
```

## Migration from MongoDB Version

If you're migrating from the original MongoDB version (`main.py`), you'll need to:

1. Export your data from MongoDB
2. Set up the MySQL database as described above
3. Import your data into the new MySQL schema
4. Update any custom modifications you made to the original code

## Development

### CI/CD Pipeline

This project includes a comprehensive GitHub Actions CI/CD pipeline:

#### 🔄 Continuous Integration
- **Automated Testing**: Tests run on Python 3.8, 3.9, 3.10, 3.11
- **Code Quality**: Linting with flake8, formatting with black, import sorting with isort
- **Security Scanning**: Security analysis with bandit and safety
- **Coverage Reporting**: Code coverage analysis with pytest-cov

#### 🚀 Continuous Deployment
- **Staging**: Auto-deploy from `main` branch
- **Production**: Deploy from version tags (`v*`)
- **Health Checks**: Automated post-deployment verification

#### 📦 Dependency Management
- **Weekly Updates**: Automatic dependency updates every Monday
- **Security Audits**: Regular vulnerability scanning
- **Pull Request Creation**: Automated PRs for dependency updates

### Development Workflow

1. **Local Development**:
   ```bash
   # Install dependencies
   pip install -r requirements.txt

   # Run all checks locally
   python run_tests.py

   # Or run individual checks
   make format        # Format code
   make lint         # Run linting
   make test         # Run tests
   make security     # Security checks
   ```

2. **Branch Strategy**:
   - `main`: Production-ready code
   - `develop`: Development branch
   - `feature/*`: Feature branches
   - `hotfix/*`: Hotfix branches

3. **Quality Gates**:
   - ✅ All tests pass
   - ✅ Code coverage meets threshold
   - ✅ No security vulnerabilities
   - ✅ Code style compliance
   - ✅ No linting errors

### Pipeline Status

Monitor the pipeline status through:
- GitHub Actions tab
- Status badges (coming soon)
- Email notifications for failures

For detailed CI/CD documentation, see [`docs/CI_CD_PIPELINE.md`](docs/CI_CD_PIPELINE.md).

### Adding New Features

1. **Models**: Add new database operations in the appropriate model file
2. **Views**: Add new display logic in the views
3. **Controllers**: Add business logic to handle new operations
4. **App**: Update the main application flow if needed

### Code Structure Guidelines

- Keep database operations in model classes
- Keep user interface logic in view classes
- Keep business logic in controller classes
- Use the database configuration singleton for all database connections

## License

This project is provided as-is for educational and development purposes.

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Ensure all prerequisites are properly installed
3. Verify your database configuration
4. Check the application logs for detailed error messages
