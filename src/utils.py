import json
import os
import streamlit as st
from config.languages import TRANSLATIONS

@st.cache_data
def load_company_data():
    """Load company data from JSON file with caching"""
    try:
        # Load from project root data directory
        file_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),  # Go up one level from src
            'data',
            'company_data.json'
        )
        
        print(f"Loading FAQs from: {file_path}")  # Debug print
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f"Loaded {len(data.get('faqs', []))} FAQs")  # Debug print
            return data
            
    except Exception as e:
        st.error(f"Error loading company data: {str(e)}")
        # Return default data if file not found
        return {
            "faqs": [
                {
                    "id": "sample",
                    "category": "general",
                    "keywords": ["sample"],
                    "question": "How do I get started?",
                    "answer": "This is a sample FAQ. Please follow these steps:\n\n1. Create an account\n2. Set up your profile\n3. Start using our services"
                }
            ]
        }

def get_translation(key, language=None):
    """Get translated text for given key and language"""
    if language is None:
        language = st.session_state.get('language', 'English')
    
    # Handle nested keys
    keys = key.split('.')
    value = TRANSLATIONS[language]
    for k in keys:
        value = value.get(k, k)
    
    return value

def validate_email(email):
    """Simple email validation"""
    return '@' in email and '.' in email.split('@')[1] 