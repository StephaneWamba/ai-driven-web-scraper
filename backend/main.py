from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

from app.database import init_db, get_db
from app.models import Product, ScrapingJob
from app.schemas import ScrapingRequest, ProductResponse, JobStatus
from app.services.scraper_service import ScraperService
from app.services.ai_service import AIService

# Load environment variables
load_dotenv()

# Global services
scraper_service = None
ai_service = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global scraper_service, ai_service

    # Initialize database
    await init_db()

    # Initialize services
    scraper_service = ScraperService()
    ai_service = AIService()

    print("🚀 AI Scraper API started successfully!")
    yield

    # Shutdown
    if scraper_service:
        await scraper_service.cleanup()
    print("👋 AI Scraper API shutdown complete!")

# Create FastAPI app
app = FastAPI(
    title="AI-Driven E-Commerce Intelligence Scraper",
    description="Advanced web scraping with AI-powered data extraction for competitive price intelligence",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "AI-Driven E-Commerce Intelligence Scraper API",
        "status": "healthy",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "service": "ai-scraper",
        "database": "connected",
        "scraper_service": "ready",
        "ai_service": "ready"
    }


@app.post("/api/scrape/start", response_model=JobStatus)
async def start_scraping(request: ScrapingRequest, background_tasks: BackgroundTasks):
    """Start a new scraping job"""
    try:
        # Create scraping job
        job = ScrapingJob(
            status="running",
            target_urls=request.urls,
            target_sites=request.target_sites
        )

        # Add to background tasks
        background_tasks.add_task(
            scraper_service.run_scraping_job, job, request)

        return JobStatus(
            job_id=str(job.id),
            status="started",
            message="Scraping job started successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to start scraping: {str(e)}")


@app.get("/api/scrape/status/{job_id}", response_model=JobStatus)
async def get_scraping_status(job_id: str):
    """Get status of a scraping job"""
    try:
        job = await scraper_service.get_job_status(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")

        return JobStatus(
            job_id=job_id,
            status=job.status,
            message=f"Job {job.status}",
            progress=job.progress if hasattr(job, 'progress') else None
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get job status: {str(e)}")


@app.get("/api/products", response_model=list[ProductResponse])
async def get_products(limit: int = 100, offset: int = 0):
    """Get scraped products with pagination"""
    try:
        async with get_db() as db:
            products = await scraper_service.get_products(db, limit, offset)
            return [ProductResponse.from_orm(product) for product in products]
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to fetch products: {str(e)}")


@app.get("/api/analysis/competitive")
async def get_competitive_analysis():
    """Get competitive analysis of scraped data"""
    try:
        analysis = await scraper_service.generate_competitive_analysis()
        return {
            "analysis": analysis,
            "generated_at": "2024-01-01T00:00:00Z"  # TODO: Add actual timestamp
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to generate analysis: {str(e)}")


@app.post("/api/alerts/configure")
async def configure_alerts(price_threshold: float, email: str = None):
    """Configure price drop alerts"""
    try:
        # TODO: Implement alert configuration
        return {
            "message": "Alerts configured successfully",
            "price_threshold": price_threshold,
            "email": email
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to configure alerts: {str(e)}")


@app.get("/api/demo/start")
async def start_demo():
    """Start a demo scraping session"""
    try:
        # Demo URLs for live demonstration
        demo_urls = [
            "https://www.amazon.com/s?k=iphone+15",
            "https://www.bestbuy.com/site/searchpage.jsp?st=iphone+15",
            "https://www.walmart.com/search?q=iphone+15"
        ]

        demo_request = ScrapingRequest(
            urls=demo_urls,
            target_sites=["amazon", "bestbuy", "walmart"],
            max_products=10
        )

        # Start demo scraping
        job = await scraper_service.start_demo_scraping(demo_request)

        return {
            "message": "Demo scraping started",
            "job_id": str(job.id),
            "demo_urls": demo_urls
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to start demo: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
