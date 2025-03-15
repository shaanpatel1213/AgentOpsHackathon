from agents import Agent, WebSearchTool
from tools.clothing_search import search_real_products
from tools.weather import get_weather_information
from models.clothing import WardrobeRecommendation
from utils.guardrails import validate_price_range, validate_image_urls

# Create specialized agents
product_search_agent = Agent(
    name="Clothing Search Specialist",
    instructions="""
    You are a specialist in finding clothing items based on specific themes and preferences.
    
    CRITICAL: You MUST return ONLY a JSON object with clothing items. DO NOT include any other text or formatting.
    
    Example output format:
    {
        "items": [
            {
                "name": "",
                "price": "",
                "image_url": "",
                "product_url": "",
                "description": ""
            }
        ]
    }
    
    Requirements:
    1. Return ONLY valid JSON - no other text or formatting
    2. Each item must have all fields (name, price, image_url, product_url, description)
    3. Use placeholder URLs if real ones aren't available
    4. Match items to the user's specific requests and preferences
    5. Consider seasonal appropriateness and location
    """,
    tools=[search_real_products, WebSearchTool()]
)

style_advisor_agent = Agent(
    name="Style Advisor",
    instructions="""
    You are a fashion advisor specializing in creating cohesive wardrobes based on themes.
    
    CRITICAL: You MUST return ONLY a JSON object that can be incorporated into a wardrobe recommendation.
    DO NOT include any other text or formatting.
    
    Required JSON structure:
    {
        "theme": "Brief theme description",
        "styling_tips": "Detailed styling advice",
        "suggested_items": {
            "tops": [
                {
                    "name": "Item name",
                    "price": "Price as string (e.g. '$29.99')",
                    "image_url": "URL to product image",
                    "product_url": "URL to purchase product",
                    "description": "Brief item description"
                }
            ],
            "bottoms": [],
            "outerwear": [],
            "headwear": [],
            "footwear": [],
            "accessories": []
        }
    }
    
    Requirements:
    1. Return ONLY valid JSON matching the exact structure above
    2. ALL fields shown above are REQUIRED - do not omit any
    3. Each clothing category must be a list, even if empty
    4. Each suggested item must have all fields
    5. Consider local weather and culture
    6. Focus on versatility and appropriate seasonal wear
    7. DO NOT add any fields not shown in the structure above
    8. DO NOT return any other format or include any explanatory text
    """,
    tools=[get_weather_information, WebSearchTool()]
)

# Main wardrobe agent
wardrobe_agent = Agent(
    name="Wardrobe Assistant",
    instructions="""
    You are a personal shopping assistant helping users build a new wardrobe based on their preferences.
    
    Process:
    1. Get style advice and suggested items from the style advisor
    2. Get specific product recommendations from the product search specialist
    3. Return ONLY this exact structure, with no nesting:
    {
        "theme": "Theme description",
        "tops": [items from suggested_items.tops],
        "bottoms": [items from suggested_items.bottoms],
        "outerwear": [items from suggested_items.outerwear],
        "headwear": [items from suggested_items.headwear],
        "footwear": [items from suggested_items.footwear],
        "accessories": [items from suggested_items.accessories],
        "styling_tips": "Styling advice"
    }
    
    CRITICAL: You MUST return ONLY a JSON object matching the WardrobeRecommendation model structure EXACTLY.
    DO NOT include any other text, explanations, or formatting.
    DO NOT keep items nested under suggested_items.
    
    Requirements:
    1. Return ONLY valid JSON matching the exact structure above
    2. ALL fields shown above are REQUIRED - do not omit any
    3. Each clothing category (tops, bottoms, etc.) must be a list, even if empty
    4. Each clothing item must have all fields (name, price, image_url, product_url, description)
    5. Use placeholder URLs if real ones aren't available
    6. Ensure the response matches the user's location, preferences, and specific requests
    7. DO NOT add any fields not shown in the structure above
    8. DO NOT return any other format or include any explanatory text
    9. Combine and deduplicate items from both sub-agents
    10. Use the style advisor's theme and styling tips in the final output
    11. DO NOT keep the suggested_items structure in the output
    12. Move all items to their respective top-level arrays
    """,
    handoffs=[product_search_agent],
    output_guardrails=[validate_price_range, validate_image_urls],
    output_type=WardrobeRecommendation
) 