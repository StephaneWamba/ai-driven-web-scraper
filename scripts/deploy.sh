#!/bin/bash

# AI Scraper Deployment Script
# This script deploys the application to the EC2 instance

set -e

# Configuration
SERVER_IP="54.165.182.47"
SSH_USER="ubuntu"
SSH_KEY="${SSH_KEY:-~/.ssh/ai-scraper.pem}"
REPO_URL="https://github.com/your-username/ai-driven-web-scraper.git"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check dependencies
check_dependencies() {
    log_info "Checking dependencies..."
    
    if ! command -v ssh &> /dev/null; then
        log_error "SSH is not installed"
        exit 1
    fi
    
    if ! command -v scp &> /dev/null; then
        log_error "SCP is not installed"
        exit 1
    fi
    
    if [ ! -f "$SSH_KEY" ]; then
        log_error "SSH key not found at $SSH_KEY"
        exit 1
    fi
    
    log_info "Dependencies check passed"
}

# Test server connectivity
test_connectivity() {
    log_info "Testing server connectivity..."
    
    if ! ssh -i "$SSH_KEY" -o ConnectTimeout=10 -o StrictHostKeyChecking=no "$SSH_USER@$SERVER_IP" "echo 'Connection successful'" &> /dev/null; then
        log_error "Cannot connect to server at $SERVER_IP"
        exit 1
    fi
    
    log_info "Server connectivity confirmed"
}

# Deploy backend
deploy_backend() {
    log_info "Deploying backend..."
    
    ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no "$SSH_USER@$SERVER_IP" << 'EOF'
        cd /home/ubuntu/ai-scraper
        git pull origin main
        cd backend
        source venv/bin/activate
        pip install -r requirements.txt
        sudo systemctl restart ai-scraper-backend
        echo "Backend deployment completed"
EOF
    
    log_info "Backend deployment completed"
}

# Deploy frontend
deploy_frontend() {
    log_info "Deploying frontend..."
    
    ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no "$SSH_USER@$SERVER_IP" << 'EOF'
        cd /home/ubuntu/ai-scraper/frontend
        npm install
        npm run build
        sudo systemctl restart nginx
        echo "Frontend deployment completed"
EOF
    
    log_info "Frontend deployment completed"
}

# Health check
health_check() {
    log_info "Performing health checks..."
    
    # Wait for services to start
    sleep 10
    
    # Check backend health
    if ! curl -f "http://$SERVER_IP:8000/health" &> /dev/null; then
        log_error "Backend health check failed"
        return 1
    fi
    
    # Check frontend
    if ! curl -f "http://$SERVER_IP" &> /dev/null; then
        log_error "Frontend health check failed"
        return 1
    fi
    
    log_info "Health checks passed"
}

# Main deployment function
main() {
    log_info "Starting deployment to $SERVER_IP"
    
    check_dependencies
    test_connectivity
    deploy_backend
    deploy_frontend
    health_check
    
    log_info "Deployment completed successfully!"
    log_info "Application URL: http://$SERVER_IP"
    log_info "API Docs: http://$SERVER_IP:8000/docs"
}

# Run main function
main "$@" 