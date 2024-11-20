import pandas as pd
import numpy as np
import re

##loading datasets

def load_data(file_path):
    """
    Loads dataset from the given file path.

    Args:
        file_path (str): Path to the data file (CSV, Excel).

    Returns:
        pd.DataFrame: Loaded dataset as a Pandas DataFrame.
    """
    try:
        if file_path.endswith('.csv'):
            data = pd.read_csv(file_path)
        elif file_path.endswith('.xlsx'):
            data = pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file format. Use CSV or Excel.")
        print(f"Data loaded successfully from {file_path}")
        return data
    except Exception as e:
        print(f"Error loading data from {file_path}: {e}")
        return None
    
    ## ICD-10 validation fields function
def validate_icd10(data, dataset_name):
    """
    Validates ICD-10-related fields in the provided dataset.

    Args:
        data (pd.DataFrame): Dataset containing ICD-10 related columns.
        dataset_name (str): Name of the dataset to track compliance.

    Returns:
        dict: A dictionary containing compliance issues found during validation.
    """
    compliance_issues = []
    compliance_counts = {column: {'valid': 0, 'total': 0} for column in data.columns if column in [
        'Cause of Death', 'Cause of Death Attributable to Treatment', 'Vital Status', 'ICD Version', 'ICD Code', 'Disability', 'On Clinical Trial', 'Clinical Trial Numbers'
    ]}
    
    rules = {
        'Cause of Death': {
            'allow_null': True,
            'example': 'Malignant neoplasm of esophagus, C15',
            'regex': r'^C\d{1,2}(\.\d+)?(-C\d{1,2}(\.\d+)?)?(,C\d{1,2}(\.\d+)?(-C\d{1,2}(\.\d+)?)?)*$'  # Matches codes with decimals and ranges
        },
        'Cause of Death Attributable to Treatment': {
            'allow_null': True,
            'standard_values': ['Unknown', 'Probably Related', 'Definitely Related']
        },
        'Vital Status': {
            'allow_null': False,
            'standard_values': ['Alive', 'Dead']
        },
        'ICD Version': {
            'allow_null': False,
            'standard_values': ['ICD9', 'ICD10']
        },
        'ICD Code': {
            'allow_null': False,
            'standard_values': 'ICD code list'
        },
        'Disability': {
            'allow_null': True,
            'standard_values': [
                'Hearing difficulty', 'Vision difficulty', 'Cognitive difficulty',
                'Ambulatory difficulty', 'Self-care difficulty', 'Independent living difficulty'
            ]
        },
        'On Clinical Trial': {
            'allow_null': True,
            'binary': True
        },
        'Clinical Trial Numbers': {
            'allow_null': True
        }
    }

    # Validate each row
    for index, row in data.iterrows():
        for column, rule in rules.items():
            if column not in data.columns:
                continue

            value = row.get(column)
            compliance_counts[column]['total'] += 1

            if pd.isna(value) and rule.get('allow_null', False):
                compliance_counts[column]['valid'] += 1
                continue

            if 'regex' in rule:
                if re.match(rule['regex'], str(value)):
                    compliance_counts[column]['valid'] += 1
                else:
                    compliance_issues.append(
                        f"Dataset: {dataset_name}, Row {index + 1}, Column '{column}': Invalid value: '{value}'. Suggested correction: Use a valid ICD-10 code format."
                    )
            elif 'standard_values' in rule and isinstance(rule['standard_values'], list):
                if value in rule['standard_values']:
                    compliance_counts[column]['valid'] += 1
                else:
                    compliance_issues.append(
                        f"Dataset: {dataset_name}, Row {index + 1}, Column '{column}': Invalid value: '{value}'. Suggested correction: Use one of the standard values: {', '.join(rule['standard_values'])}."
                    )
            elif 'binary' in rule and rule['binary'] and value not in [0, 1, '0', '1', True, False, 'True', 'False']:
                compliance_issues.append(
                    f"Dataset: {dataset_name}, Row {index + 1}, Column '{column}': Invalid value: '{value}'. Suggested correction: Use binary values (0 or 1)."
                )

    return compliance_issues, compliance_counts

## data processing function 

if __name__ == "__main__":
    # List of file paths for multiple datasets
    file_paths = [
        'Hospital Patient Dataset Validata.csv',
        'Large Hospital Dataset.csv'
    ]
    
    # Loop through each dataset, load, and validate
    all_compliance_issues = []
    all_compliance_counts = {}

    for file_path in file_paths:
        data = load_data(file_path)
        if data is not None:
            dataset_name = file_path.split('/')[-1]
            compliance_issues, compliance_counts = validate_icd10(data, dataset_name)
            
            all_compliance_issues.extend(compliance_issues)
            all_compliance_counts[dataset_name] = compliance_counts
    
    # Display compliance issues for each dataset
    if all_compliance_issues:
        print("\nCompliance Issues Found:")
        for issue in all_compliance_issues:
            print(issue)
    else:
        print("All ICD-10 fields are compliant in both datasets.")

    # Compliance Summary for each dataset
    print(f"\nCompliance Summary:")
    for dataset_name, compliance_counts in all_compliance_counts.items():
        print(f"Dataset: {dataset_name}")
        for column, counts in compliance_counts.items():
            compliance_rate = (counts['valid'] / counts['total']) * 100 if counts['total'] > 0 else 100
            print(f"{column} Compliance: {compliance_rate:.2f}%")
        print("\n")  # New line after each dataset's summary
