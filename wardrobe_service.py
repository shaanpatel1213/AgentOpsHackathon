from openai import OpenAI
from agents import Runner
from my_agents.wardrobe_agents import wardrobe_agent
from models.clothing import WardrobeRecommendation, ClothingItem
import json
import os
from dotenv import load_dotenv
import asyncio
import nest_asyncio
from colorama import init, Fore, Style, Back

# Initialize colorama
init()

# Apply nest_asyncio to allow nested event loops
nest_asyncio.apply()

load_dotenv()

class WardrobeService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
    def _ensure_event_loop(self):
        """Ensure there's an event loop available in the current thread."""
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        return loop

    def create_wardrobe_recommendation(self, user_prompt: str) -> WardrobeRecommendation:
        """
        Generate a wardrobe recommendation based on user prompt.
        
        Args:
            user_prompt: User's request for a wardrobe recommendation
            
        Returns:
            WardrobeRecommendation object
        """
        # Ensure we have an event loop
        loop = self._ensure_event_loop()
        
        # Run the agent in the event loop
        result = loop.run_until_complete(
            Runner.run(
                wardrobe_agent,
                user_prompt
            )
        )
        
        return self._parse_agent_output(result.final_output)
    
    def _parse_agent_output(self, output) -> WardrobeRecommendation:
        """Parse the agent's output into a WardrobeRecommendation object."""
        if isinstance(output, str):
            try:
                data = json.loads(output)
            except json.JSONDecodeError as e:
                raise ValueError(f"Agent output is not valid JSON: {e}")
        elif isinstance(output, dict):
            data = output
        else:
            return output  # Already a WardrobeRecommendation object
            
        try:
            # Handle different output formats
            if "items" in data:
                return self._create_from_items(data)
            elif "suggested_items" in data:
                return self._create_from_suggested_items(data)
            elif "results" in data:
                return self._create_from_results(data)
            else:
                return WardrobeRecommendation(**data)
        except Exception as e:
            raise ValueError(f"Error creating recommendation: {e}")
    
    def _create_from_items(self, data: dict) -> WardrobeRecommendation:
        """Create WardrobeRecommendation from items format."""
        items = data["items"]
        return WardrobeRecommendation(
            theme=data.get("theme", "Personalized Wardrobe"),
            styling_tips=data.get("styling_tips", "Mix and match these pieces for a versatile and personalized wardrobe."),
            tops=[ClothingItem(**item) for item in items if "shirt" in item["name"].lower() or "tee" in item["name"].lower() or "jersey" in item["name"].lower()],
            bottoms=[ClothingItem(**item) for item in items if "pants" in item["name"].lower() or "jeans" in item["name"].lower() or "shorts" in item["name"].lower()],
            outerwear=[ClothingItem(**item) for item in items if "jacket" in item["name"].lower() or "hoodie" in item["name"].lower() or "coat" in item["name"].lower()],
            headwear=[ClothingItem(**item) for item in items if "hat" in item["name"].lower() or "cap" in item["name"].lower() or "beanie" in item["name"].lower()],
            footwear=[ClothingItem(**item) for item in items if "shoes" in item["name"].lower() or "sneaker" in item["name"].lower() or "boots" in item["name"].lower()],
            accessories=[ClothingItem(**item) for item in items if "accessory" in item["name"].lower() or "scarf" in item["name"].lower() or "bag" in item["name"].lower()]
        )
    
    def _create_from_suggested_items(self, data: dict) -> WardrobeRecommendation:
        """Create WardrobeRecommendation from suggested_items format."""
        return WardrobeRecommendation(
            theme=data.get("theme", "Personalized Wardrobe"),
            styling_tips=data.get("styling_tips", "Mix and match these pieces for a versatile and personalized wardrobe."),
            tops=[ClothingItem(**item) for item in data["suggested_items"].get("tops", [])],
            bottoms=[ClothingItem(**item) for item in data["suggested_items"].get("bottoms", [])],
            outerwear=[ClothingItem(**item) for item in data["suggested_items"].get("outerwear", [])],
            headwear=[ClothingItem(**item) for item in data["suggested_items"].get("headwear", [])],
            footwear=[ClothingItem(**item) for item in data["suggested_items"].get("footwear", [])],
            accessories=[ClothingItem(**item) for item in data["suggested_items"].get("accessories", [])]
        )
    
    def _create_from_results(self, data: dict) -> WardrobeRecommendation:
        """Create WardrobeRecommendation from search_real_products results format."""
        return WardrobeRecommendation(
            theme=data.get("theme", "Personalized Wardrobe"),
            styling_tips="Mix and match these pieces for a versatile and personalized wardrobe.",
            tops=[ClothingItem(**item) for item in data["results"] if "shirt" in item["name"].lower() or "tee" in item["name"].lower() or "jersey" in item["name"].lower()],
            bottoms=[ClothingItem(**item) for item in data["results"] if "pants" in item["name"].lower() or "jeans" in item["name"].lower() or "shorts" in item["name"].lower()],
            outerwear=[ClothingItem(**item) for item in data["results"] if "jacket" in item["name"].lower() or "hoodie" in item["name"].lower() or "coat" in item["name"].lower()],
            headwear=[ClothingItem(**item) for item in data["results"] if "hat" in item["name"].lower() or "cap" in item["name"].lower() or "beanie" in item["name"].lower()],
            footwear=[ClothingItem(**item) for item in data["results"] if "shoes" in item["name"].lower() or "sneaker" in item["name"].lower() or "boots" in item["name"].lower()],
            accessories=[ClothingItem(**item) for item in data["results"] if "accessory" in item["name"].lower() or "scarf" in item["name"].lower() or "bag" in item["name"].lower()]
        )
    
def print_item(item: ClothingItem):
    """Print a single clothing item with formatting."""
    print(f"\n{Fore.WHITE}{Style.BRIGHT}• {item.name}{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}Price:{Style.RESET_ALL} {item.price}")
    if item.description:
        print(f"  {Fore.CYAN}Description:{Style.RESET_ALL} {item.description}")
    print(f"  {Fore.BLUE}Product URL:{Style.RESET_ALL} {item.product_url}")
    print(f"  {Fore.MAGENTA}Image URL:{Style.RESET_ALL} {item.image_url}")

def print_section(title: str, items: list[ClothingItem]):
    """Print a section of clothing items with formatting."""
    print(f"\n{Back.WHITE}{Fore.BLACK}{Style.BRIGHT}=== {title} ==={Style.RESET_ALL}")
    if not items:
        print(f"{Fore.RED}No items found{Style.RESET_ALL}")
    for item in items:
        print_item(item)

def main():
    """Test the wardrobe service with a sample prompt."""
    service = WardrobeService()
    
    test_prompt = "I need a casual wardrobe for a Boston Red Sox fan who likes comfortable clothes"

    
    try:
        # Print request
        print(f"\n{Back.BLUE}{Fore.WHITE}{Style.BRIGHT} WARDROBE REQUEST {Style.RESET_ALL}")
        print(f"{Fore.CYAN}Prompt:{Style.RESET_ALL} {test_prompt}")
        
        # Get recommendation
        recommendation = service.create_wardrobe_recommendation(test_prompt)
        
        # Print theme and styling tips
        print(f"\n{Back.GREEN}{Fore.BLACK}{Style.BRIGHT} WARDROBE RECOMMENDATION {Style.RESET_ALL}")
        print(f"\n{Fore.GREEN}{Style.BRIGHT}Theme:{Style.RESET_ALL} {recommendation.theme}")
        print(f"\n{Fore.GREEN}{Style.BRIGHT}Styling Tips:{Style.RESET_ALL} {recommendation.styling_tips}")
        
        # Print each section
        print_section("TOPS", recommendation.tops)
        print_section("BOTTOMS", recommendation.bottoms)
        print_section("OUTERWEAR", recommendation.outerwear)
        print_section("HEADWEAR", recommendation.headwear)
        print_section("FOOTWEAR", recommendation.footwear)
        print_section("ACCESSORIES", recommendation.accessories)
            
    except Exception as e:
        print(f"\n{Back.RED}{Fore.WHITE}{Style.BRIGHT} ERROR {Style.RESET_ALL}")
        print(f"{Fore.RED}{str(e)}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
