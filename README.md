# AI-Driven Web Scraper Portfolio Project

> **🚀 Portfolio Project**: AI-Powered Web Scraper for E-commerce Intelligence

A comprehensive full-stack application demonstrating AI-powered web scraping for competitive price intelligence across major e-commerce platforms.

## ✨ Features

- **🤖 AI-Powered Scraping**: Uses OpenAI GPT-4 for intelligent data extraction
- **🛒 Multi-Platform Support**: Amazon, Best Buy, Walmart
- **📊 Real-Time Analytics**: Live price comparisons and market analysis
- **🎨 Modern UI**: React with TypeScript and Tailwind CSS
- **⚡ High Performance**: FastAPI backend with async processing
- **☁️ Cloud-Native**: AWS infrastructure with Terraform
- **🔄 CI/CD Pipeline**: Automated deployment with GitHub Actions

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend│    │  FastAPI Backend│    │  PostgreSQL DB  │
│   (TypeScript)  │◄──►│   (Python)      │◄──►│   (AWS RDS)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Nginx Proxy   │    │   AI Service    │    │   S3 Storage    │
│   (Port 80)     │    │  (OpenAI GPT-4) │    │   (Data Files)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- AWS CLI (for deployment)

### Local Development

```bash
# Clone the repository
git clone https://github.com/StephaneWamba/ai-driven-web-scraper.git
cd ai-driven-web-scraper

# Start with Docker Compose
docker-compose up -d

# Access the application
# Frontend: http://localhost
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Production Deployment

```bash
# Deploy infrastructure
cd terraform
terraform init
terraform apply -var="db_password=YourSecurePassword"

# Deploy application
./scripts/deploy.sh
```

## 📋 Project Structure

```
ai-driven-web-scraper/
├── backend/                 # FastAPI application
│   ├── app/
│   │   ├── services/       # Business logic
│   │   ├── models.py       # Database models
│   │   └── schemas.py      # Pydantic schemas
│   └── main.py             # Application entry point
├── frontend/               # React TypeScript app
│   ├── src/
│   │   ├── components/     # React components
│   │   └── App.tsx         # Main application
│   └── package.json
├── terraform/              # Infrastructure as Code
│   ├── main.tf            # AWS resources
│   └── variables.tf       # Configuration
├── scripts/               # Deployment scripts
├── docs/                  # Documentation
└── .github/workflows/     # CI/CD pipeline
```

## 🔧 Configuration

### Environment Variables

```bash
# Backend (.env)
DATABASE_URL=postgresql://user:pass@host:5432/db
OPENAI_API_KEY=your_openai_api_key
AWS_REGION=us-east-1
S3_BUCKET_NAME=your-bucket-name

# Frontend
REACT_APP_API_URL=http://localhost:8000
```

### AWS Services Used

- **EC2**: Application server (t3.micro)
- **RDS**: PostgreSQL database
- **S3**: Data storage
- **VPC**: Network isolation
- **Security Groups**: Access control

## 🧪 Testing

```bash
# Backend tests
cd backend
pip install -r requirements.txt
pytest

# Frontend tests
cd frontend
npm install
npm test
```

## 📊 Monitoring

### Health Checks

- **Backend**: `http://54.165.182.47:8000/health`
- **Frontend**: `http://54.165.182.47`

### Logs

```bash
# Backend logs
sudo journalctl -u ai-scraper-backend -f

# Nginx logs
sudo tail -f /var/log/nginx/access.log
```

## 🔒 Security

- **HTTPS**: SSL/TLS encryption (configure with Let's Encrypt)
- **Authentication**: JWT-based auth (planned)
- **Input Validation**: Pydantic schemas
- **Rate Limiting**: API protection
- **Secrets Management**: GitHub Secrets for CI/CD

## 💰 Cost Optimization

### Current Monthly Costs (~$30-40)

- **EC2 t3.micro**: ~$8-10
- **RDS t3.micro**: ~$15-20
- **S3 Storage**: ~$0.02/GB
- **Data Transfer**: Minimal

### Cost Reduction Tips

1. Use Spot Instances for non-critical workloads
2. Schedule shutdowns during off-hours
3. Monitor usage with CloudWatch
4. Use reserved instances for predictable workloads

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/StephaneWamba/ai-driven-web-scraper/issues)
- **Discussions**: [GitHub Discussions](https://github.com/StephaneWamba/ai-driven-web-scraper/discussions)

---

**🎯 Perfect for**: Portfolio demonstrations, client presentations, learning modern full-stack development, and showcasing AI integration in web applications.

**🔗 Repository**: [https://github.com/StephaneWamba/ai-driven-web-scraper](https://github.com/StephaneWamba/ai-driven-web-scraper)
