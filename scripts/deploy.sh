#!/bin/bash
# Production deployment script

set -e

echo "=========================================="
echo "FabricERP Deployment Script"
echo "=========================================="

# Check environment
ENVIRONMENT=${ENVIRONMENT:-production}
echo "Environment: $ENVIRONMENT"

# Pull latest code
echo "Pulling latest code..."
git pull origin main

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run migrations
echo "Running database migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Compile translation files
echo "Compiling translation files..."
python manage.py compilemessages

# Restart services
echo "Restarting services..."
sudo systemctl restart gunicorn
sudo systemctl restart nginx

# Health check
echo "Performing health check..."
sleep 5
curl -f http://localhost:8000/health/ || {
    echo "Health check failed!"
    exit 1
}

echo "=========================================="
echo "Deployment completed successfully!"
echo "=========================================="