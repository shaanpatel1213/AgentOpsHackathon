from agents import function_tool

@function_tool
def get_weather_information(location: str):
    """
    Get weather information for a location to help with wardrobe recommendations.
    
    Args:
        location: City or region name
        
    Returns:
        Weather information including temperature range and conditions
    """
    # Mock weather data for common locations
    weather_data = {
        "boston": {
            "current_temp": "45°F",
            "conditions": "Partly cloudy",
            "seasonal_range": "15°F to 85°F",
            "precipitation": "Moderate rainfall, winter snow"
        },
        "miami": {
            "current_temp": "82°F",
            "conditions": "Sunny",
            "seasonal_range": "65°F to 90°F",
            "precipitation": "Occasional heavy rain, humid"
        },
        "seattle": {
            "current_temp": "52°F",
            "conditions": "Light rain",
            "seasonal_range": "35°F to 75°F",
            "precipitation": "Frequent light rain, occasional snow"
        }
    }
    
    # Default data for unknown locations
    default_data = {
        "current_temp": "65°F",
        "conditions": "Variable",
        "seasonal_range": "Varies by season",
        "precipitation": "Varies throughout the year"
    }
    
    location_key = location.lower().replace(" ", "")
    for key in weather_data:
        if key in location_key:
            return {"location": location, **weather_data[key]}
    
    return {"location": location, **default_data} 