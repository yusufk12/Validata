import pandas as pd

def load_data(file_path):
    """
    Loads oncology dataset from the given file path.
    
    Args:
        file_path (str): Path to the data file (CSV, Excel, or XML).
        
    Returns:
        pd.DataFrame: Loaded dataset as a Pandas DataFrame.
    """
    try:
        if file_path.endswith('.csv'):
            data = pd.read_csv(file_path)
        elif file_path.endswith('.xlsx'):
            data = pd.read_excel(file_path)
        elif file_path.endswith('.xml'):
            data = pd.read_xml(file_path)
        else:
            raise ValueError("Unsupported file format. Use CSV, Excel, or XML.")
        print("Data loaded successfully.")
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

if __name__ == "__main__":
    
    file_path = 'Hospital Patient Dataset Validata.xlsx'
    data = load_data(file_path)  # Call the load_data function to load the dataset
    if data is not None:
        print(data.head())  # Display the first few rows of the dataset