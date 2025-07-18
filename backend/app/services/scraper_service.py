import asyncio
import logging
from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

from ..models import Product, ScrapingJob, ScrapingSession, PriceHistory
from ..schemas import ScrapingRequest, JobStatus
from .ai_service import AIService
from .site_scrapers import AmazonScraper, BestBuyScraper, WalmartScraper

logger = logging.getLogger(__name__)


class ScraperService:
    def __init__(self):
        self.ai_service = AIService()
        self.scrapers = {
            "amazon": AmazonScraper(),
            "bestbuy": BestBuyScraper(),
            "walmart": WalmartScraper()
        }
        self.active_jobs: Dict[str, asyncio.Task] = {}

    async def run_scraping_job(self, job: ScrapingJob, request: ScrapingRequest):
        """Run a scraping job asynchronously"""
        try:
            logger.info(f"Starting scraping job {job.job_id}")

            # Update job status
            job.status = "running"
            job.started_at = datetime.utcnow()

            # Create scraping sessions for each site
            sessions = []
            for site in request.target_sites:
                session = ScrapingSession(
                    job_id=job.job_id,
                    site=site,
                    url=str(request.urls[0]),  # Simplified for demo
                    status="pending"
                )
                sessions.append(session)

            # Run scraping for each site concurrently
            tasks = []
            for session in sessions:
                task = asyncio.create_task(
                    self._scrape_site(session, request)
                )
                tasks.append(task)

            # Wait for all scraping tasks to complete
            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Process results
            total_products = 0
            for result in results:
                if isinstance(result, Exception):
                    logger.error(f"Scraping error: {result}")
                    job.error_message = str(result)
                else:
                    total_products += result

            # Update job completion
            job.products_scraped = total_products
            job.status = "completed"
            job.completed_at = datetime.utcnow()
            job.progress = 1.0

            logger.info(
                f"Scraping job {job.job_id} completed with {total_products} products")

        except Exception as e:
            logger.error(f"Scraping job {job.job_id} failed: {e}")
            job.status = "failed"
            job.error_message = str(e)
            job.completed_at = datetime.utcnow()

    async def _scrape_site(self, session: ScrapingSession, request: ScrapingRequest) -> int:
        """Scrape a specific site"""
        try:
            session.status = "running"
            session.started_at = datetime.utcnow()

            # Get appropriate scraper
            scraper = self.scrapers.get(session.site)
            if not scraper:
                raise ValueError(
                    f"No scraper available for site: {session.site}")

            # Scrape products
            products = await scraper.scrape_products(
                url=session.url,
                max_products=request.max_products,
                use_ai_parsing=request.use_ai_parsing
            )

            # Save products to database
            saved_count = await self._save_products(products, session.site)

            # Update session
            session.status = "completed"
            session.completed_at = datetime.utcnow()
            session.products_found = saved_count

            logger.info(f"Scraped {saved_count} products from {session.site}")
            return saved_count

        except Exception as e:
            logger.error(f"Error scraping {session.site}: {e}")
            session.status = "failed"
            session.error_message = str(e)
            session.completed_at = datetime.utcnow()
            raise

    async def _save_products(self, products: List[Dict], competitor: str) -> int:
        """Save scraped products to database"""
        # This would be implemented with actual database session
        # For now, return mock count
        return len(products)

    async def get_job_status(self, job_id: str) -> Optional[ScrapingJob]:
        """Get status of a scraping job"""
        # This would query the database
        # For now, return mock data
        return ScrapingJob(
            job_id=job_id,
            status="running",
            progress=0.65,
            products_scraped=32
        )

    async def get_products(self, db: AsyncSession, limit: int = 100, offset: int = 0) -> List[Product]:
        """Get scraped products with pagination"""
        # This would query the database
        # For now, return mock data
        return [
            Product(
                id=1,
                name="iPhone 15 Pro Max",
                price=1199.99,
                competitor="amazon",
                url="https://example.com",
                scraped_at=datetime.utcnow(),
                confidence_score=0.95
            ),
            Product(
                id=2,
                name="iPhone 15 Pro Max",
                price=1199.99,
                competitor="bestbuy",
                url="https://example.com",
                scraped_at=datetime.utcnow(),
                confidence_score=0.92
            )
        ]

    async def generate_competitive_analysis(self) -> Dict[str, Any]:
        """Generate competitive analysis of scraped data"""
        # This would analyze the database
        # For now, return mock analysis
        return {
            "total_products": 150,
            "average_price": 899.99,
            "price_range": {"min": 699.99, "max": 1299.99},
            "price_comparison": {
                "amazon": {"avg_price": 899.99, "count": 50},
                "bestbuy": {"avg_price": 899.99, "count": 50},
                "walmart": {"avg_price": 899.99, "count": 50}
            },
            "market_insights": [
                "Amazon has the most competitive pricing",
                "Best Buy offers the best customer service ratings",
                "Walmart has the fastest shipping options"
            ]
        }

    async def start_demo_scraping(self, request: ScrapingRequest) -> ScrapingJob:
        """Start a demo scraping session"""
        # Create demo job
        job = ScrapingJob(
            status="running",
            target_urls=[str(url) for url in request.urls],
            target_sites=request.target_sites,
            max_products=request.max_products
        )

        # Start scraping in background
        asyncio.create_task(self.run_scraping_job(job, request))

        return job

    async def cleanup(self):
        """Cleanup resources"""
        # Cancel active jobs
        for task in self.active_jobs.values():
            task.cancel()

        # Cleanup scrapers
        for scraper in self.scrapers.values():
            await scraper.cleanup()
