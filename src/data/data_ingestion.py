import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import yaml
import logging
import os
from src.utils.utils import setup_logger


logger = logging.getLogger(__name__)
def load_params(params_path: str) -> dict:
    """Load parameters from a YAML file."""
    try:
        with open(params_path, 'r') as file:
            params = yaml.safe_load(file)
        logger.debug(f'Parameters retrieved from {params_path}')
        return params
    except FileNotFoundError:
        logger.error(f'File not found: {params_path}')
        raise
    except yaml.YAMLError as e:
        logger.error(f'YAML error: {e}')
        raise
    except Exception as e:
        logger.error(f'Unexpected error: {e}')
        raise

def load_data(data_url: str) -> pd.DataFrame:
    """Load data from a CSV file."""
    try:
        df = pd.read_csv(data_url)
        logger.debug(f'Data loaded from {data_url}')
        return df
    except pd.errors.ParserError as e:
        logger.error(f'Failed to parse the CSV file: {e}')
        raise
    except Exception as e:
        logger.error(f'Unexpected error occurred while loading the data: {e}')
        raise

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """Preprocess the data by handling missing values, duplicates, and empty strings."""
    try:
        # Removing missing values
        df.dropna(inplace=True)
        # Removing duplicates
        df.drop_duplicates(inplace=True)
        # Removing rows with empty strings
        df = df[df['clean_comment'].str.strip() != '']
        
        logger.debug('Data preprocessing completed: Missing values, duplicates, and empty strings removed.')
        return df
    except KeyError as e:
        logger.error(f'Missing column in the dataframe: {e}')
        raise
    except Exception as e:
        logger.error(f'Unexpected error during preprocessing: {e}')
        raise

def save_data(train_data: pd.DataFrame, test_data: pd.DataFrame, data_path: str) -> None:
    """Save the train and test datasets, creating the raw folder if it doesn't exist."""
    try:
        raw_data_path = os.path.join(data_path, 'raw')
        
        # Create the data/raw directory if it does not exist
        os.makedirs(raw_data_path, exist_ok=True)
        
        # Save the train and test data
        train_data.to_csv(os.path.join(raw_data_path, "train.csv"), index=False)
        test_data.to_csv(os.path.join(raw_data_path, "test.csv"), index=False)
        
        logger.debug('Train and test data saved to %s', raw_data_path)
    except Exception as e:
        logger.error('Unexpected error occurred while saving the data: %s', e)
        raise

def main():
    try:
        # Load parameters from the params.yaml in the root directory
        params = load_params(params_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../params.yaml'))
        test_size = params['data_ingestion']['test_size']
        
        # Load data from the specified URL
        df = load_data(data_url='https://raw.githubusercontent.com/Himanshu-1703/reddit-sentiment-analysis/refs/heads/main/data/reddit.csv')
        
        # Preprocess the data
        final_df = preprocess_data(df)
        
        # Split the data into training and testing sets
        train_data, test_data = train_test_split(final_df, test_size=test_size, random_state=42)
        
        # Save the split datasets and create the raw folder if it doesn't exist
        save_data(train_data, test_data, data_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../data'))
        
    except Exception as e:
        logger.error(f'Failed to complete the data ingestion process: {e}')
        print(f"Error: {e}")

if __name__ == '__main__':
    setup_logger()
    main()