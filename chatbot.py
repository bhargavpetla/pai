import os
import json
import logging
from langchain.chains import LLMChain
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.messages import SystemMessage
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

def main():
    """
    This function sets up the Groq client, initializes embeddings, and handles the chat interaction via the terminal.
    """

    # -------------------- Configuration --------------------
    # Configure logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    # Load environment variables from .env file
    load_dotenv()
    groq_api_key = os.getenv('GROQ_API_KEY')

    if not groq_api_key:
        logger.error("GROQ_API_KEY not found in environment variables.")
        raise ValueError("GROQ_API_KEY not found in environment variables.")

    model = 'llama3-8b-8192'  # Ensure this model ID is valid

    # Initialize Groq LangChain chat object
    groq_chat = ChatGroq(
        groq_api_key=groq_api_key, 
        model_name=model
    )
    
    print("Hello! I'm your friendly Groq chatbot. I can help answer your questions, provide information, or just chat. I'm also super fast! Let's start our conversation!")

    system_prompt = 'You are a friendly conversational chatbot'
    conversational_memory_length = 5  # Number of previous messages the chatbot will remember during the conversation

    memory = ConversationBufferWindowMemory(
        k=conversational_memory_length, 
        memory_key="chat_history", 
        return_messages=True
    )

    # -------------------- Load Embeddings and Initialize FAISS --------------------
    try:
        with open('embeddings.json', 'r', encoding='utf-8') as f:
            embeddings_data = json.load(f)
        logger.debug("Successfully loaded embeddings.json.")
    except FileNotFoundError:
        logger.error("embeddings.json not found. Please ensure it exists.")
        raise

    if not embeddings_data:
        logger.error("embeddings.json is empty. Please ensure it contains embeddings.")
        raise ValueError("No embeddings found in 'embeddings.json'.")

    # Extract embedding dimensions
    embedding_dim = len(embeddings_data[0]['embedding'])  # Assumes all embeddings have the same dimension

    # Initialize FAISS index
    try:
        index = faiss.IndexFlatL2(embedding_dim)
        embedding_vectors = np.array([item['embedding'] for item in embeddings_data]).astype('float32')
        index.add(embedding_vectors)
        logger.debug("FAISS index successfully built and embeddings added.")
    except Exception as e:
        logger.exception("Error building FAISS index.")
        raise

    # -------------------- Initialize SentenceTransformer --------------------
    try:
        embedding_model = SentenceTransformer('all-MiniLM-L6-v2')  # Use the same model for consistency
        logger.debug("SentenceTransformer model loaded successfully.")
    except Exception as e:
        logger.exception("Error loading SentenceTransformer model.")
        raise

    # -------------------- Construct the Chat Prompt Template --------------------
    prompt_template = ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content=system_prompt
            ),  # Persistent system prompt
            MessagesPlaceholder(
                variable_name="chat_history"
            ),  # Placeholder for chat history
            HumanMessagePromptTemplate.from_template(
                "{human_input}"
            ),  # User's current input
        ]
    )

    # -------------------- Create the Conversation Chain --------------------
    conversation = LLMChain(
        llm=groq_chat,  # Groq LangChain chat object
        prompt=prompt_template,  # Constructed prompt template
        verbose=False,  # Set to True for detailed logs
        memory=memory,  # Conversation memory
    )

    # -------------------- Chat Loop --------------------
    while True:
        user_question = input("You: ")

        if user_question.lower() in ['exit', 'quit', 'bye']:
            print("Chatbot: Goodbye! Have a great day!")
            break

        if user_question:
            # Perform similarity search to retrieve relevant context
            try:
                # Generate embedding for the user query using SentenceTransformer
                query_embedding = embedding_model.encode(user_question).astype('float32')
                logger.debug(f"Generated query embedding: {query_embedding[:5]}...")  # Log first 5 values

                # Perform similarity search
                k = 5  # Number of nearest neighbors
                D, I = index.search(np.array([query_embedding]), k)
                context = "\n".join([embeddings_data[i]['content'] for i in I[0]])
                logger.debug(f"Similarity search results: Indices {I[0]}, Distances {D[0]}")
                logger.debug(f"Context for prompt: {context}")
            except Exception as e:
                logger.exception("Error during similarity search.")
                print("Chatbot: Sorry, I encountered an error while processing your request.")
                continue

            # Update the conversation memory with the context
            conversation.memory.chat_memory.add_user_message(user_question)
            conversation.memory.chat_memory.add_ai_message(context)

            # Generate a response using the conversation chain
            try:
                response = conversation.predict(human_input=user_question)
                print(f"Chatbot: {response}")
            except Exception as e:
                logger.exception("Error generating response from Groq API.")
                print("Chatbot: Sorry, I couldn't generate a response at the moment.")

if __name__ == "__main__":
    main()
