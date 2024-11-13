# process_data.py

import os
import json
import pandas as pd
import logging
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from nltk.tokenize import sent_tokenize
import nltk
from tqdm import tqdm

# Initialize NLTK data
nltk.download('punkt')

def setup_logging(log_file='process_data.log'):
    """
    Configures logging for the script.

    :param log_file: Name of the log file.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

def load_environment_variables():
    """
    Loads environment variables from a .env file.

    :return: Dictionary of environment variables.
    """
    load_dotenv()
    groq_api_key = os.getenv('GROQ_API_KEY')
    
    if not groq_api_key:
        logging.error("GROQ_API_KEY not found in environment variables.")
        raise ValueError("GROQ_API_KEY not found in environment variables.")
    
    return {
        'GROQ_API_KEY': groq_api_key
    }

def initialize_embedding_model(model_name='all-MiniLM-L6-v2'):
    """
    Initializes the SentenceTransformer model.

    :param model_name: Name of the SentenceTransformer model.
    :return: Initialized SentenceTransformer model.
    """
    try:
        model = SentenceTransformer(model_name)
        logging.info(f"Loaded SentenceTransformer model '{model_name}'.")
        return model
    except Exception as e:
        logging.error(f"Error loading SentenceTransformer model '{model_name}': {e}")
        raise

def read_excel_file(excel_file):
    """
    Reads an Excel file and retrieves all sheet names.

    :param excel_file: Path to the Excel file.
    :return: List of sheet names.
    """
    try:
        xl = pd.ExcelFile(excel_file)
        sheet_names = xl.sheet_names
        logging.info(f"Found sheets: {sheet_names}")
        return sheet_names
    except FileNotFoundError:
        logging.error(f"The file '{excel_file}' was not found.")
        raise
    except Exception as e:
        logging.error(f"Error reading '{excel_file}': {e}")
        raise

def process_sheet(sheet_name, df):
    """
    Processes a single sheet by extracting relevant columns, tokenizing into sentences,
    and preparing data entries.

    :param sheet_name: Name of the sheet.
    :param df: DataFrame of the sheet.
    :return: List of processed data entries.
    """
    data_entries = []
    
    # Define the columns to use for content. Adjust based on your needs.
    content_columns = ['Description', 'Use Case Description']
    
    # Check if required content columns exist
    for col in content_columns:
        if col not in df.columns:
            logging.warning(f"Column '{col}' not found in sheet '{sheet_name}'. Skipping this column.")
    
    # Combine specified content columns into a single 'combined_content' column
    df['combined_content'] = df[content_columns].apply(
        lambda row: ' '.join(row.dropna().astype(str)), axis=1
    )
    
    # Iterate through each row to tokenize and create data entries
    for idx, row in df.iterrows():
        combined_text = row.get('combined_content', '').strip()
        if not combined_text:
            logging.info(f"Row {idx + 1} in sheet '{sheet_name}' has no content. Skipping.")
            continue
        
        # Tokenize the combined text into sentences
        sentences = sent_tokenize(combined_text)
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence:
                # Extract additional metadata as needed
                sr_no = row.get('Sr. No.', None)
                industry = row.get('Industry', 'Unknown')
                role = row.get('Role', 'Unknown')
                title_of_use_case = row.get('Title of the Use Case', 'No Title')
                deep_tech_used = row.get('Deep Tech Used', 'N/A')
                potential_vector = row.get('Potential Vector', 'N/A')
                potential_vector_benefit = row.get('Potential Vector Benefit', 'N/A')
                use_case_case_study = row.get('Use Case/Case Study', 'N/A')
                casegenie_link = row.get('CaseGenie Link', 'N/A')
                dtsp = row.get('DTSP', 'N/A')
                
                data_entries.append({
                    'content': sentence,
                    'metadata': {
                        'sheet_name': sheet_name,
                        'row_index': idx + 1,  # 1-based indexing
                        'sr_no': sr_no,
                        'industry': industry,
                        'role': role,
                        'title_of_use_case': title_of_use_case,
                        'deep_tech_used': deep_tech_used,
                        'potential_vector': potential_vector,
                        'potential_vector_benefit': potential_vector_benefit,
                        'use_case_case_study': use_case_case_study,
                        'casegenie_link': casegenie_link,
                        'dtsp': dtsp
                    }
                })
                logging.debug(f"Processed sentence from row {idx + 1} in sheet '{sheet_name}'.")
    
    logging.info(f"Processed {len(data_entries)} sentences from sheet '{sheet_name}'.")
    return data_entries

def generate_embeddings(data_entries, embedding_model):
    """
    Generates embeddings for each data entry using the provided embedding model.

    :param data_entries: List of data entries.
    :param embedding_model: Initialized SentenceTransformer model.
    :return: List of data entries with embeddings.
    """
    logging.info("Generating embeddings...")
    
    for item in tqdm(data_entries, desc="Generating embeddings"):
        try:
            embedding = embedding_model.encode(item['content']).tolist()
            item['embedding'] = embedding
        except Exception as e:
            logging.error(f"Error generating embedding for content: '{item['content']}'. Error: {e}")
            item['embedding'] = []
    
    logging.info("Embedding generation completed.")
    return data_entries

def save_embeddings(data_entries, output_file='embeddings.json'):
    """
    Saves the data entries with embeddings to a JSON file.

    :param data_entries: List of data entries with embeddings.
    :param output_file: Name of the output JSON file.
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data_entries, f, indent=4, ensure_ascii=False)
        logging.info(f"Successfully saved {len(data_entries)} embeddings to '{output_file}'.")
    except Exception as e:
        logging.error(f"Error saving embeddings to '{output_file}': {e}")
        raise

def main():
    """
    Main function to orchestrate the data processing and embedding generation.
    """
    setup_logging()
    logging.info("Starting data processing...")
    
    # Load environment variables
    env_vars = load_environment_variables()
    
    # Initialize embedding model
    embedding_model = initialize_embedding_model()
    
    # Define the path to your Excel file
    excel_file = 'data.xlsx'  # Replace with your actual file path if different
    
    # Read Excel file and get sheet names
    sheet_names = read_excel_file(excel_file)
    
    all_data_entries = []
    
    # Process each sheet
    for sheet in sheet_names:
        logging.info(f"Processing sheet: '{sheet}'")
        try:
            df = pd.read_excel(excel_file, sheet_name=sheet)
            data_entries = process_sheet(sheet, df)
            all_data_entries.extend(data_entries)
        except Exception as e:
            logging.error(f"Failed to process sheet '{sheet}': {e}")
            continue
    
    if not all_data_entries:
        logging.warning("No data entries found. Exiting without generating embeddings.")
        return
    
    # Generate embeddings
    all_data_entries = generate_embeddings(all_data_entries, embedding_model)
    
    # Save embeddings to JSON
    save_embeddings(all_data_entries)
    
    logging.info("Data processing and embedding generation completed successfully.")

if __name__ == "__main__":
    main()
