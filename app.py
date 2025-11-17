"""
HealthBot Backend Server - Production Version
Flask API for Healthcare Chatbot
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from chatbot_engine import HealthChatbot
import logging
import os

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for all domains (adjust for production security)
CORS(app, resources={
    r"/api/*": {
        "origins": "*",  # Allow all origins for now
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type"]
    }
})

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize chatbot engine
try:
    chatbot = HealthChatbot()
    logger.info("✅ Chatbot engine initialized successfully")
except Exception as e:
    logger.error(f"❌ Failed to initialize chatbot: {e}")
    chatbot = None

# Home route
@app.route('/')
def home():
    """Home endpoint - API status check"""
    return jsonify({
        'status': 'online',
        'message': 'HealthBot API is running',
        'version': '1.0',
        'endpoints': {
            '/': 'API status',
            '/api/chat': 'Chat endpoint (POST)',
            '/api/health': 'Health check'
        }
    })

# Health check endpoint
@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'chatbot_loaded': chatbot is not None,
        'total_topics': len(chatbot.intents) if chatbot else 0
    })

# Main chat endpoint
@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Main chat endpoint
    Accepts: {"message": "user message"}
    Returns: {"response": "bot response", "confidence": 0.95}
    """
    try:
        # Get user message from request
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                'error': 'No message provided',
                'response': 'Please send a message in the format: {"message": "your question"}'
            }), 400
        
        user_message = data['message'].strip()
        
        if not user_message:
            return jsonify({
                'error': 'Empty message',
                'response': 'Please type a valid question.'
            }), 400
        
        # Log the request
        logger.info(f"📨 Received message: {user_message}")
        
        # Get bot response
        if chatbot:
            bot_response, confidence = chatbot.get_response(user_message)
            logger.info(f"🤖 Response generated (confidence: {confidence:.2f})")
        else:
            bot_response = "Sorry, the chatbot engine is not available at the moment. Please try again later."
            confidence = 0.0
        
        # Return response
        return jsonify({
            'response': bot_response,
            'confidence': confidence,
            'status': 'success'
        })
    
    except Exception as e:
        logger.error(f"❌ Error processing message: {e}")
        return jsonify({
            'error': 'Internal server error',
            'response': 'Sorry, I encountered an error processing your request. Please try again.',
            'status': 'error'
        }), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Endpoint not found',
        'message': 'The requested endpoint does not exist'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'error': 'Internal server error',
        'message': 'Something went wrong on the server'
    }), 500

# Run the server
if __name__ == '__main__':
    # Get port from environment variable (for deployment)
    port = int(os.environ.get('PORT', 5000))
    
    print("\n" + "="*60)
    print("🏥 HealthBot Backend Server")
    print("="*60)
    print("🚀 Starting server...")
    print(f"📍 Server will run on port: {port}")
    print("💡 Press CTRL+C to stop the server")
    print("="*60 + "\n")
    
    # Run Flask server
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False  # Set to False in production
    )