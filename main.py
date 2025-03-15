from openai import OpenAI
from agents import Runner
from my_agents.wardrobe_agents import wardrobe_agent
from models.clothing import WardrobeRecommendation
import os
from dotenv import load_dotenv
import json

load_dotenv()

# Set up OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def create_wardrobe_recommendation(user_prompt):
    """
    Generate a wardrobe recommendation based on user prompt.
    
    Args:
        user_prompt: User's request for a wardrobe recommendation
        
    Returns:
        Structured wardrobe recommendation
    """
    result = Runner.run_sync(
        wardrobe_agent,
        user_prompt
    )
    
    # Convert the result to a WardrobeRecommendation object if it's not already
    if isinstance(result.final_output, str):
        try:
            # Try to parse the string as a JSON dictionary
            data = json.loads(result.final_output)
            return WardrobeRecommendation(**data)
        except json.JSONDecodeError:
            raise ValueError(f"Agent output is not in the expected format: {result.final_output}")
    elif isinstance(result.final_output, dict):
        # If it's already a dictionary, convert it to WardrobeRecommendation
        return WardrobeRecommendation(**result.final_output)
    else:
        return result.final_output  # If it's already a WardrobeRecommendation object

def print_recommendation(recommendation):
    """Print a formatted wardrobe recommendation."""
    print("\n=== WARDROBE RECOMMENDATION ===")
    print(f"Theme: {recommendation.theme}")
    
    print("\n== HEADWEAR ==")
    for item in recommendation.headwear:
        print(f"- {item.name}: {item.price}")
        print(f"  {item.description}")
        print(f"  Image: {item.image_url}")
        print(f"  Buy: {item.product_url}")
    
    print("\n== TOPS ==")
    for item in recommendation.tops:
        print(f"- {item.name}: {item.price}")
        print(f"  {item.description}")
        print(f"  Image: {item.image_url}")
        print(f"  Buy: {item.product_url}")
    
    print("\n== OUTERWEAR ==")
    for item in recommendation.outerwear:
        print(f"- {item.name}: {item.price}")
        print(f"  {item.description}")
        print(f"  Image: {item.image_url}")
        print(f"  Buy: {item.product_url}")
    
    print("\n== STYLING TIPS ==")
    print(recommendation.styling_tips)

if __name__ == "__main__":
    # Example prompts
    example_prompts = [
        "I recently moved to Boston. I am a Red Sox fan. Create a new wardrobe for me, with hats.",
        "I need a minimalist wardrobe for my new job in Seattle. I prefer neutral colors.",
        "Help me create a summer festival wardrobe with a bohemian vibe. I love hats and accessories."
    ]
    
    # Choose a prompt to test
    test_prompt = example_prompts[0]
    print(f"Processing request: {test_prompt}")
    
    # Get recommendation
    try:
        # Add debug logging
        # print("\n=== DEBUG INFO ===")
        result = Runner.run_sync(wardrobe_agent, test_prompt)
        # print(f"Result type: {type(result.final_output)}")
        # print(f"Result content: {result.final_output}")
        if isinstance(result.final_output, str):
            # print("\nAttempting to parse as JSON:")
            try:
                parsed = json.loads(result.final_output)
                #print(f"Parsed JSON: {json.dumps(parsed, indent=2)}")
                recommendation = WardrobeRecommendation(theme=parsed["theme"],
                                                        styling_tips=parsed["styling_tips"],
                                                        tops=parsed["suggested_items"]["tops"],
                                                        bottoms=parsed["suggested_items"]["bottoms"],
                                                        outerwear=parsed["suggested_items"]["outerwear"],
                                                        headwear=parsed["suggested_items"]["headwear"],
                                                        footwear=parsed["suggested_items"]["footwear"],
                                                        accessories=parsed["suggested_items"]["accessories"])
            except json.JSONDecodeError as e:
                print(f"JSON parsing failed: {e}")
        # print("=== END DEBUG ===\n")
        
        #recommendation = create_wardrobe_recommendation(test_prompt)
        print(recommendation)
        print_recommendation(recommendation)
        
    except Exception as e:
        print(f"Error generating recommendation: {e}")