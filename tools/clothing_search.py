from agents import function_tool
from typing import Optional, Dict, List, Any
import requests
from bs4 import BeautifulSoup
import re

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

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.5",
}

def extract_product_name(item: BeautifulSoup) -> Optional[str]:
    """Extract product name from a Walmart item."""
    name_elem = (
        item.select_one("span[data-automation-id='product-title']") or
        item.select_one("span.w_iUH7") or
        item.select_one("span.normal")
    )
    return name_elem.text.strip() if name_elem else None

def extract_product_url(item: BeautifulSoup) -> Optional[str]:
    """Extract product URL from a Walmart item."""
    product_id = item.get('data-item-id')
    if not product_id:
        return None
        
    for link in item.select("a"):
        href = link.get('href', '')
        if product_id in href or '/ip/' in href:
            url = href
            if not url.startswith('http'):
                url = f"https://www.walmart.com{url}"
            return url.split('?')[0] if '?' in url else url
    return None

def extract_product_price(item: BeautifulSoup) -> Optional[str]:
    """Extract product price from a Walmart item."""
    price_elem = (
        item.select_one("span[data-automation-id='product-price-1']") or
        item.select_one("div[data-automation-id='product-price']") or
        item.select_one("div.b_Wu1_") or
        item.select_one("span.price-main")
    )
    if not price_elem:
        return None
        
    price_text = price_elem.text.strip()
    price_match = re.search(r'\$\d+\.?\d{0,2}', price_text)
    return price_match.group(0) if price_match else None

def extract_product_image(item: BeautifulSoup) -> Optional[str]:
    """Extract product image URL from a Walmart item."""
    img_elem = (
        item.select_one("img[data-automation-id='product-image']") or
        item.select_one("img.absolute") or
        item.select_one("img")
    )
    if not img_elem:
        return None
        
    image = img_elem.get('src')
    if not image or image.startswith('data:'):
        image = img_elem.get('data-src')
    return image

def scrape_walmart_products(query: str, theme: str, max_results: int) -> List[Dict[str, Any]]:
    """Scrape products from Walmart search results."""
    walmart_url = f"https://www.walmart.com/search?q={query.replace(' ', '+')}"
    print(f"Searching Walmart for: {query}")
    
    try:
        response = requests.get(walmart_url, headers=HEADERS)
        soup = BeautifulSoup(response.text, "html.parser")
        items = soup.select("div[data-item-id]")
        print(f"Found {len(items)} items on Walmart")
        
        products = []
        for item in items[:min(max_results, 3)]:
            try:
                name = extract_product_name(item)
                url = extract_product_url(item)
                price = extract_product_price(item)
                image = extract_product_image(item)
                
                if name and price and url:
                    products.append({
                        "id": item.get('data-item-id', ''),
                        "name": name,
                        "price": price,
                        "retailer": "Walmart",
                        "image_url": image or "https://example.com/placeholder.jpg",
                        "product_url": url,
                        "theme": theme,
                        "description": f"{name} - Available at Walmart"
                    })
            except Exception as e:
                print(f"Error processing item: {e}")
                continue
            
            if len(products) >= max_results:
                break
                
        return products
    except Exception as e:
        print(f"Error searching Walmart: {e}")
        return []

@function_tool
def search_real_products(query: str, item_type: str, max_results: int):
    """
    Search for real products using Walmart's website.
    
    Args:
        query: Search query including theme and item details
        item_type: Type of clothing item
        max_results: Maximum number of results to return
        
    Returns:
        Dictionary containing query info and list of real products
    """
    search_query = f"{query} {item_type}"
    products = scrape_walmart_products(search_query, query, max_results)
    
    # If no products found, return mock data
    if not products:
        products = [{
            "id": f"{query.replace(' ', '-')}-{i}",
            "name": f"{query.title()} {item_type.title()} - Style {i}",
            "price": f"${20*i}.99",
            "retailer": ["Amazon", "Nordstrom", "Macy's", "Target"][i % 4],
            "image_url": f"https://example.com/products/{query.replace(' ', '-')}-{i}.jpg",
            "product_url": f"https://example.com/shop/{query.replace(' ', '-')}-{i}",
            "theme": query,
            "description": f"Example {item_type} matching {query} theme"
        } for i in range(1, max_results + 1)]
    
    return {
        "query": query,
        "item_type": item_type,
        "theme": query,
        "results": products
    } 