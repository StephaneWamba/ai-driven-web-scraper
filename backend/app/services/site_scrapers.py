import asyncio
import logging
import random
import time
from typing import List, Dict, Any, Optional
from playwright.async_api import async_playwright, Browser, Page
import re

logger = logging.getLogger(__name__)


class BaseScraper:
    """Base scraper class with common functionality"""

    def __init__(self):
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ]

    async def setup_browser(self):
        """Setup Playwright browser with anti-detection measures"""
        if not self.browser:
            playwright = await async_playwright().start()
            self.browser = await playwright.chromium.launch(
                headless=True,
                args=[
                    "--no-sandbox",
                    "--disable-blink-features=AutomationControlled",
                    "--disable-dev-shm-usage"
                ]
            )

    async def create_page(self) -> Page:
        """Create a new page with anti-bot measures"""
        await self.setup_browser()

        self.page = await self.browser.new_page()

        # Set random user agent
        user_agent = random.choice(self.user_agents)
        await self.page.set_extra_http_headers({"User-Agent": user_agent})

        # Hide automation indicators
        await self.page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
        """)

        return self.page

    async def random_delay(self, min_delay: float = 1.0, max_delay: float = 3.0):
        """Add random delay to mimic human behavior"""
        delay = random.uniform(min_delay, max_delay)
        await asyncio.sleep(delay)

    async def human_like_scroll(self, page: Page):
        """Scroll like a human user"""
        await page.evaluate("""
            window.scrollTo({
                top: document.body.scrollHeight,
                behavior: 'smooth'
            });
        """)
        await self.random_delay(2.0, 4.0)

    async def cleanup(self):
        """Cleanup browser resources"""
        if self.page:
            await self.page.close()
        if self.browser:
            await self.browser.close()


class AmazonScraper(BaseScraper):
    """Amazon-specific scraper"""

    async def scrape_products(self, url: str, max_products: int = 100, use_ai_parsing: bool = True) -> List[Dict[str, Any]]:
        """Scrape products from Amazon"""
        try:
            page = await self.create_page()

            # Navigate to URL
            await page.goto(url, wait_until="networkidle")
            await self.random_delay()

            # Handle cookie consent if present
            try:
                await page.click('[data-cel-widget="sp-cc-accept"]', timeout=5000)
            except:
                pass

            products = []
            product_elements = await page.query_selector_all('[data-component-type="s-search-result"]')

            for i, element in enumerate(product_elements[:max_products]):
                try:
                    product_data = await self._extract_product_data(element, page)
                    if product_data:
                        products.append(product_data)

                    if len(products) >= max_products:
                        break

                except Exception as e:
                    logger.error(f"Error extracting product {i}: {e}")
                    continue

            logger.info(f"Scraped {len(products)} products from Amazon")
            return products

        except Exception as e:
            logger.error(f"Amazon scraping failed: {e}")
            return []

    async def _extract_product_data(self, element, page) -> Optional[Dict[str, Any]]:
        """Extract product data from Amazon product element"""
        try:
            # Extract basic information
            name_elem = await element.query_selector('h2 a span')
            name = await name_elem.text_content() if name_elem else "Unknown Product"

            # Extract price
            price_elem = await element.query_selector('.a-price-whole')
            price_text = await price_elem.text_content() if price_elem else "0"
            price = float(re.sub(r'[^\d.]', '', price_text) or "0")

            # Extract rating
            rating_elem = await element.query_selector('.a-icon-alt')
            rating_text = await rating_elem.text_content() if rating_elem else "0"
            rating_match = re.search(r'(\d+\.?\d*)', rating_text)
            rating = float(rating_match.group(1)) if rating_match else None

            # Extract review count
            reviews_elem = await element.query_selector('a[href*="customerReviews"] span')
            reviews_text = await reviews_elem.text_content() if reviews_elem else "0"
            reviews_match = re.search(r'(\d+)', reviews_text.replace(',', ''))
            review_count = int(reviews_match.group(1)) if reviews_match else 0

            # Extract image URL
            img_elem = await element.query_selector('img.s-image')
            image_url = await img_elem.get_attribute('src') if img_elem else None

            # Extract product URL
            link_elem = await element.query_selector('h2 a')
            product_url = await link_elem.get_attribute('href') if link_elem else ""
            if product_url and not product_url.startswith('http'):
                product_url = f"https://www.amazon.com{product_url}"

            return {
                "name": name.strip(),
                "price": price,
                "rating": rating,
                "review_count": review_count,
                "image_url": image_url,
                "url": product_url,
                "competitor": "amazon",
                "availability": "In Stock"  # Default assumption
            }

        except Exception as e:
            logger.error(f"Error extracting Amazon product data: {e}")
            return None


class BestBuyScraper(BaseScraper):
    """Best Buy-specific scraper"""

    async def scrape_products(self, url: str, max_products: int = 100, use_ai_parsing: bool = True) -> List[Dict[str, Any]]:
        """Scrape products from Best Buy"""
        try:
            page = await self.create_page()

            # Navigate to URL
            await page.goto(url, wait_until="networkidle")
            await self.random_delay()

            products = []
            product_elements = await page.query_selector_all('.shop-sku-list-item')

            for i, element in enumerate(product_elements[:max_products]):
                try:
                    product_data = await self._extract_product_data(element, page)
                    if product_data:
                        products.append(product_data)

                    if len(products) >= max_products:
                        break

                except Exception as e:
                    logger.error(f"Error extracting Best Buy product {i}: {e}")
                    continue

            logger.info(f"Scraped {len(products)} products from Best Buy")
            return products

        except Exception as e:
            logger.error(f"Best Buy scraping failed: {e}")
            return []

    async def _extract_product_data(self, element, page) -> Optional[Dict[str, Any]]:
        """Extract product data from Best Buy product element"""
        try:
            # Extract name
            name_elem = await element.query_selector('h4 a')
            name = await name_elem.text_content() if name_elem else "Unknown Product"

            # Extract price
            price_elem = await element.query_selector('.priceView-customer-price span')
            price_text = await price_elem.text_content() if price_elem else "0"
            price = float(re.sub(r'[^\d.]', '', price_text) or "0")

            # Extract rating
            rating_elem = await element.query_selector('.c-ratings-reviews-v2 .c-ratings-reviews-v2__reviews')
            rating_text = await rating_elem.text_content() if rating_elem else "0"
            rating_match = re.search(r'(\d+\.?\d*)', rating_text)
            rating = float(rating_match.group(1)) if rating_match else None

            # Extract image URL
            img_elem = await element.query_selector('img')
            image_url = await img_elem.get_attribute('src') if img_elem else None

            # Extract product URL
            link_elem = await element.query_selector('h4 a')
            product_url = await link_elem.get_attribute('href') if link_elem else ""
            if product_url and not product_url.startswith('http'):
                product_url = f"https://www.bestbuy.com{product_url}"

            return {
                "name": name.strip(),
                "price": price,
                "rating": rating,
                "review_count": 0,  # Best Buy doesn't show review count in list
                "image_url": image_url,
                "url": product_url,
                "competitor": "bestbuy",
                "availability": "In Stock"
            }

        except Exception as e:
            logger.error(f"Error extracting Best Buy product data: {e}")
            return None


class WalmartScraper(BaseScraper):
    """Walmart-specific scraper"""

    async def scrape_products(self, url: str, max_products: int = 100, use_ai_parsing: bool = True) -> List[Dict[str, Any]]:
        """Scrape products from Walmart"""
        try:
            page = await self.create_page()

            # Navigate to URL
            await page.goto(url, wait_until="networkidle")
            await self.random_delay()

            products = []
            product_elements = await page.query_selector_all('[data-item-id]')

            for i, element in enumerate(product_elements[:max_products]):
                try:
                    product_data = await self._extract_product_data(element, page)
                    if product_data:
                        products.append(product_data)

                    if len(products) >= max_products:
                        break

                except Exception as e:
                    logger.error(f"Error extracting Walmart product {i}: {e}")
                    continue

            logger.info(f"Scraped {len(products)} products from Walmart")
            return products

        except Exception as e:
            logger.error(f"Walmart scraping failed: {e}")
            return []

    async def _extract_product_data(self, element, page) -> Optional[Dict[str, Any]]:
        """Extract product data from Walmart product element"""
        try:
            # Extract name
            name_elem = await element.query_selector('[data-testid="product-title"]')
            name = await name_elem.text_content() if name_elem else "Unknown Product"

            # Extract price
            price_elem = await element.query_selector('[data-testid="price-wrap"] span')
            price_text = await price_elem.text_content() if price_elem else "0"
            price = float(re.sub(r'[^\d.]', '', price_text) or "0")

            # Extract rating
            rating_elem = await element.query_selector('[data-testid="rating"]')
            rating_text = await rating_elem.text_content() if rating_elem else "0"
            rating_match = re.search(r'(\d+\.?\d*)', rating_text)
            rating = float(rating_match.group(1)) if rating_match else None

            # Extract image URL
            img_elem = await element.query_selector('img')
            image_url = await img_elem.get_attribute('src') if img_elem else None

            # Extract product URL
            link_elem = await element.query_selector('a')
            product_url = await link_elem.get_attribute('href') if link_elem else ""
            if product_url and not product_url.startswith('http'):
                product_url = f"https://www.walmart.com{product_url}"

            return {
                "name": name.strip(),
                "price": price,
                "rating": rating,
                "review_count": 0,  # Walmart doesn't show review count in list
                "image_url": image_url,
                "url": product_url,
                "competitor": "walmart",
                "availability": "In Stock"
            }

        except Exception as e:
            logger.error(f"Error extracting Walmart product data: {e}")
            return None
