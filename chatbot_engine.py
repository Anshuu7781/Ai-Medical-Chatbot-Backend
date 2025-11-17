"""
HealthBot Chatbot Engine - SIMPLE VERSION
Easy to understand keyword matching logic
"""

import json
import os

class HealthChatbot:
    """Simple Healthcare Chatbot using keyword matching"""
    
    def __init__(self, intents_file='data/intents.json'):
        """Initialize the chatbot"""
        self.intents_file = intents_file
        self.intents = []
        self.load_intents()
        print(f"✅ Chatbot loaded with {len(self.intents)} health topics")
    
    def load_intents(self):
        """Load healthcare data from JSON file"""
        try:
            file_path = os.path.join(os.path.dirname(__file__), self.intents_file)
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.intents = data.get('intents', [])
            print(f"✅ Loaded {len(self.intents)} intents from {self.intents_file}")
        except FileNotFoundError:
            print(f"❌ Error: {self.intents_file} not found!")
            self.intents = []
        except json.JSONDecodeError:
            print(f"❌ Error: Invalid JSON in {self.intents_file}")
            self.intents = []
    
    def clean_text(self, text):
        """
        Convert text to lowercase and remove extra spaces
        Simple preprocessing for better matching
        """
        return ' '.join(text.lower().strip().split())
    
    def check_keywords(self, user_message, keywords):
        """
        Check if any keyword from the list is in user message
        Returns True if match found
        
        Algorithm:
        1. Clean the user message (lowercase, trim spaces)
        2. For each keyword in the keywords list:
           - Clean the keyword
           - Check if keyword exists in user message
           - If found, return True
        3. If no match found, return False
        """
        user_message = self.clean_text(user_message)
        
        for keyword in keywords:
            keyword = self.clean_text(keyword)
            if keyword in user_message:
                return True
        return False
    
    def get_response(self, user_message):
        """
        Get bot response by matching keywords
        
        Process:
        1. Clean user message
        2. Loop through all intents in knowledge base
        3. Check if user message matches any keywords
        4. If match found, return that intent's response
        5. If no match, return default response
        
        Returns: (response_text, confidence_score)
        """
        user_message = self.clean_text(user_message)
        
        # Check each intent for keyword matches
        for intent in self.intents:
            keywords = intent.get('keywords', [])
            
            # If keywords match, return response
            if self.check_keywords(user_message, keywords):
                response = intent.get('response', '')
                return response, 0.95  # High confidence on match
        
        # No match found - return default response
        default_response = """I'm not sure about that specific topic. I can help you with:

<strong>Common Health Topics:</strong>
• Fever, Cold, Flu, Headache
• Diabetes, Blood Pressure, Heart Disease
• Burns, Cuts, Wounds, Sprains
• CPR, Choking, First Aid
• Asthma, Allergies, COVID-19
• Nutrition, Exercise, Sleep
• Mental Health, Stress, Anxiety
• Pregnancy, Women's Health
• Child Health, Vaccinations

Please ask about any of these topics, and I'll provide detailed information! 😊

<em>💡 Tip: Try to be specific, like "What are fever symptoms?" or "How to treat burns?"</em>"""
        
        return default_response, 0.3  # Low confidence - no match found


# Simple test function
if __name__ == "__main__":
    """
    Test the chatbot engine
    Run this file directly to test: python chatbot_engine.py
    """
    print("\n" + "="*60)
    print("🧪 Testing HealthBot Chatbot Engine")
    print("="*60 + "\n")
    
    # Initialize bot
    bot = HealthChatbot()
    
    print(f"\n📚 Knowledge Base Stats:")
    print(f"   Total Topics: {len(bot.intents)}")
    print(f"   Status: {'✅ Ready' if bot.intents else '❌ No data loaded'}\n")
    
    # Test queries
    test_queries = [
        "What are fever symptoms?",
        "How to treat burns?",
        "Tell me about diabetes",
        "I have a headache",
        "First aid for cuts"
    ]
    
    print("🔍 Testing Sample Queries:\n")
    for query in test_queries:
        response, confidence = bot.get_response(query)
        print(f"Q: {query}")
        print(f"Confidence: {confidence:.2%}")
        print(f"A: {response[:150]}...")
        print("-" * 60 + "\n")
    
    print("✅ Test Complete!\n")