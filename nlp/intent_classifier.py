import re
import spacy
from transformers import pipeline
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import pickle
import os

class IntentClassifier:
    def __init__(self):
        self.model = None
        self.intents = {
            'balance_inquiry': [
                'what is my balance', 'how much money do i have', 'current balance',
                'account balance', 'total balance', 'how much do i have', 'show my balance',
                'balance check', 'my money', 'current funds', 'available balance'
            ],
            'spending_analysis': [
                'how much did i spend', 'spending this month', 'expenses',
                'where did my money go', 'spending breakdown', 'what did i buy',
                'monthly expenses', 'spending report', 'expense analysis', 'money spent'
            ],
            'forecast_inquiry': [
                'will i have enough money', 'future balance', 'predict my balance',
                'cash flow forecast', 'how much will i have', 'money prediction',
                'future finances', 'next month balance', 'financial forecast'
            ],
            'savings_advice': [
                'how can i save money', 'savings tips', 'reduce expenses',
                'budget advice', 'financial advice', 'save more money',
                'help me save', 'money saving tips', 'cut expenses', 'financial tips'
            ],
            'affordability_check': [
                'can i afford', 'should i buy', 'is it safe to spend',
                'can i purchase', 'afford to buy', 'budget for', 'can i spend'
            ],
            'investment_advice': [
                'investment advice', 'how to invest', 'stock market', 'investing tips',
                'portfolio advice', 'investment strategy', 'manage stocks', 'financial planning'
            ],
            'greeting': [
                'hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening',
                'greetings', 'howdy', 'what can you do', 'help me'
            ],
            'general_help': [
                'what can you help with', 'what do you do', 'help', 'assistance',
                'features', 'capabilities', 'how does this work'
            ]
        }
        
        # Load or train the model
        self._load_or_train_model()
        
        # Load spaCy model for text preprocessing
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("spaCy model not found. Install with: python -m spacy download en_core_web_sm")
            self.nlp = None
    
    def _load_or_train_model(self):
        """Load existing model or train a new one"""
        model_path = 'models/intent_classifier.pkl'
        
        if os.path.exists(model_path):
            try:
                with open(model_path, 'rb') as f:
                    self.model = pickle.load(f)
                return
            except:
                pass
        
        # Train new model
        self._train_model()
        
        # Save the model
        os.makedirs('models', exist_ok=True)
        with open(model_path, 'wb') as f:
            pickle.dump(self.model, f)
    
    def _train_model(self):
        """Train intent classification model"""
        # Prepare training data
        X_train = []
        y_train = []
        
        for intent, examples in self.intents.items():
            for example in examples:
                X_train.append(example)
                y_train.append(intent)
                
                # Add variations
                variations = self._generate_variations(example)
                for variation in variations:
                    X_train.append(variation)
                    y_train.append(intent)
        
        # Create and train pipeline
        self.model = Pipeline([
            ('tfidf', TfidfVectorizer(ngram_range=(1, 2), stop_words='english')),
            ('classifier', MultinomialNB(alpha=0.1))
        ])
        
        self.model.fit(X_train, y_train)
    
    def _generate_variations(self, text):
        """Generate variations of training examples"""
        variations = []
        
        # Simple word substitutions
        substitutions = {
            'money': ['cash', 'funds', 'dollars'],
            'spend': ['spent', 'use', 'used'],
            'balance': ['amount', 'total'],
            'month': ['week', 'period'],
            'buy': ['purchase', 'get']
        }
        
        words = text.split()
        for i, word in enumerate(words):
            if word in substitutions:
                for sub in substitutions[word]:
                    new_words = words.copy()
                    new_words[i] = sub
                    variations.append(' '.join(new_words))
        
        return variations[:3]  # Limit variations
    
    def preprocess_text(self, text):
        """Preprocess text for classification"""
        # Convert to lowercase
        text = text.lower().strip()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Extract financial amounts and replace with placeholder
        text = re.sub(r'\$?\d+(?:,\d{3})*(?:\.\d{2})?', '[AMOUNT]', text)
        
        # Use spaCy for lemmatization if available
        if self.nlp:
            doc = self.nlp(text)
            text = ' '.join([token.lemma_ for token in doc if not token.is_stop and not token.is_punct])
        
        return text
    
    def classify_intent(self, text):
        """Classify the intent of user input"""
        # First try rule-based classification (more reliable for simple cases)
        rule_based_intent = self._rule_based_classification(text)
        if rule_based_intent:
            return rule_based_intent, 0.9
        
        # Fallback to ML model if available
        if self.model:
            try:
                # Preprocess text
                processed_text = self.preprocess_text(text)
                
                # Get prediction and confidence
                prediction = self.model.predict([processed_text])[0]
                probabilities = self.model.predict_proba([processed_text])[0]
                confidence = max(probabilities)
                
                return prediction, confidence
            except Exception as e:
                print(f"ML classification error: {e}")
                return 'general_help', 0.5
        
        # Default fallback
        return 'general_help', 0.5
    
    def _rule_based_classification(self, text):
        """Rule-based classification for specific patterns"""
        text_lower = text.lower()
        
        # Greetings
        if any(word in text_lower for word in ['hello', 'hi', 'hey', 'good morning', 'good afternoon']):
            return 'greeting'
        
        # Balance inquiries
        if any(word in text_lower for word in ['balance', 'money', 'total', 'have']):
            return 'balance_inquiry'
        
        # Spending analysis
        if any(word in text_lower for word in ['spend', 'spent', 'expense', 'cost', 'monthly']):
            return 'spending_analysis'
        
        # Forecast inquiries
        if any(word in text_lower for word in ['will', 'future', 'predict', 'forecast', 'next month']):
            return 'forecast_inquiry'
        
        # Affordability checks
        if any(phrase in text_lower for phrase in ['can i afford', 'should i buy', 'can i purchase', 'afford']):
            return 'affordability_check'
        
        # Savings advice
        if any(word in text_lower for word in ['save', 'saving', 'budget', 'advice', 'tips']):
            return 'savings_advice'
        
        # Investment advice
        if any(word in text_lower for word in ['invest', 'stock', 'portfolio', 'investment']):
            return 'investment_advice'
        
        # General help
        if any(word in text_lower for word in ['help', 'what', 'how', 'can you']):
            return 'general_help'
        
        return None
    
    def extract_entities(self, text):
        """Extract financial entities from text"""
        entities = {}
        
        # Extract amounts
        amount_pattern = r'\$?(\d+(?:,\d{3})*(?:\.\d{2})?)'
        amounts = re.findall(amount_pattern, text)
        if amounts:
            entities['amounts'] = [float(amount.replace(',', '')) for amount in amounts]
        
        # Extract time periods
        time_patterns = {
            'month': r'\b(?:this\s+)?month\b',
            'week': r'\b(?:this\s+)?week\b',
            'year': r'\b(?:this\s+)?year\b',
            'day': r'\b(?:today|yesterday)\b'
        }
        
        for period, pattern in time_patterns.items():
            if re.search(pattern, text.lower()):
                entities['time_period'] = period
                break
        
        # Extract categories (simple keyword matching)
        categories = ['food', 'gas', 'groceries', 'entertainment', 'shopping', 'bills', 'rent']
        for category in categories:
            if category in text.lower():
                entities['category'] = category
                break
        
        return entities