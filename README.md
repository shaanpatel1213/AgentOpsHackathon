# AI Wardrobe Assistant

An intelligent wardrobe recommendation system that uses AI to generate personalized clothing suggestions based on user preferences, style, and context. The system leverages OpenAI's API and a multi-agent architecture to provide detailed wardrobe recommendations with real product suggestions.

## Features

- **Personalized Recommendations**: Generates wardrobe suggestions based on user's style preferences, occasion, and needs
- **Real Product Search**: Integrates with Walmart's product catalog to find actual clothing items
- **Structured Output**: Organizes recommendations by category (tops, bottoms, outerwear, etc.)
- **Detailed Information**: Provides product names, prices, descriptions, and URLs for each item
- **Styling Tips**: Includes personalized advice on how to combine and wear the suggested items
- **REST API**: Offers a Flask-based API endpoint for easy integration

## Setup

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Create a `.env` file with your OpenAI API key:
```
OPENAI_API_KEY=your-api-key-here
```

## Usage

### API Endpoint

Start the Flask server:
```bash
python main.py
```

Make a request:
```bash
curl -X POST http://127.0.0.1:5000/api/wardrobe/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "I need a minimalist wardrobe with neutral colors for a professional setting"
  }'
```

### Example Response

```json
{
  "theme": "Professional Minimalist Wardrobe",
  "styling_tips": "Mix and match these versatile pieces...",
  "tops": [
    {
      "name": "Classic White Oxford Shirt",
      "price": "$45.99",
      "description": "Crisp cotton oxford shirt...",
      "product_url": "https://...",
      "image_url": "https://..."
    }
  ],
  // Other categories: bottoms, outerwear, headwear, footwear, accessories
}
```

## Architecture

The system uses a multi-agent approach:
- **Product Search Agent**: Finds real clothing items matching the user's requirements
- **Style Advisor Agent**: Provides fashion advice and styling tips
- **Main Wardrobe Agent**: Coordinates the recommendations and ensures coherent output

## Technologies

- Python 3.8+
- OpenAI API
- Flask
- Pydantic for data validation
- Colorama for formatted console output
- Async support with nest_asyncio
