from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, JSON
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import ARRAY
from .database import Base
import uuid


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    price = Column(Float, nullable=False)
    original_price = Column(Float, nullable=True)
    currency = Column(String(3), default="USD")
    competitor = Column(String(50), nullable=False, index=True)
    url = Column(Text, nullable=False)
    image_url = Column(Text, nullable=True)
    rating = Column(Float, nullable=True)
    review_count = Column(Integer, nullable=True)
    availability = Column(String(50), nullable=True)
    scraped_at = Column(DateTime(timezone=True),
                        server_default=func.now(), index=True)
    confidence_score = Column(Float, default=1.0)
    metadata = Column(JSON, nullable=True)  # Store additional data

    def __repr__(self):
        return f"<Product(name='{self.name}', price={self.price}, competitor='{self.competitor}')>"


class ScrapingJob(Base):
    __tablename__ = "scraping_jobs"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String(36), unique=True, index=True,
                    default=lambda: str(uuid.uuid4()))
    # pending, running, completed, failed
    status = Column(String(20), nullable=False, default="pending")
    target_urls = Column(ARRAY(Text), nullable=False)
    target_sites = Column(ARRAY(String), nullable=False)
    max_products = Column(Integer, default=100)
    products_scraped = Column(Integer, default=0)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    error_message = Column(Text, nullable=True)
    progress = Column(Float, default=0.0)  # 0.0 to 1.0
    metadata = Column(JSON, nullable=True)

    def __repr__(self):
        return f"<ScrapingJob(id='{self.job_id}', status='{self.status}')>"


class PriceHistory(Base):
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, nullable=False, index=True)
    price = Column(Float, nullable=False)
    recorded_at = Column(DateTime(timezone=True),
                         server_default=func.now(), index=True)
    source = Column(String(50), nullable=False)  # amazon, bestbuy, walmart

    def __repr__(self):
        return f"<PriceHistory(product_id={self.product_id}, price={self.price}, source='{self.source}')>"


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), nullable=False)
    price_threshold = Column(Float, nullable=False)
    product_name = Column(String(255), nullable=True)
    competitor = Column(String(50), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Alert(email='{self.email}', threshold={self.price_threshold})>"


class ScrapingSession(Base):
    __tablename__ = "scraping_sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(36), unique=True, index=True,
                        default=lambda: str(uuid.uuid4()))
    job_id = Column(String(36), nullable=False, index=True)
    site = Column(String(50), nullable=False)
    url = Column(Text, nullable=False)
    status = Column(String(20), default="pending")
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    products_found = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)

    def __repr__(self):
        return f"<ScrapingSession(session_id='{self.session_id}', site='{self.site}')>"
