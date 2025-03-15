from flask import Flask, request, jsonify
from wardrobe_service import WardrobeService
from models.clothing import ClothingItem
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
wardrobe_service = WardrobeService()

@app.route('/api/wardrobe/recommend', methods=['POST'])
def get_wardrobe_recommendation():
    """
    Generate a wardrobe recommendation based on user prompt.
    
    Request body:
    {
        "prompt": "string"  // User's wardrobe request
    }
    """
    try:
        logger.debug("Received wardrobe recommendation request")
        data = request.get_json()
        logger.debug(f"Request data: {data}")
        
        if not data or 'prompt' not in data:
            logger.error("Missing prompt in request body")
            return jsonify({'error': 'Missing prompt in request body'}), 400
            
        prompt = data['prompt']
        logger.debug(f"Processing prompt: {prompt}")
        
        recommendation = wardrobe_service.create_wardrobe_recommendation(prompt)
        logger.debug("Generated recommendation")
        
        # Convert recommendation to dictionary
        result = {
            'theme': recommendation.theme,
            'styling_tips': recommendation.styling_tips,
            'tops': [item.__dict__ for item in recommendation.tops],
            'bottoms': [item.__dict__ for item in recommendation.bottoms],
            'outerwear': [item.__dict__ for item in recommendation.outerwear],
            'headwear': [item.__dict__ for item in recommendation.headwear],
            'footwear': [item.__dict__ for item in recommendation.footwear],
            'accessories': [item.__dict__ for item in recommendation.accessories]
        }
        
        logger.debug(f"Sending response: {result}")
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    logger.info("Starting Flask server...")
    app.run(debug=True, port=5000)