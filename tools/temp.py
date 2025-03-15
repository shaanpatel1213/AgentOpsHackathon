from agents import function_tool
from typing import Optional

@function_tool
def search_clothing_items(
    theme: str, 
    item_type: str, 
    price_range: Optional[str] = None,
    brand: Optional[str] = None,
    gender: Optional[str] = None
):
    """
    Search for clothing items based on theme and type.
    
    Args:
        theme: Style theme (e.g., "Boston Red Sox fan", "minimalist", "bohemian")
        item_type: Type of clothing (e.g., "hat", "jersey", "jeans", "sneakers")
        price_range: Optional price range (e.g., "under $50", "$50-$100")
        brand: Optional brand preference
        gender: Optional gender preference for sizing/style
        
    Returns:
        List of items matching the criteria
    """
    # Create search query for logging
    search_query = f"{theme} {item_type}"
    if price_range:
        search_query += f" {price_range}"
    if brand:
        search_query += f" by {brand}"
    if gender:
        search_query += f" for {gender}"
    
    print(f"Searching for: {search_query}")
    
    # Mock response - in production, replace with actual API call
    return {
        "search_query": search_query,
        "results_count": 5,
        "message": f"Found 5 {item_type} items matching '{theme}' theme"
    }

@function_tool
def get_product_details(product_id: str, theme: str, item_type: str):
    """
    Get detailed information about a specific product.
    
    Args:
        product_id: Identifier for the product
        theme: The theme context to help generate appropriate mock data
        item_type: Type of item to help generate appropriate mock data
        
    Returns:
        Detailed product information including name, price, images, and URL
    """
    # Create price with some variation
    import random
    base_price = random.randint(20, 100)
    price = f"${base_price}.{random.randint(0, 99):02d}"
    
    # Create mock product name
    product_name = f"{theme.title()} {item_type.title()}"
    if "hat" in item_type.lower() or "cap" in item_type.lower():
        product_name = f"{theme.title()} Adjustable Cap"
    elif "shirt" in item_type.lower() or "jersey" in item_type.lower():
        product_name = f"{theme.title()} Graphic Tee"
    elif "hoodie" in item_type.lower() or "jacket" in item_type.lower():
        product_name = f"{theme.title()} Zip-Up Hoodie"
    
    # Generate mock URLs
    image_url = f"https://example.com/images/{theme.replace(' ', '-').lower()}-{item_type.lower()}.jpg"
    product_url = f"https://example.com/products/{product_id}"
    
    return {
        "product_id": product_id,
        "name": product_name,
        "price": price,
        "image_url": image_url,
        "product_url": product_url,
        "description": f"This {item_type} features {theme} styling with premium quality materials."
    }

@function_tool
def unused_function(query: str, item_type: str, max_results: int):
    """
    Search for real products using a web search API.
    
    Args:
        query: Search query including theme and item details
        item_type: Type of clothing item
        max_results: Maximum number of results to return
        
    Returns:
        List of real products with details
    """
    results = []
    for i in range(1, max_results + 1):
        item_id = f"{query.replace(' ', '-')}-{i}"
        results.append({
            "id": item_id,
            "name": f"{query.title()} {item_type.title()} - Style {i}",
            "price": f"${20*i}.99",
            "retailer": ["Amazon", "Nordstrom", "Macy's", "Target"][i % 4],
            "image_url": f"https://example.com/products/{item_id}.jpg",
            "product_url": f"https://example.com/shop/{item_id}"
        })
    
    return {
        "query": query,
        "item_type": item_type,
        "results": results
    } 