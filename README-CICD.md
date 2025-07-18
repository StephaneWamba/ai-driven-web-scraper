# CI/CD Pipeline Setup - AI-Driven Web Scraper

## 🚀 Quick Start

Your CI/CD pipeline is now fully configured! Here's what you need to do to activate it:

### 1. GitHub Repository Setup

1. **Push your code to GitHub**:

   ```bash
   git add .
   git commit -m "feat: Complete CI/CD pipeline setup"
   git push origin main
   ```

2. **Add GitHub Secrets** (Repository → Settings → Secrets and variables → Actions):
   - `AWS_ACCESS_KEY_ID`: Your AWS access key
   - `AWS_SECRET_ACCESS_KEY`: Your AWS secret key
   - `EC2_SSH_KEY`: Your private SSH key content

### 2. SSH Key Setup

Generate and configure SSH access:

```bash
# Generate SSH key
ssh-keygen -t rsa -b 4096 -C "your-email@example.com" -f ~/.ssh/ai-scraper

# Add public key to EC2 instance
cat ~/.ssh/ai-scraper.pub
# Copy this content and add to ~/.ssh/authorized_keys on your EC2 instance

# Add private key to GitHub secrets
cat ~/.ssh/ai-scraper
# Copy this content and add as EC2_SSH_KEY secret
```

## 📋 What's Included

### ✅ Infrastructure (Deployed)

- **EC2 Instance**: `54.165.182.47` (t3.micro)
- **RDS Database**: PostgreSQL 14
- **S3 Bucket**: Data storage
- **Security Groups**: Properly configured
- **VPC & Networking**: Isolated and secure

### ✅ CI/CD Pipeline

- **GitHub Actions Workflow**: `.github/workflows/ci-cd.yml`
- **Automated Testing**: Backend and frontend tests
- **Security Scanning**: Trivy vulnerability scanner
- **Deployment**: Automatic deployment to EC2
- **Health Checks**: Service verification
- **Notifications**: Deployment status reporting

### ✅ Application Services

- **Backend**: FastAPI running on port 8000
- **Frontend**: React app served by nginx on port 80
- **Systemd Services**: Automatic startup and restart
- **Nginx Configuration**: Reverse proxy setup

## 🌐 Access URLs

| Service          | URL                              | Status  |
| ---------------- | -------------------------------- | ------- |
| **Frontend**     | http://54.165.182.47             | ✅ Live |
| **Backend API**  | http://54.165.182.47:8000        | ✅ Live |
| **API Docs**     | http://54.165.182.47:8000/docs   | ✅ Live |
| **Health Check** | http://54.165.182.47:8000/health | ✅ Live |

## 🔄 Deployment Process

### Automatic Deployment (GitHub Actions)

1. **Push to main branch** → Triggers pipeline
2. **Run tests** → Backend and frontend tests
3. **Build images** → Docker image creation
4. **Deploy to EC2** → SSH deployment
5. **Health check** → Service verification
6. **Security scan** → Vulnerability check
7. **Notify** → Status reporting

### Manual Deployment

```bash
# Use the deployment script
chmod +x scripts/deploy.sh
export SSH_KEY=~/.ssh/ai-scraper
./scripts/deploy.sh
```

## 📊 Monitoring & Logs

### Service Status

```bash
# Check backend service
sudo systemctl status ai-scraper-backend

# Check nginx service
sudo systemctl status nginx
```

### View Logs

```bash
# Backend logs
sudo journalctl -u ai-scraper-backend -f

# Nginx access logs
sudo tail -f /var/log/nginx/access.log

# Nginx error logs
sudo tail -f /var/log/nginx/error.log
```

### Health Monitoring

```bash
# Test backend health
curl http://54.165.182.47:8000/health

# Test frontend
curl http://54.165.182.47
```

## 🛠️ Troubleshooting

### Common Issues

1. **Pipeline Fails on SSH**

   - Verify `EC2_SSH_KEY` secret is correct
   - Check public key is in EC2 `authorized_keys`
   - Ensure security group allows SSH (port 22)

2. **Deployment Fails**

   - Check disk space: `df -h`
   - Verify services: `sudo systemctl status ai-scraper-backend`
   - Check logs for errors

3. **Health Check Fails**
   - Restart services: `sudo systemctl restart ai-scraper-backend`
   - Check nginx: `sudo nginx -t && sudo systemctl restart nginx`

### Debug Commands

```bash
# Connect to server
ssh -i ~/.ssh/ai-scraper ubuntu@54.165.182.47

# Check application directory
ls -la /home/ubuntu/ai-scraper/

# Check service logs
sudo journalctl -u ai-scraper-backend --since "5 minutes ago"

# Test local connectivity
curl http://localhost:8000/health
```

## 🔧 Configuration Files

### Key Files

- **CI/CD Pipeline**: `.github/workflows/ci-cd.yml`
- **Deployment Script**: `scripts/deploy.sh`
- **Infrastructure**: `terraform/` directory
- **Docker Configs**: `Dockerfile.backend`, `Dockerfile.frontend`
- **Nginx Config**: Configured in user data script

### Environment Variables

The application uses these environment variables:

- `DATABASE_URL`: PostgreSQL connection string
- `OPENAI_API_KEY`: OpenAI API key for AI features
- `AWS_REGION`: AWS region (us-east-1)
- `S3_BUCKET_NAME`: S3 bucket for data storage

## 📈 Next Steps

### Immediate Actions

1. **Set up GitHub secrets** (required for pipeline)
2. **Configure SSH access** (required for deployment)
3. **Test the pipeline** by pushing to main branch

### Future Enhancements

1. **Monitoring**: Set up CloudWatch alarms
2. **Backups**: Configure automatic database backups
3. **SSL**: Add HTTPS with Let's Encrypt
4. **Domain**: Configure custom domain
5. **Scaling**: Set up auto-scaling groups
6. **Staging**: Create staging environment

## 💰 Cost Optimization

### Current Costs (Monthly)

- **EC2 t3.micro**: ~$8-10/month
- **RDS t3.micro**: ~$15-20/month
- **S3 Storage**: ~$0.02/GB/month
- **Data Transfer**: Minimal for small traffic

### Cost Reduction Tips

1. **Use Spot Instances** for non-critical workloads
2. **Schedule shutdowns** during off-hours
3. **Monitor usage** with CloudWatch
4. **Use reserved instances** for predictable workloads

## 🔒 Security Best Practices

1. **SSH Keys**: Use dedicated deployment keys
2. **IAM Roles**: Minimal required permissions
3. **Security Groups**: Restrict access to necessary ports
4. **Secrets**: Never commit secrets to repository
5. **Updates**: Regular security updates
6. **Monitoring**: Log monitoring and alerting

## 📞 Support

If you encounter issues:

1. **Check logs** using the commands above
2. **Review GitHub Actions** for pipeline errors
3. **Verify infrastructure** with `terraform show`
4. **Test connectivity** to all services

---

**🎉 Congratulations!** Your AI-Driven Web Scraper now has a complete CI/CD pipeline that will automatically deploy updates whenever you push to the main branch.
