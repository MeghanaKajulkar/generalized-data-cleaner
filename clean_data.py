import pandas as pd
import json5
import os

def load_config(config_path):
    """Load cleaning rules from config file."""
    with open(config_path, 'r') as file:
        config = json5.load(file)
    return config

def clean_data(file_path, config):
    """Clean the data according to the specified rules."""
    # Read the dataset
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    elif file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path)
    elif file_path.endswith('.json'):
        df = pd.read_json(file_path)
    else:
        print("Unsupported file type.")
        return
    
    # Apply cleaning rules
    if config.get("drop_missing"):
        df.dropna(inplace=True)
    
    if config.get("drop_duplicates"):
        df.drop_duplicates(inplace=True)
    
    # Example of normalizing numeric columns
    for column in config.get("normalize_columns", []):
        if column in df.columns:
            df[column] = (df[column] - df[column].mean()) / df[column].std()
    
    # Save the cleaned data in the output directory
    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_file_path = os.path.join(output_dir, f"cleaned_{os.path.basename(file_path)}")
    df.to_csv(output_file_path, index=False)
    print(f"Cleaned data saved to {output_file_path}")

def main():
    config_path = 'config.json5'
    config = load_config(config_path)
    
    # Loop through all files in the input directory and clean them
    input_dir = 'input'
    for file in os.listdir(input_dir):
        if file.endswith('.csv') or file.endswith('.xlsx') or file.endswith('.json'):
            clean_data(os.path.join(input_dir, file), config)

if __name__ == "__main__":
    main()
