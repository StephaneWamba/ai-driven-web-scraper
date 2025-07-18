# AI-Driven E-Commerce Intelligence Scraper

A portfolio project demonstrating advanced web scraping with AI-powered data extraction for competitive price intelligence.

## Features

- **Real-time Price Monitoring**: Live scraping of e-commerce sites
- **AI-Powered Data Extraction**: Intelligent parsing with OpenAI
- **Competitive Analysis Dashboard**: React frontend with FastAPI backend
- **Cloud Infrastructure**: AWS deployment with Terraform
- **Anti-Bot Evasion**: Advanced scraping techniques

## Tech Stack

- **Frontend**: React + TypeScript
- **Backend**: FastAPI + Python
- **Infrastructure**: Terraform + AWS
- **Scraping**: Playwright + Crawl4AI
- **AI**: OpenAI GPT-4
- **Database**: PostgreSQL (RDS)

## Quick Start

1. **Setup Infrastructure**:

   ```bash
   cd terraform
   terraform init
   terraform plan
   terraform apply
   ```

2. **Backend Setup**:

   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```

3. **Frontend Setup**:
   ```bash
   cd frontend
   npm install
   npm start
   ```

## Project Structure

```
├── terraform/          # Infrastructure as Code
├── backend/           # FastAPI application
├── frontend/          # React application
├── scraper/           # Core scraping logic
└── docs/             # Documentation
```

## Portfolio Highlights

- **Business Value**: Competitive price intelligence with ROI calculations
- **Technical Complexity**: AI-powered parsing, anti-bot strategies
- **Live Demo**: Real-time scraping dashboard
- **Scalable Architecture**: Cloud-native design
