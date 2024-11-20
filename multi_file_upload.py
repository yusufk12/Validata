import pandas as pd

def load_data(file_path):
    """
    Loads dataset from the given file path.
    
    Args:
        file_path (str): Path to the data file (CSV, Excel, or HTML).
        
    Returns:
        pd.DataFrame: Loaded dataset as a Pandas DataFrame.
    """
    try:
        if file_path.endswith('.csv'):
            data = pd.read_csv(file_path)
        elif file_path.endswith('.xlsx'):
            data = pd.read_excel(file_path)
        elif file_path.endswith('.html'):
            data = pd.read_html(file_path)[0]  # read_html returns a list of DataFrames, so select the first one
        else:
            raise ValueError("Unsupported file format. Use CSV, Excel, or HTML.")
        print(f"Data loaded successfully from {file_path}")
        return data
    except Exception as e:
        print(f"Error loading data from {file_path}: {e}")
        return None

if __name__ == "__main__":

    # List of file paths to load
    file_paths = [
        'Hospital Patient Dataset Validata.xlsx',
        'Hospital Patient Dataset Validata.csv',
        'Large Hospital Dataset.csv',
        'Large Hospital Dataset.xlsx'
    ]
    
    # Loop through each file path and load the data
    for file_path in file_paths:
        data = load_data(file_path)
        if data is not None:
            print(f"First few rows from {file_path}:")
            print(data.head())  # Display the first few rows of the dataset
