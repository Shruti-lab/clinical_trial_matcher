#!/bin/bash

# Clinical Trial Matcher - Development Environment Setup Script

set -e  # Exit on any error

echo "🚀 Clinical Trial Matcher - Development Setup"
echo "============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
print_status "Checking prerequisites..."

# Check Docker
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Check Node.js
if ! command -v node &> /dev/null; then
    print_error "Node.js is not installed. Please install Node.js 18+ first."
    exit 1
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.11+ first."
    exit 1
fi

print_success "All prerequisites are installed!"

# Setup environment files
print_status "Setting up environment files..."

if [ ! -f "backend/.env" ]; then
    cp backend/.env.example backend/.env
    print_success "Created backend/.env from template"
else
    print_warning "backend/.env already exists, skipping..."
fi

if [ ! -f "frontend/.env" ]; then
    cp frontend/.env.example frontend/.env
    print_success "Created frontend/.env from template"
else
    print_warning "frontend/.env already exists, skipping..."
fi

# Start Docker services
print_status "Starting Docker services..."
docker-compose up -d

print_status "Waiting for services to be ready..."
sleep 10

# Check service health
print_status "Checking service health..."

# Wait for MySQL
print_status "Waiting for MySQL to be ready..."
until docker-compose exec -T mysql mysqladmin ping -h localhost --silent; do
    echo -n "."
    sleep 2
done
print_success "MySQL is ready!"

# Wait for Redis
print_status "Waiting for Redis to be ready..."
until docker-compose exec -T redis redis-cli ping | grep -q PONG; do
    echo -n "."
    sleep 2
done
print_success "Redis is ready!"

# Wait for LocalStack
print_status "Waiting for LocalStack to be ready..."
until curl -s http://localhost:4566/_localstack/health | grep -q '"s3": "available"'; do
    echo -n "."
    sleep 2
done
print_success "LocalStack is ready!"

# Wait for OpenSearch
print_status "Waiting for OpenSearch to be ready..."
until curl -s http://localhost:9200/_cluster/health | grep -q '"status":"'; do
    echo -n "."
    sleep 2
done
print_success "OpenSearch is ready!"

# Setup backend
print_status "Setting up Python backend..."
cd backend

if [ ! -d "venv" ]; then
    print_status "Creating Python virtual environment..."
    python3 -m venv venv
    print_success "Virtual environment created!"
fi

print_status "Activating virtual environment and installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt
print_success "Backend dependencies installed!"

cd ..

# Setup frontend
print_status "Setting up React frontend..."
cd frontend

if [ ! -d "node_modules" ]; then
    print_status "Installing Node.js dependencies..."
    npm install
    print_success "Frontend dependencies installed!"
else
    print_warning "node_modules already exists, skipping npm install..."
fi

cd ..

# Run verification script
print_status "Running environment verification..."
cd backend
source venv/bin/activate
python ../scripts/verify-setup.py
cd ..

print_success "🎉 Development environment setup complete!"
echo ""
echo "Next steps:"
echo "1. Start the backend server:"
echo "   cd backend && source venv/bin/activate && uvicorn src.main:app --reload"
echo ""
echo "2. In a new terminal, start the frontend server:"
echo "   cd frontend && npm run dev"
echo ""
echo "3. Open your browser to:"
echo "   - Frontend: http://localhost:5173"
echo "   - Backend API: http://localhost:8000"
echo "   - API Docs: http://localhost:8000/docs"
echo ""
echo "4. To stop services later:"
echo "   docker-compose down"
echo ""
print_success "Happy coding! 🚀"