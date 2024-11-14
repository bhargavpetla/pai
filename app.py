# app.py

import os
import json
import logging
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from langchain.chains import LLMChain
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain.schema import SystemMessage
from langchain.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import re

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
groq_api_key = os.getenv('GROQ_API_KEY')

if not groq_api_key:
    logger.error("Environment variable GROQ_API_KEY is missing. Please set it in your environment or .env file.")
    raise ValueError("Missing environment variable: GROQ_API_KEY")

# Initialize the app
app = Flask(__name__)
CORS(app)

# Initialize ChatGroq model
try:
    model_name = 'llama3-8b-8192'
    groq_chat = ChatGroq(groq_api_key=groq_api_key, model_name=model_name)
    logger.info("ChatGroq model initialized successfully.")
except Exception as e:
    logger.error(f"Failed to initialize ChatGroq: {e}")
    raise

# Load embeddings data
try:
    embeddings_file = 'embeddings.json'
    with open(embeddings_file, 'r', encoding='utf-8') as f:
        embeddings_data = json.load(f)
    logger.info("Embeddings data loaded successfully.")
except FileNotFoundError:
    logger.error(f"Embeddings file '{embeddings_file}' not found.")
    raise
except json.JSONDecodeError as e:
    logger.error(f"Error decoding JSON in '{embeddings_file}': {e}")
    raise

# Initialize FAISS index
try:
    embedding_dim = len(embeddings_data[0]['embedding'])
    index = faiss.IndexFlatL2(embedding_dim)
    embedding_vectors = np.array([item['embedding'] for item in embeddings_data]).astype('float32')
    index.add(embedding_vectors)
    logger.info("FAISS index initialized and embeddings added.")
except Exception as e:
    logger.error(f"Error initializing FAISS index: {e}")
    raise

# Load SentenceTransformer model
try:
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    logger.info("SentenceTransformer model loaded successfully.")
except Exception as e:
    logger.error(f"Error loading SentenceTransformer model: {e}")
    raise

# Set up chat memory and prompts
system_prompt = 'You are a friendly conversational chatbot only responding to AI use cases and related topics.'
memory = ConversationBufferWindowMemory(k=5, memory_key="chat_history", return_messages=True)

prompt_template = ChatPromptTemplate.from_messages([
    SystemMessage(content=system_prompt),
    MessagesPlaceholder(variable_name="chat_history"),
    HumanMessagePromptTemplate.from_template("{human_input}"),
])

conversation = LLMChain(
    llm=groq_chat,
    prompt=prompt_template,
    verbose=False,
    memory=memory,
)

# Mapping value chain keywords to image filenames
value_chain_images = {
    "asset reconstruction": "2.jpg",
    "ev battery": "3.jpg",
    "asset management": "4.jpg",
    "chemical manufacturing": "5.jpg",
    "pharma": "6.jpg",
    "consumer durables": "7.jpg",
    "retail": "8.jpg",
    "banking": "9.jpg",
    "payment processing": "10.jpg",
    "manufacturing": "11.jpg",
    "fabtech": "12.jpg",
    "petroleum": "13.jpg"
}

@app.route('/value_chain_image/<filename>')
def value_chain_image(filename):
    return send_from_directory('frontend/src/assets/value_chain', filename)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip().lower()

        # Explicitly check if the user is asking for a value chain
        if "value chain" in user_message:
            for keyword, filename in value_chain_images.items():
                if keyword in user_message:
                    image_url = f"{request.url_root}value_chain_image/{filename}"
                    return jsonify({
                        'response': f"Here is the {keyword.replace('_', ' ').title()} value chain.",
                        'image': image_url
                    }), 200

        # If no value chain request is detected, process as an AI use case query
        query_embedding = embedding_model.encode(user_message).astype('float32')
        k = 5
        distances, indices = index.search(np.array([query_embedding]), k)
        threshold = 0.7
        relevant_contexts = [embeddings_data[i]['content'] for i, d in zip(indices[0], distances[0]) if d < threshold]

        if not relevant_contexts:
            return jsonify({'response': "This question is not related to AI use cases, so I cannot answer."}), 200

        context = "\n".join(relevant_contexts[:4])  # Limit to top 4
        conversation.memory.chat_memory.add_user_message(user_message)
        conversation.memory.chat_memory.add_ai_message(context)

        response = conversation.predict(human_input=user_message)
        return jsonify({'response': format_numbered_lists(response)}), 200

    except Exception as e:
        logger.exception(f"Error in /chat endpoint: {e}")
        return jsonify({'error': 'An unexpected error occurred.'}), 500

@app.route('/suggestions', methods=['POST'])
def suggestions():
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip().lower()

        # Check if the last user query was for a value chain
        if "value chain" in user_message:
            return jsonify({'suggestions': [f"Tell me more about {keyword} value chain" for keyword in list(value_chain_images.keys())[:4]]})
        
        # Otherwise, provide general AI use case suggestions
        query_embedding = embedding_model.encode(user_message).astype('float32')
        k = 5
        distances, indices = index.search(np.array([query_embedding]), k)
        threshold = 0.7
        suggestions = [embeddings_data[i]['content'] for i, d in zip(indices[0], distances[0]) if d < threshold][:4]

        if not suggestions:
            suggestions = [
                "What are some AI use cases in manufacturing?",
                "How can AI improve customer service?",
                "What are the benefits of AI in healthcare?",
                "Show me AI use cases for supply chain."
            ]

        return jsonify({'suggestions': suggestions})

    except Exception as e:
        logger.exception(f"Error in /suggestions endpoint: {e}")
        return jsonify({'error': 'Failed to generate suggestions.'}), 500

@app.route('/reset_chat', methods=['POST'])
def reset_chat():
    try:
        conversation.memory.chat_memory.clear()
        logger.info("Conversation memory has been reset.")
        return jsonify({'message': 'Conversation memory has been reset.'}), 200
    except Exception as e:
        logger.error(f"Error resetting conversation memory: {e}")
        return jsonify({'error': 'Failed to reset conversation memory.'}), 500

@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Flask backend is running.'}), 200

def format_numbered_lists(text):
    lines = text.split('\n')
    formatted_lines = []
    for line in lines:
        match = re.match(r'^(\d+)\.\s+(.*)', line)
        if match:
            formatted_lines.append(f"{match[1]}. {match[2]}")
        else:
            formatted_lines.append(line)
    return '\n'.join(formatted_lines)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002, debug=True, use_reloader=False)
