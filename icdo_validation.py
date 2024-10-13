# Importing necessary libraries
import pandas as pd  # Used for data manipulation and analysis
import json  # Used if we need to load or manage JSON configurations or standards in the future

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
def validate_histology(row_value):
    """
    Validates the Histology field to ensure it matches one of the allowed values.

    Args:
        row_value (str): Value from the "Histology" column.

    Returns:
        str or None: An error message if validation fails, otherwise None.
    """
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
    # If the value is not in the valid list, return an error message
    if row_value not in valid_histology:
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
    # If the value is not in the valid list, return an error message
    if row_value not in valid_staging_systems:
        return f"Invalid staging system value: '{row_value}'. Suggested correction: Use one of the standard values, such as 'AJCC9', 'AJCC8', or 'AJCC7'."
    return None

# Function to apply validations to the dataset
def validate_icdo_data(dataset):
    """
    Validates the ICD-O related fields in the dataset.

    Args:
        dataset (pd.DataFrame): The dataset to validate.

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
            histology_issue = validate_histology(histology_value)
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
def generate_compliance_report(issues, compliance_percentages):
    """
    Generates a compliance report by printing out any validation issues found.

    Args:
        issues (list): A list of validation issues.
        compliance_percentages (dict): A dictionary containing compliance percentages for each column.
    """
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

# Main script block
def main():
    """
    Main function to load the dataset, validate ICD-O fields, and generate a compliance report.
    """
    # Specify the file path of the dataset
    file_path = "Hospital Patient Dataset Validata.csv"
    
    # Load the dataset
    data = load_dataset(file_path)
    
    # If the dataset is successfully loaded, proceed with validation
    if data is not None:
        validation_issues, compliance_percentages = validate_icdo_data(data)
        generate_compliance_report(validation_issues, compliance_percentages)

# Execute the main function if the script is run directly
if __name__ == "__main__":
    main()