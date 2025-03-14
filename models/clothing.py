from pydantic import BaseModel, Field
from typing import List, Optional

class ClothingItem(BaseModel):
    name: str = Field(..., description="Name of the clothing item")
    price: str = Field(..., description="Price of the item in string format (e.g., '$34.99')")
    image_url: str = Field(..., description="URL to the image of the product")
    product_url: str = Field(..., description="URL to purchase the product")
    description: Optional[str] = Field(None, description="Brief description of the item")
    
class WardrobeRecommendation(BaseModel):
    theme: str = Field(..., description="The theme or style of this wardrobe")
    tops: List[ClothingItem] = Field(default_factory=list, description="Recommended shirts, t-shirts, jerseys, etc.")
    bottoms: List[ClothingItem] = Field(default_factory=list, description="Recommended pants, shorts, skirts, etc.")
    outerwear: List[ClothingItem] = Field(default_factory=list, description="Recommended jackets, hoodies, etc.")
    headwear: List[ClothingItem] = Field(default_factory=list, description="Recommended hats, caps, beanies, etc.")
    footwear: Optional[List[ClothingItem]] = Field(default_factory=list, description="Recommended shoes, socks, etc.")
    accessories: Optional[List[ClothingItem]] = Field(default_factory=list, description="Recommended accessories like bags, jewelry, etc.")
    styling_tips: str = Field(..., description="Tips on how to combine these items and wear them") 