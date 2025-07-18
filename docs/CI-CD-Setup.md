# CI/CD Pipeline Setup Guide

This guide explains how to set up the CI/CD pipeline for the AI-Driven Web Scraper project using GitHub Actions.

## Overview

The CI/CD pipeline automatically:

- Runs tests on both backend and frontend
- Builds Docker images
- Deploys to the EC2 instance
- Performs security scans
- Provides deployment status notifications

## Prerequisites

1. **GitHub Repository**: Ensure your code is in a GitHub repository
2. **AWS EC2 Instance**: The infrastructure should be deployed via Terraform
3. **SSH Key**: You need an SSH key to access the EC2 instance

## GitHub Secrets Setup

Navigate to your GitHub repository → Settings → Secrets and variables → Actions, then add the following secrets:

### Required Secrets

| Secret Name             | Description                            | Example                                    |
| ----------------------- | -------------------------------------- | ------------------------------------------ |
| `AWS_ACCESS_KEY_ID`     | AWS access key for deployment          | `AKIAIOSFODNN7EXAMPLE`                     |
| `AWS_SECRET_ACCESS_KEY` | AWS secret access key                  | `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY` |
| `EC2_SSH_KEY`           | Private SSH key content for EC2 access | `-----BEGIN RSA PRIVATE KEY-----...`       |

### Optional Secrets

| Secret Name     | Description                         | Example                                |
| --------------- | ----------------------------------- | -------------------------------------- |
| `SLACK_WEBHOOK` | Slack webhook URL for notifications | `https://hooks.slack.com/services/...` |
| `CODECOV_TOKEN` | Codecov token for coverage reports  | `abc123def456...`                      |

## SSH Key Setup

1. **Generate SSH Key** (if you don't have one):

   ```bash
   ssh-keygen -t rsa -b 4096 -C "your-email@example.com" -f ~/.ssh/ai-scraper
   ```

2. **Add Public Key to EC2 Instance**:

   ```bash
   # Copy the public key content
   cat ~/.ssh/ai-scraper.pub

   # Add to EC2 instance authorized_keys
   ssh -i your-existing-key.pem ubuntu@54.165.182.47
   echo "your-public-key-content" >> ~/.ssh/authorized_keys
   ```

3. **Add Private Key to GitHub Secrets**:
   - Copy the content of `~/.ssh/ai-scraper`
   - Add it as the `EC2_SSH_KEY` secret in GitHub

## Pipeline Configuration

The pipeline is configured in `.github/workflows/ci-cd.yml` and includes:

### Jobs

1. **test-backend**: Runs Python tests with coverage
2. **test-frontend**: Runs React tests with coverage
3. **build-and-deploy**: Builds and deploys to EC2
4. **security-scan**: Runs Trivy vulnerability scanner
5. **notify**: Provides deployment status

### Triggers

- **Push to main/develop**: Triggers full pipeline
- **Pull Request to main**: Runs tests only

## Deployment Process

1. **Code Push**: When code is pushed to main branch
2. **Tests**: Backend and frontend tests run in parallel
3. **Build**: Docker images are built
4. **Deploy**: Code is deployed to EC2 instance via SSH
5. **Health Check**: Services are verified to be running
6. **Security Scan**: Vulnerability scan is performed
7. **Notification**: Deployment status is reported

## Manual Deployment

You can also deploy manually using the deployment script:

```bash
# Make script executable
chmod +x scripts/deploy.sh

# Set SSH key path
export SSH_KEY=~/.ssh/ai-scraper

# Run deployment
./scripts/deploy.sh
```

## Monitoring

### Deployment Status

- Check GitHub Actions tab for pipeline status
- View logs for detailed information about each step

### Application Health

- Frontend: http://54.165.182.47
- Backend API: http://54.165.182.47:8000
- API Documentation: http://54.165.182.47:8000/docs
- Health Check: http://54.165.182.47:8000/health

### Logs

```bash
# Backend logs
ssh -i ~/.ssh/ai-scraper ubuntu@54.165.182.47
sudo journalctl -u ai-scraper-backend -f

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

## Troubleshooting

### Common Issues

1. **SSH Connection Failed**

   - Verify SSH key is correct in GitHub secrets
   - Check EC2 security group allows SSH (port 22)
   - Ensure public key is in authorized_keys

2. **Deployment Fails**

   - Check server disk space: `df -h`
   - Verify services are running: `sudo systemctl status ai-scraper-backend`
   - Check logs for errors

3. **Health Check Fails**
   - Verify backend is running: `curl http://localhost:8000/health`
   - Check nginx configuration: `sudo nginx -t`
   - Restart services if needed

### Debug Commands

```bash
# Check service status
sudo systemctl status ai-scraper-backend
sudo systemctl status nginx

# View recent logs
sudo journalctl -u ai-scraper-backend --since "10 minutes ago"
sudo journalctl -u nginx --since "10 minutes ago"

# Test connectivity
curl -v http://localhost:8000/health
curl -v http://localhost

# Check disk space
df -h
du -sh /home/ubuntu/ai-scraper/*
```

## Security Considerations

1. **SSH Key Security**: Use a dedicated SSH key for deployments
2. **AWS Credentials**: Use IAM roles with minimal required permissions
3. **Secrets Management**: Never commit secrets to the repository
4. **Network Security**: Ensure EC2 security groups are properly configured

## Cost Optimization

1. **EC2 Instance**: Use t3.micro for development, scale up for production
2. **GitHub Actions**: Use self-hosted runners for cost savings
3. **Monitoring**: Set up CloudWatch alarms for cost monitoring

## Next Steps

1. Set up monitoring and alerting
2. Configure automatic backups
3. Implement blue-green deployments
4. Add performance testing
5. Set up staging environment
