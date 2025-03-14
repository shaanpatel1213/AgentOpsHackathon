# AI Wardrobe Assistant

An AI-powered wardrobe assistant that helps users create personalized clothing recommendations based on their style preferences, location, and specific needs.

## Features

- Theme-based wardrobe recommendations
- Location-aware clothing suggestions
- Detailed product recommendations with pricing
- Styling tips and outfit combinations
- Support for specific clothing requests (e.g., hats, accessories)
- Weather-appropriate clothing suggestions

## Project Structure

```
.
├── agents/
│   └── wardrobe_agents.py    # Agent definitions
├── models/
│   └── clothing.py           # Data models
├── tools/
│   ├── clothing_search.py    # Clothing search tools
│   └── weather.py           # Weather information tool
├── utils/
│   └── guardrails.py        # Output validation
├── main.py                  # Main application
├── requirements.txt         # Dependencies
└── README.md               # Documentation
```

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

Run the main script with an example prompt:

```bash
python main.py
```

Or import and use the wardrobe recommendation function in your code:

```python
from main import create_wardrobe_recommendation

prompt = "I need a minimalist wardrobe for my new job in Seattle. I prefer neutral colors."
recommendation = create_wardrobe_recommendation(prompt)
```

## Example Prompts

- "I recently moved to Boston. I am a Red Sox fan. Create a new wardrobe for me, with hats."
- "I need a minimalist wardrobe for my new job in Seattle. I prefer neutral colors."
- "Help me create a summer festival wardrobe with a bohemian vibe. I love hats and accessories."

## Output Format

The wardrobe recommendations include:
- Theme description
- Clothing items by category (tops, bottoms, outerwear, etc.)
- Price information
- Product images and purchase links
- Styling tips

## Note

This is a demonstration project using mock data. In a production environment, you would need to:
1. Implement real e-commerce API integrations
2. Use actual weather API data
3. Set up proper error handling and rate limiting
4. Implement caching for API responses
5. Add proper security measures for API keys and user data
