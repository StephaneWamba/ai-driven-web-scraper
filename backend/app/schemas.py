from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class SiteType(str, Enum):
    AMAZON = "amazon"
    BESTBUY = "bestbuy"
    WALMART = "walmart"


class JobStatusEnum(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class ScrapingRequest(BaseModel):
    urls: List[HttpUrl] = Field(..., description="List of URLs to scrape")
    target_sites: List[SiteType] = Field(...,
                                         description="Target e-commerce sites")
    max_products: int = Field(
        default=100, ge=1, le=1000, description="Maximum products to scrape")
    use_ai_parsing: bool = Field(
        default=True, description="Use AI for intelligent data extraction")
    include_images: bool = Field(
        default=True, description="Include product images")
    include_reviews: bool = Field(
        default=False, description="Include product reviews")

    class Config:
        schema_extra = {
            "example": {
                "urls": [
                    "https://www.amazon.com/s?k=iphone+15",
                    "https://www.bestbuy.com/site/searchpage.jsp?st=iphone+15"
                ],
                "target_sites": ["amazon", "bestbuy"],
                "max_products": 50,
                "use_ai_parsing": True
            }
        }


class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    original_price: Optional[float] = None
    currency: str = "USD"
    competitor: str
    url: str
    image_url: Optional[str] = None
    rating: Optional[float] = None
    review_count: Optional[int] = None
    availability: Optional[str] = None
    scraped_at: datetime
    confidence_score: float
    metadata: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": 1,
                "name": "iPhone 15 Pro Max",
                "price": 1199.99,
                "original_price": 1299.99,
                "currency": "USD",
                "competitor": "amazon",
                "url": "https://www.amazon.com/iPhone-15-Pro-Max/dp/B0CM5KJ8QZ",
                "image_url": "https://example.com/image.jpg",
                "rating": 4.5,
                "review_count": 1250,
                "availability": "In Stock",
                "scraped_at": "2024-01-01T12:00:00Z",
                "confidence_score": 0.95
            }
        }


class JobStatus(BaseModel):
    job_id: str
    status: JobStatusEnum
    message: str
    progress: Optional[float] = Field(
        None, ge=0.0, le=1.0, description="Progress from 0.0 to 1.0")
    products_scraped: Optional[int] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "job_id": "550e8400-e29b-41d4-a716-446655440000",
                "status": "running",
                "message": "Scraping in progress",
                "progress": 0.65,
                "products_scraped": 32,
                "started_at": "2024-01-01T12:00:00Z"
            }
        }


class CompetitiveAnalysis(BaseModel):
    total_products: int
    average_price: float
    price_range: Dict[str, float]
    best_deals: List[ProductResponse]
    price_comparison: Dict[str, Dict[str, float]]
    market_insights: List[str]
    generated_at: datetime

    class Config:
        schema_extra = {
            "example": {
                "total_products": 150,
                "average_price": 899.99,
                "price_range": {"min": 699.99, "max": 1299.99},
                "best_deals": [],
                "price_comparison": {
                    "amazon": {"avg_price": 899.99, "count": 50},
                    "bestbuy": {"avg_price": 899.99, "count": 50},
                    "walmart": {"avg_price": 899.99, "count": 50}
                },
                "market_insights": [
                    "Amazon has the most competitive pricing",
                    "Best Buy offers the best customer service ratings"
                ],
                "generated_at": "2024-01-01T12:00:00Z"
            }
        }


class AlertConfig(BaseModel):
    price_threshold: float = Field(..., gt=0,
                                   description="Price threshold for alerts")
    email: Optional[str] = Field(
        None, description="Email for price drop notifications")
    product_name: Optional[str] = None
    competitor: Optional[SiteType] = None
    is_active: bool = True

    class Config:
        schema_extra = {
            "example": {
                "price_threshold": 999.99,
                "email": "user@example.com",
                "product_name": "iPhone 15",
                "competitor": "amazon"
            }
        }


class DemoRequest(BaseModel):
    search_term: str = Field(
        default="iphone 15", description="Search term for demo")
    max_products: int = Field(default=10, ge=1, le=50,
                              description="Maximum products for demo")
    sites: List[SiteType] = Field(
        default=[SiteType.AMAZON, SiteType.BESTBUY, SiteType.WALMART])

    class Config:
        schema_extra = {
            "example": {
                "search_term": "iphone 15",
                "max_products": 10,
                "sites": ["amazon", "bestbuy", "walmart"]
            }
        }


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        schema_extra = {
            "example": {
                "error": "Scraping failed",
                "detail": "Rate limit exceeded",
                "timestamp": "2024-01-01T12:00:00Z"
            }
        }
