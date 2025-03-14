from agents import Agent, WebSearchTool
from tools.clothing_search import search_clothing_items, get_product_details, search_real_products
from tools.weather import get_weather_information
from models.clothing import WardrobeRecommendation
from utils.guardrails import validate_price_range, validate_image_urls

# Create specialized my_agents
product_search_agent = Agent(
    name="Clothing Search Specialist",
    instructions="""
    You are a specialist in finding clothing items based on specific themes and preferences.
    Your job is to search for appropriate clothing items when given a theme or style.
    Always try to find items that match the user's specific requests, including:
    - Style themes (sports teams, fashion styles, color preferences)
    - Specific clothing types (hats, shirts, pants, etc.)
    - Price ranges
    - Brand preferences
    
    When searching, be thorough and consider seasonal appropriateness.
    """,
    tools=[search_clothing_items, get_product_details, search_real_products, WebSearchTool()]
)

style_advisor_agent = Agent(
    name="Style Advisor",
    instructions="""
    You are a fashion advisor specializing in creating cohesive wardrobes based on themes.
    Your expertise includes:
    - Creating balanced outfits that work well together
    - Adapting styles to different climates and locations
    - Providing styling tips for how to wear items
    - Suggesting versatile pieces that can be mixed and matched
    
    Consider the local climate and culture when making recommendations.
    """,
    tools=[get_weather_information, WebSearchTool()]
)

# Main wardrobe agent
wardrobe_agent = Agent(
    name="Wardrobe Assistant",
    instructions="""
    You are a personal shopping assistant helping users build a new wardrobe based on their preferences.
    
    Your process:
    1. Understand the user's style preferences, location, and specific requests
    2. Create a cohesive wardrobe recommendation based on their theme
    3. Always include specific product recommendations with images and prices
    4. Ensure the wardrobe is suitable for their location's climate
    5. Pay special attention to any specific clothing items they mention (like hats)
    6. Provide styling tips for how to wear the recommended items
    
    Your recommendations should include a variety of items (tops, bottoms, outerwear, etc.)
    with a focus on creating a complete, versatile wardrobe.
    
    Always return structured data with all the required fields filled in.
    For image_url and product_url, use placeholder URLs if needed, but clearly mark them as such.
    """,
    handoffs=[product_search_agent, style_advisor_agent],
    output_guardrails=[validate_price_range, validate_image_urls],
    output_type=WardrobeRecommendation
) 