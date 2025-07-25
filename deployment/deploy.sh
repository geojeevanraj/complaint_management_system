#!/bin/bash
# Traditional server deployment script (no Docker)

set -e  # Exit on any error

echo "🚀 Starting deployment of Complaint Management System..."

# Configuration
APP_DIR="/var/www/complaint_system"
SERVICE_NAME="complaint-system"
BACKUP_DIR="/var/backups/complaint_system"
PYTHON_VERSION="3.12"

# Function to create backup
create_backup() {
    echo "📦 Creating backup..."
    sudo mkdir -p $BACKUP_DIR
    sudo cp -r $APP_DIR $BACKUP_DIR/backup_$(date +%Y%m%d_%H%M%S)
    echo "✅ Backup created"
}

# Function to setup application
setup_application() {
    echo "🔧 Setting up application..."
    
    # Create app directory if it doesn't exist
    sudo mkdir -p $APP_DIR
    cd $APP_DIR
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        echo "Creating virtual environment..."
        python$PYTHON_VERSION -m venv venv
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Upgrade pip
    pip install --upgrade pip
    
    # Install dependencies
    echo "Installing dependencies..."
    pip install -r requirements.txt
    
    # Set permissions
    sudo chown -R www-data:www-data $APP_DIR
    sudo chmod -R 755 $APP_DIR
    
    echo "✅ Application setup complete"
}

# Function to setup database
setup_database() {
    echo "🗄️ Setting up database..."
    
    # Activate virtual environment
    cd $APP_DIR
    source venv/bin/activate
    
    # Run database setup
    python setup_database.py
    
    echo "✅ Database setup complete"
}

# Function to setup systemd service
setup_service() {
    echo "⚙️ Setting up systemd service..."
    
    # Copy service file
    sudo cp deployment/complaint-system.service /etc/systemd/system/
    
    # Reload systemd
    sudo systemctl daemon-reload
    
    # Enable service
    sudo systemctl enable $SERVICE_NAME
    
    echo "✅ Service setup complete"
}

# Function to start application
start_application() {
    echo "🚀 Starting application..."
    
    # Start service
    sudo systemctl start $SERVICE_NAME
    
    # Check status
    sleep 5
    if sudo systemctl is-active --quiet $SERVICE_NAME; then
        echo "✅ Application started successfully"
        sudo systemctl status $SERVICE_NAME
    else
        echo "❌ Failed to start application"
        sudo systemctl status $SERVICE_NAME
        exit 1
    fi
}

# Function to run health check
health_check() {
    echo "🏥 Running health check..."
    
    # Wait for application to be ready
    sleep 10
    
    # Check if application is responding
    if curl -f http://localhost:8000/health 2>/dev/null; then
        echo "✅ Health check passed"
    else
        echo "⚠️ Health check failed - application may not be fully ready"
    fi
}

# Function to rollback
rollback() {
    echo "🔄 Rolling back to previous version..."
    
    # Stop current service
    sudo systemctl stop $SERVICE_NAME
    
    # Restore from latest backup
    LATEST_BACKUP=$(ls -1t $BACKUP_DIR | head -n 1)
    if [ -n "$LATEST_BACKUP" ]; then
        sudo rm -rf $APP_DIR
        sudo cp -r $BACKUP_DIR/$LATEST_BACKUP $APP_DIR
        sudo systemctl start $SERVICE_NAME
        echo "✅ Rollback complete"
    else
        echo "❌ No backup found for rollback"
        exit 1
    fi
}

# Main deployment function
deploy() {
    echo "🎯 Starting deployment process..."
    
    # Create backup before deployment
    if [ -d "$APP_DIR" ]; then
        create_backup
    fi
    
    # Setup application
    setup_application
    
    # Setup database
    setup_database
    
    # Setup systemd service
    setup_service
    
    # Restart service if it was already running
    if sudo systemctl is-active --quiet $SERVICE_NAME; then
        echo "🔄 Restarting existing service..."
        sudo systemctl restart $SERVICE_NAME
    else
        # Start new service
        start_application
    fi
    
    # Run health check
    health_check
    
    echo "🎉 Deployment completed successfully!"
}

# Command line interface
case "$1" in
    deploy)
        deploy
        ;;
    rollback)
        rollback
        ;;
    start)
        start_application
        ;;
    stop)
        echo "⏹️ Stopping application..."
        sudo systemctl stop $SERVICE_NAME
        echo "✅ Application stopped"
        ;;
    restart)
        echo "🔄 Restarting application..."
        sudo systemctl restart $SERVICE_NAME
        echo "✅ Application restarted"
        ;;
    status)
        sudo systemctl status $SERVICE_NAME
        ;;
    logs)
        sudo journalctl -u $SERVICE_NAME -f
        ;;
    setup)
        setup_application
        setup_database
        setup_service
        ;;
    *)
        echo "Usage: $0 {deploy|rollback|start|stop|restart|status|logs|setup}"
        echo ""
        echo "Commands:"
        echo "  deploy   - Full deployment process"
        echo "  rollback - Rollback to previous version"
        echo "  start    - Start the application"
        echo "  stop     - Stop the application"
        echo "  restart  - Restart the application"
        echo "  status   - Show application status"
        echo "  logs     - Show application logs"
        echo "  setup    - Initial setup only"
        exit 1
esac
