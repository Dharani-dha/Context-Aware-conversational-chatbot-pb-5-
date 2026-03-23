import re
import json

class ContextManager:
    """Manages conversational state, entity memory, and chat history for each user."""
    
    def __init__(self):
        # We store session contexts in a dict, keyed by user_id for multi-user support
        self.sessions = {}

    def get_context(self, user_id):
        if user_id not in self.sessions:
            self.sessions[user_id] = {
                'state': 'neutral',
                'entities': {},
                'history': []
            }
        return self.sessions[user_id]
        
    def update_entity(self, user_id, entity_name, entity_value):
        context = self.get_context(user_id)
        context['entities'][entity_name] = entity_value
        
    def add_history(self, user_id, role, message):
        context = self.get_context(user_id)
        context['history'].append({'role': role, 'message': message})
        
    def set_state(self, user_id, state):
        context = self.get_context(user_id)
        context['state'] = state

class IntentRecognizer:
    """Uses regex-based keyword matching to classify user intents."""
    
    def __init__(self):
        self.intents = {
            'greeting': r'\b(hi|hello|hey|greetings)\b',
            'track_order': r'\b(track|where|status)\b.*\b(order|package)\b|\b(track|status)\b',
            'request_refund': r'\b(refund|return|money back|cancel)\b',
        }

    def predict_intent(self, text):
        text = text.lower()
        for intent, pattern in self.intents.items():
            if re.search(pattern, text, re.IGNORECASE):
                return intent
                
        return 'unknown'

class DialogueHandler:
    """Handles generating responses coherently based on intent and active context state."""
    
    def __init__(self, context_manager, intent_recognizer):
        self.context_manager = context_manager
        self.intent_recognizer = intent_recognizer

    def extract_order_id(self, message):
        """Helper to extract an order ID. Ensures it doesn't match normal words like 'nevermind'."""
        words = [re.sub(r'[^\w\s]', '', w) for w in message.split()]
        for word in words:
            # A valid order ID should be 5-10 characters long and contain at least one number.
            if len(word) >= 5 and len(word) <= 10 and any(c.isdigit() for c in word):
                return word.upper()
        return None

    def handle_message(self, user_id, message):
        self.context_manager.add_history(user_id, 'user', message)
        context = self.context_manager.get_context(user_id)
        
        intent = self.intent_recognizer.predict_intent(message)
        current_state = context['state']
        
        # Proactively check for entities in the same message that might fulfill intents
        inline_order_id = self.extract_order_id(message)
        if inline_order_id:
             self.context_manager.update_entity(user_id, 'order_id', inline_order_id)
             context = self.context_manager.get_context(user_id) # refresh reference
        
        response = ""
        
        # 1. State-driven dialogue (Expectations based on previous turns)
        if current_state == 'awaiting_order_id_for_tracking':
             order_id = self.extract_order_id(message)
             if order_id:
                 self.context_manager.update_entity(user_id, 'order_id', order_id)
                 self.context_manager.set_state(user_id, 'neutral')
                 response = f"Got it. Order {order_id} is currently out for delivery and should arrive tomorrow."
             else:
                 response = "I couldn't find a valid order ID in your message. Please provide your 5-10 character alphanumeric order ID."
                 
        elif current_state == 'awaiting_order_id_for_refund':
             order_id = self.extract_order_id(message)
             if order_id:
                 self.context_manager.update_entity(user_id, 'order_id', order_id)
                 self.context_manager.set_state(user_id, 'neutral')
                 response = f"I've initiated a refund for order {order_id}. You should see it in your account within 3-5 business days."
             else:
                 response = "I need your order ID to process the refund. Please provide it."

        # 2. Intent-driven dialogue (Standard flow)
        else:
            if intent == 'greeting':
                response = "Hello! I am your customer support assistant. How can I help you today? You can ask me to track an order or request a refund."
            elif intent == 'track_order':
                if 'order_id' in context['entities']:
                    order_id = context['entities']['order_id']
                    response = f"Checking on your order {order_id}... It is out for delivery."
                else:
                    self.context_manager.set_state(user_id, 'awaiting_order_id_for_tracking')
                    response = "I can help with tracking. Please provide your order ID."
            elif intent == 'request_refund':
                if 'order_id' in context['entities']:
                    order_id = context['entities']['order_id']
                    response = f"I can process a refund for your previously mentioned order {order_id}. I've initiated it now."
                else:
                    self.context_manager.set_state(user_id, 'awaiting_order_id_for_refund')
                    response = "I can help you with a refund. Could you please provide your order ID?"
            else:
                response = "I'm sorry, I didn't quite catch that. Could you rephrase? I can help track your order or process a refund."
                
        self.context_manager.add_history(user_id, 'bot', response)
        return response

if __name__ == '__main__':
    context_mgr = ContextManager()
    intent_rec = IntentRecognizer()
    bot = DialogueHandler(context_mgr, intent_rec)
    
    print("=====================================================")
    print("   Context-Aware Conversational Chatbot Started      ")
    print("   Type 'quit' or 'exit' to stop.                    ")
    print("=====================================================\n")
    
    user_id = "user_123"
    
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ['quit', 'exit']:
                print("Bot: Goodbye!")
                break
            
            reply = bot.handle_message(user_id, user_input)
            print(f"Bot: {reply}")
        except KeyboardInterrupt:
            break
