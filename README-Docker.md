# AI-Driven Web Scraper - Docker & CI/CD Setup

This document explains the Docker containerization and CI/CD pipeline setup for the AI-Driven Web Scraper project.

## 🐳 Docker Setup

### Architecture Overview

The application is containerized using Docker with the following components:

- **Backend**: FastAPI application with Python 3.11
- **Frontend**: React application served by Nginx
- **Database**: PostgreSQL 14
- **Cache/Queue**: Redis 7
- **Worker**: Celery for background tasks
- **Monitor**: Flower for task monitoring

### Docker Images

#### Backend Image (`Dockerfile.backend`)

- Base: Python 3.11-slim
- Includes: Playwright, Node.js, all Python dependencies
- Security: Non-root user, health checks
- Port: 8000

#### Frontend Image (`Dockerfile.frontend`)

- Multi-stage build: Node.js → Nginx
- Optimized: Production build, static file serving
- Security: Security headers, rate limiting
- Port: 80

### Local Development

#### Prerequisites

```bash
# Install Docker and Docker Compose
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

#### Quick Start

```bash
# Clone the repository
git clone <repository-url>
cd ai-driven-web-scraper

# Make deployment script executable
chmod +x scripts/deploy.sh

# Deploy locally
./scripts/deploy.sh local
```

#### Manual Docker Compose

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild and restart
docker-compose up -d --build
```

#### Service URLs (Local)

- **Frontend**: http://localhost
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Flower (Task Monitor)**: http://localhost:5555
- **Database**: localhost:5432
- **Redis**: localhost:6379

### Production Deployment

#### AWS ECR Setup

```bash
# Create ECR repositories
aws ecr create-repository --repository-name ai-scraper-backend
aws ecr create-repository --repository-name ai-scraper-frontend

# Get login token
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
```

#### Environment Variables

```bash
export OPENAI_API_KEY="your_openai_api_key"
export AWS_ACCOUNT_ID="your_aws_account_id"
export DB_PASSWORD="secure_password"
```

#### Deploy to Production

```bash
./scripts/deploy.sh production
```

## 🔄 CI/CD Pipeline

### GitHub Actions Workflow

The CI/CD pipeline is defined in `.github/workflows/ci-cd.yml` and includes:

#### 1. Testing Phase

- **Backend Tests**: Python unit tests with coverage
- **Frontend Tests**: React component tests with coverage
- **Code Quality**: Linting, type checking

#### 2. Build Phase

- **Docker Images**: Build and tag images
- **Security Scan**: Trivy vulnerability scanning
- **Push to ECR**: Upload images to AWS ECR

#### 3. Deployment Phase

- **Infrastructure**: Terraform deployment
- **ECS Update**: Update ECS services
- **Health Checks**: Verify deployment success

#### 4. Post-Deployment

- **Performance Tests**: Load testing with Locust
- **Monitoring**: Service health verification
- **Notifications**: Slack/email notifications

### Pipeline Triggers

- **Push to main**: Full deployment to production
- **Push to develop**: Testing and staging deployment
- **Pull Request**: Testing only

### Required Secrets

Configure these secrets in your GitHub repository:

```bash
# AWS Credentials
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY

# Database
DB_PASSWORD

# API Keys
OPENAI_API_KEY

# Notifications
SLACK_WEBHOOK

# Performance Testing
API_URL
```

## 🏗️ Infrastructure as Code

### Terraform Integration

The CI/CD pipeline integrates with Terraform for infrastructure management:

```yaml
# Deploy infrastructure
- name: Deploy infrastructure with Terraform
  run: |
    cd terraform
    terraform init
    terraform plan -var="environment=production" -var="aws_region=${{ env.AWS_REGION }}" -var="db_password=${{ secrets.DB_PASSWORD }}"
    terraform apply -auto-approve -var="environment=production" -var="aws_region=${{ env.AWS_REGION }}" -var="db_password=${{ secrets.DB_PASSWORD }}"
```

### ECS Service Update

```yaml
# Update ECS service
- name: Update ECS service
  run: |
    aws ecs update-service --cluster $ECS_CLUSTER --service $ECS_SERVICE --force-new-deployment
```

## 🔒 Security Features

### Docker Security

- **Non-root users**: All containers run as non-root
- **Health checks**: Built-in health monitoring
- **Minimal base images**: Alpine/slim images where possible
- **Security scanning**: Trivy vulnerability scanning

### Network Security

- **Rate limiting**: API rate limiting via Nginx
- **Security headers**: XSS protection, content type validation
- **CORS configuration**: Proper CORS setup
- **Network isolation**: Docker networks for service isolation

### Secrets Management

- **Environment variables**: Secure secret injection
- **AWS Secrets Manager**: Production secret storage
- **No hardcoded secrets**: All secrets externalized

## 📊 Monitoring & Observability

### Health Checks

```yaml
# Backend health check
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
```

### Logging

- **Structured logging**: JSON format logs
- **Centralized logging**: CloudWatch integration
- **Log rotation**: Automatic log management

### Metrics

- **Application metrics**: Custom business metrics
- **Infrastructure metrics**: CPU, memory, disk usage
- **Performance metrics**: Response times, throughput

## 🚀 Performance Optimization

### Docker Optimizations

- **Multi-stage builds**: Reduced image sizes
- **Layer caching**: Optimized build times
- **Alpine images**: Minimal footprint
- **Build context optimization**: .dockerignore usage

### Application Optimizations

- **Gzip compression**: Nginx compression
- **Static file caching**: Long-term caching
- **CDN integration**: CloudFront for global delivery
- **Database connection pooling**: Optimized DB connections

## 🔧 Troubleshooting

### Common Issues

#### 1. Build Failures

```bash
# Clean Docker cache
docker system prune -a

# Rebuild without cache
docker-compose build --no-cache
```

#### 2. Service Health Issues

```bash
# Check service logs
docker-compose logs <service-name>

# Check service health
curl http://localhost:8000/health
```

#### 3. Database Connection Issues

```bash
# Check database connectivity
docker-compose exec postgres pg_isready -U scraper_user

# Check database logs
docker-compose logs postgres
```

#### 4. CI/CD Pipeline Issues

```bash
# Check GitHub Actions logs
# Go to Actions tab in GitHub repository

# Test locally
./scripts/deploy.sh local
```

### Debug Commands

```bash
# Enter running container
docker-compose exec backend bash

# View real-time logs
docker-compose logs -f backend

# Check resource usage
docker stats

# Inspect container
docker inspect ai-scraper-backend
```

## 📈 Scaling

### Horizontal Scaling

```bash
# Scale backend services
docker-compose up -d --scale backend=3 --scale worker=2

# Scale in production
aws ecs update-service --cluster ai-scraper-cluster --service ai-scraper-backend --desired-count 3
```

### Load Balancing

- **Application Load Balancer**: AWS ALB for traffic distribution
- **Auto Scaling**: ECS auto-scaling based on metrics
- **Health checks**: Automatic unhealthy instance removal

## 🔄 Rollback Strategy

### Blue-Green Deployment

1. Deploy new version to green environment
2. Run health checks and tests
3. Switch traffic to green environment
4. Keep blue environment for quick rollback

### Rollback Commands

```bash
# Rollback ECS service
aws ecs update-service --cluster ai-scraper-cluster --service ai-scraper-service --task-definition ai-scraper-task:previous

# Rollback Terraform
terraform apply -var="image_tag=previous_version"
```

## 📚 Additional Resources

- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [AWS ECS Documentation](https://docs.aws.amazon.com/ecs/)
- [Terraform Documentation](https://www.terraform.io/docs)

---

This Docker and CI/CD setup provides a robust, scalable, and maintainable deployment pipeline for the AI-Driven Web Scraper project.
