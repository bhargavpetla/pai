# list_models.py

import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

# Check if GROQ_API_KEY is set
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in environment variables.")

# Configure API endpoint and headers
MODELS_API_URL = 'https://api.groq.com/openai/v1/models'
HEADERS = {
    'Authorization': f'Bearer {GROQ_API_KEY}',
    'Content-Type': 'application/json'
}

# Get the list of models
response = requests.get(MODELS_API_URL, headers=HEADERS)
if response.status_code == 200:
    models_data = response.json()
    models = models_data.get('data', [])
    print("Available models:")
    for model in models:
        print(f"- {model['id']}")
else:
    print(f"Error fetching models: {response.status_code}")
    print(response.text)
