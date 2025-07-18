import os
import logging
from typing import Dict, Any, List, Optional
import openai
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


class AIService:
    def __init__(self):
        self.client = openai.AsyncOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            timeout=30.0
        )
        self.model = "gpt-4"  # or "gpt-3.5-turbo" for cost optimization

    async def extract_product_data(self, html_content: str, site: str) -> Dict[str, Any]:
        """Extract product data from HTML using AI"""
        try:
            prompt = self._create_extraction_prompt(html_content, site)

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert web scraping assistant. Extract product information from HTML content and return it as JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.1,
                max_tokens=1000
            )

            # Parse AI response
            content = response.choices[0].message.content
            extracted_data = self._parse_ai_response(content)

            # Add confidence score based on AI response quality
            confidence_score = self._calculate_confidence(
                response.usage, extracted_data)
            extracted_data["confidence_score"] = confidence_score

            logger.info(
                f"AI extracted data with confidence: {confidence_score}")
            return extracted_data

        except Exception as e:
            logger.error(f"AI extraction failed: {e}")
            return self._get_fallback_data()

    async def validate_product_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and clean product data using AI"""
        try:
            prompt = f"""
            Validate and clean this product data. Return only valid, cleaned data as JSON:
            
            {data}
            
            Rules:
            - Price must be a positive number
            - Name must be non-empty
            - URL must be valid
            - Remove any invalid or empty fields
            """

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a data validation expert. Clean and validate product data."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.1,
                max_tokens=500
            )

            content = response.choices[0].message.content
            validated_data = self._parse_ai_response(content)

            logger.info("AI validation completed")
            return validated_data

        except Exception as e:
            logger.error(f"AI validation failed: {e}")
            return data

    async def generate_market_insights(self, products: List[Dict[str, Any]]) -> List[str]:
        """Generate market insights from product data"""
        try:
            # Prepare product summary
            product_summary = self._prepare_product_summary(products)

            prompt = f"""
            Analyze this product data and provide 3-5 key market insights:
            
            {product_summary}
            
            Focus on:
            - Price trends and competitiveness
            - Market positioning
            - Customer preferences
            - Business opportunities
            
            Return insights as a JSON array of strings.
            """

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a market intelligence expert. Provide actionable insights from product data."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=800
            )

            content = response.choices[0].message.content
            insights = self._parse_ai_response(content)

            if isinstance(insights, list):
                return insights
            else:
                return ["Market analysis completed successfully"]

        except Exception as e:
            logger.error(f"AI insights generation failed: {e}")
            return ["Market analysis available", "Price comparison data ready"]

    def _create_extraction_prompt(self, html_content: str, site: str) -> str:
        """Create extraction prompt for specific site"""
        site_prompts = {
            "amazon": """
            Extract product information from this Amazon page HTML:
            - Product name
            - Current price
            - Original price (if on sale)
            - Rating (out of 5)
            - Number of reviews
            - Availability status
            - Product image URL
            
            HTML Content:
            {html_content}
            
            Return as JSON with these exact field names: name, price, original_price, rating, review_count, availability, image_url
            """,
            "bestbuy": """
            Extract product information from this Best Buy page HTML:
            - Product name
            - Current price
            - Original price (if on sale)
            - Rating (out of 5)
            - Number of reviews
            - Availability status
            - Product image URL
            
            HTML Content:
            {html_content}
            
            Return as JSON with these exact field names: name, price, original_price, rating, review_count, availability, image_url
            """,
            "walmart": """
            Extract product information from this Walmart page HTML:
            - Product name
            - Current price
            - Original price (if on sale)
            - Rating (out of 5)
            - Number of reviews
            - Availability status
            - Product image URL
            
            HTML Content:
            {html_content}
            
            Return as JSON with these exact field names: name, price, original_price, rating, review_count, availability, image_url
            """
        }

        return site_prompts.get(site, site_prompts["amazon"]).format(html_content=html_content[:2000])

    def _parse_ai_response(self, content: str) -> Dict[str, Any]:
        """Parse AI response and extract JSON"""
        try:
            import json
            # Try to extract JSON from response
            if "{" in content and "}" in content:
                start = content.find("{")
                end = content.rfind("}") + 1
                json_str = content[start:end]
                return json.loads(json_str)
            else:
                logger.warning("No JSON found in AI response")
                return {}
        except Exception as e:
            logger.error(f"Failed to parse AI response: {e}")
            return {}

    def _calculate_confidence(self, usage: Any, data: Dict[str, Any]) -> float:
        """Calculate confidence score based on AI response quality"""
        try:
            # Base confidence on token usage and data completeness
            base_confidence = 0.8

            # Adjust based on data completeness
            required_fields = ["name", "price"]
            present_fields = sum(
                1 for field in required_fields if field in data and data[field])
            completeness = present_fields / len(required_fields)

            # Adjust based on token usage (more tokens = more detailed analysis)
            if hasattr(usage, 'total_tokens'):
                token_confidence = min(usage.total_tokens / 1000, 1.0) * 0.2
            else:
                token_confidence = 0.1

            confidence = base_confidence * completeness + token_confidence
            return min(confidence, 1.0)

        except Exception as e:
            logger.error(f"Confidence calculation failed: {e}")
            return 0.5

    def _get_fallback_data(self) -> Dict[str, Any]:
        """Return fallback data when AI extraction fails"""
        return {
            "name": "Product Name Unavailable",
            "price": 0.0,
            "confidence_score": 0.0,
            "error": "AI extraction failed"
        }

    def _prepare_product_summary(self, products: List[Dict[str, Any]]) -> str:
        """Prepare product summary for AI analysis"""
        if not products:
            return "No products available for analysis"

        summary = f"Total products: {len(products)}\n"

        # Price statistics
        prices = [p.get("price", 0) for p in products if p.get("price")]
        if prices:
            summary += f"Average price: ${sum(prices)/len(prices):.2f}\n"
            summary += f"Price range: ${min(prices):.2f} - ${max(prices):.2f}\n"

        # Competitor breakdown
        competitors = {}
        for product in products:
            comp = product.get("competitor", "unknown")
            competitors[comp] = competitors.get(comp, 0) + 1

        summary += "Products by competitor:\n"
        for comp, count in competitors.items():
            summary += f"- {comp}: {count} products\n"

        return summary
