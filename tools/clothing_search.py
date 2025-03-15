import requests
from bs4 import BeautifulSoup
import re
from agents import function_tool
from typing import Optional

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

@function_tool
def search_real_products(query: str, item_type: str, max_results: int):
    """Scrapes Walmart for product details"""
    query = f"{query} {item_type}"
    walmart_url = f"https://www.walmart.com/search?q={query.replace(' ', '+')}"
    print(f"Fetching Walmart URL: {walmart_url}")
    response = requests.get(walmart_url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    
    products = []
    items = soup.select("div[data-item-id]")
    print(f"Found {len(items)} Walmart items")
    
    for item in items[:max_results]:
        try:
            # Get product name
            name = None
            name_elem = (
                item.select_one("span[data-automation-id='product-title']") or
                item.select_one("span.w_iUH7") or
                item.select_one("span.normal")
            )
            if name_elem:
                name = name_elem.text.strip()
            
            # Get product URL
            url = "URL not available"
            product_id = item.get('data-item-id')
            if product_id:
                links = item.select("a")
                for link in links:
                    href = link.get('href', '')
                    if product_id in href or '/ip/' in href:
                        url = href
                        if not url.startswith('http'):
                            url = f"https://www.walmart.com{url}"
                        if '?' in url:
                            url = url.split('?')[0]
                        break
            
            # Get product price
            price = "Price not available"
            price_elem = (
                item.select_one("span[data-automation-id='product-price-1']") or
                item.select_one("div[data-automation-id='product-price']") or
                item.select_one("div.b_Wu1_") or
                item.select_one("span.price-main")
            )
            if price_elem:
                price_text = price_elem.text.strip()
                price_match = re.search(r'\$(\d+\.?\d{0,2})', price_text)
                if price_match:
                    price = price_match.group(1)
                    try:
                        price = "{:.2f}".format(float(price) / 100)
                    except:
                        price = "Price not available"

            # Get product image
            image = None
            img_elem = (
                item.select_one("img[data-automation-id='product-image']") or
                item.select_one("img.absolute") or
                item.select_one("img")
            )
            if img_elem:
                image = img_elem.get('src')
                if not image or image.startswith('data:'):
                    image = img_elem.get('data-src')
            
            # Only add product if we have at least a name
            if name:
                products.append({
                    "name": name,
                    "price": price if price else "Price not available",
                    "image_url": image if image else "Image not available",
                    "product_url": url,
                    "description": description if description else "Description not available"
                })
        
            print(products)
            
        except Exception as e:
            print(f"Error processing Walmart item: {e}")
            continue

    return products