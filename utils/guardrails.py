from agents import output_guardrail

@output_guardrail
def validate_price_range(context, input_text):
    """Ensure recommendations include various price points"""
    if "only expensive" in input_text.lower() or "only luxury" in input_text.lower():
        return False, "Please provide options at various price points"
    return True, None

@output_guardrail
def validate_image_urls(context, input_text):
    """Ensure all recommendations include image URLs"""
    if "ClothingItem" in input_text and "image_url" in input_text:
        if "example.com" in input_text and not "placeholder" in input_text.lower():
            return False, "Please use realistic image URLs or indicate they are placeholders"
    return True, None 