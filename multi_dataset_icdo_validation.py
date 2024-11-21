# Importing necessary libraries
import pandas as pd  # Used for data manipulation and analysis
import json  # Used if we need to load or manage JSON configurations or standards in the future
from fuzzywuzzy import process  # Used for fuzzy matching to suggest corrections

# Function to load the dataset from a given file path
def load_dataset(file_path):
    """
    Loads the dataset from the provided file path.
    Supports CSV, Excel, and XML formats.

    Args:
        file_path (str): Path to the data file.

    Returns:
        pd.DataFrame: Loaded dataset as a Pandas DataFrame, or None if loading fails.
    """
    try:
        # Check the file extension and load accordingly
        if file_path.endswith('.csv'):
            return pd.read_csv(file_path)
        elif file_path.endswith('.xlsx'):
            return pd.read_excel(file_path)
        elif file_path.endswith('.xml'):
            return pd.read_xml(file_path)
        else:
            raise ValueError("Unsupported file format. Use CSV, Excel, or XML.")
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

# Function to validate the "Histology" field
def validate_histology(row_value, valid_histology):
    """
    Validates the Histology field to ensure it matches one of the allowed values.

    Args:
        row_value (str): Value from the "Histology" column.
        valid_histology (list): List of valid histology values.

    Returns:
        str or None: An error message if validation fails, otherwise None.
    """
    # Normalize the value for comparison
    row_value_normalized = row_value.strip().lower()
    valid_histology_normalized = [value.lower() for value in valid_histology]
    
    # If the value is not in the valid list, use fuzzy matching to suggest corrections
    if row_value_normalized not in valid_histology_normalized:
        closest_match, score = process.extractOne(row_value, valid_histology_normalized)
        if score > 80:  # Suggest correction if the similarity score is above 80
            return f"Invalid histology value: '{row_value}'. Suggested correction: '{closest_match}'."
        else:
            return f"Invalid histology value: '{row_value}'. Suggested correction: Use one of the standard values, such as 'Adenocarcinoma', 'Ductal Carcinoma', etc."
    return None

# Function to validate the "Staging System" field
def validate_staging_system(row_value):
    """
    Validates the Staging System field to ensure it matches one of the allowed staging systems.

    Args:
        row_value (str): Value from the "Staging System" column.

    Returns:
        str or None: An error message if validation fails, otherwise None.
    """
    # List of valid staging systems based on accepted oncology standards
    valid_staging_systems = ["AJCC9", "AJCC8", "AJCC7"]
    # Normalize the value for comparison
    row_value_normalized = row_value.strip().lower()
    valid_staging_systems_normalized = [value.lower() for value in valid_staging_systems]
    
    # If the value is not in the valid list, return an error message
    if row_value_normalized not in valid_staging_systems_normalized:
        return f"Invalid staging system value: '{row_value}'. Suggested correction: Use one of the standard values, such as 'AJCC9', 'AJCC8', or 'AJCC7'."
    return None

# Function to apply validations to the dataset
def validate_icdo_data(dataset, valid_histology):
    """
    Validates the ICD-O related fields in the dataset.

    Args:
        dataset (pd.DataFrame): The dataset to validate.
        valid_histology (list): List of valid histology values.

    Returns:
        tuple: A list of validation issues found in the dataset and a dictionary with compliance percentages.
    """
    issues = []  # Initialize an empty list to store any validation issues
    total_histology = 0
    compliant_histology = 0
    total_staging = 0
    compliant_staging = 0

    # Loop through each row in the dataset
    for index, row in dataset.iterrows():
        # Validate Histology field
        histology_value = row.get('Histology', '')
        if histology_value:
            total_histology += 1
            histology_issue = validate_histology(histology_value, valid_histology)
            if histology_issue:
                issues.append(f"Row {index + 1}, Column 'Histology': {histology_issue}")
            else:
                compliant_histology += 1

        # Validate Staging System field
        staging_value = row.get('Staging System', '')
        if staging_value:
            total_staging += 1
            staging_issue = validate_staging_system(staging_value)
            if staging_issue:
                issues.append(f"Row {index + 1}, Column 'Staging System': {staging_issue}")
            else:
                compliant_staging += 1

    # Calculate compliance percentages
    compliance_percentages = {
        'Histology': (compliant_histology / total_histology * 100) if total_histology > 0 else 0,
        'Staging System': (compliant_staging / total_staging * 100) if total_staging > 0 else 0
    }

    return issues, compliance_percentages

# Function to generate a compliance report based on the validation results
def generate_compliance_report(dataset_name, issues, compliance_percentages):
    """
    Generates a compliance report by printing out any validation issues found.

    Args:
        dataset_name (str): The name of the dataset being validated.
        issues (list): A list of validation issues.
        compliance_percentages (dict): A dictionary containing compliance percentages for each column.
    """
    print(f"\nDataset: {dataset_name}")
    if not issues:
        # If no issues found, print compliance confirmation
        print("All records are compliant.")
    else:
        # If issues are found, print each one with detailed information
        print("Compliance Issues Found:")
        for issue in issues:
            print(issue)

    # Print compliance percentages
    print("\nCompliance Summary:")
    for field, percentage in compliance_percentages.items():
        print(f"{field} Compliance: {percentage:.2f}%")

    # Print common errors summary
    if issues:
        error_summary = {}
        for issue in issues:
            error_value = issue.split("'")[1]
            if error_value in error_summary:
                error_summary[error_value] += 1
            else:
                error_summary[error_value] = 1
        print("\nCommon Histology Errors:")
        for error, count in sorted(error_summary.items(), key=lambda x: x[1], reverse=True):
            print(f"'{error}' occurred {count} times.")

# Main script block
def main():
    """
    Main function to load multiple datasets, validate ICD-O fields, and generate compliance reports for each.
    """
    # List of file paths for the datasets to be validated
    file_paths = [
        "Hospital Patient Dataset Validata.csv",
        "Large Hospital Dataset.csv"
    ]
    
    # List of valid histology values based on ICD-O standards
    valid_histology = [
        "Adenocarcinoma", "Ductal Carcinoma", "Small Cell Carcinoma",
        "Acinar adenocarcinoma", "Mucinous (colloid) acinar adenocarcinoma",
        "Signet ring-like cell acinar adenocarcinoma", "Sarcomatoid acinar adenocarcinoma",
        "Prostatic intraepithelial neoplasia (high grade)", "Intraductal carcinoma",
        "Papillary Ductal Adenocarcinoma", "Urothelial Carcinoma", "Squamous cell carcinoma",
        "Basal cell carcinoma", "Well-differentiated neuroendocrine tumor",
        "Large cell neuroendocrine carcinoma"
    ]
    
    # Loop through each file path, load the dataset, and perform validation
    for file_path in file_paths:
        # Load the dataset
        data = load_dataset(file_path)
        
        # If the dataset is successfully loaded, proceed with validation
        if data is not None:
            validation_issues, compliance_percentages = validate_icdo_data(data, valid_histology)
            generate_compliance_report(file_path, validation_issues, compliance_percentages)

# Execute the main function if the script is run directly
if __name__ == "__main__":
    main()
