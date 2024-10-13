import pandas as pd

def validate_icd10(data):
    """
    Validates ICD-10-related fields in the provided dataset.

    Args:
        data (pd.DataFrame): Dataset containing ICD-10 related columns.

    Returns:
        dict: A dictionary containing compliance issues found during validation.
    """
    compliance_issues = []
    compliance_counts = {column: {'valid': 0, 'total': 0} for column in data.columns if column in [
        'Cause of Death', 'Cause of Death Attributable to Treatment', 'Vital Status', 'ICD Version', 'ICD Code', 'Disability', 'On Clinical Trial', 'Clinical Trial Numbers'
    ]}
    
    # ICD-10 Validation Rules
    rules = {
        'Cause of Death': {
            'allow_null': True,
            'example': 'Malignant neoplasm of esophagus, C15',
            'standard_values': 'ICD10 Codes'
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
            'allow_null': True,  # Only if not on clinical trial
            'binary': True
        },
        'Clinical Trial Numbers': {
            'allow_null': True
        }
    }

    # Validate each row in the dataset
    for index, row in data.iterrows():
        for column, rule in rules.items():
            value = row.get(column)

            # Skip validation if column not in dataset
            if column not in data.columns:
                continue

            compliance_counts[column]['total'] += 1

            if pd.isna(value) and rule.get('allow_null', False):
                compliance_counts[column]['valid'] += 1
                continue
            
            # Check for binary fields
            if rule.get('binary', False):
                if value in [1, None]:
                    compliance_counts[column]['valid'] += 1
                else:
                    compliance_issues.append(
                        f"Row {index + 1}, Column '{column}': Invalid value: '{value}'. Suggested correction: Should be '1' if the patient is on a clinical trial, otherwise leave blank."
                    )

            # Validate standard values
            elif 'standard_values' in rule:
                if isinstance(rule['standard_values'], list) and value in rule['standard_values']:
                    compliance_counts[column]['valid'] += 1
                elif isinstance(rule['standard_values'], list) and value not in rule['standard_values']:
                    compliance_issues.append(
                        f"Row {index + 1}, Column '{column}': Invalid value: '{value}'. Suggested correction: Use one of the standard values, such as {', '.join(rule['standard_values'])}."
                    )
                elif rule['standard_values'] == 'ICD10 Codes':
                    # Placeholder for ICD-10 codes validation, assuming a function validate_icd10_code exists
                    if validate_icd10_code(value):
                        compliance_counts[column]['valid'] += 1
                    else:
                        compliance_issues.append(
                            f"Row {index + 1}, Column '{column}': Invalid ICD-10 code: '{value}'. Please refer to the ICD-10 codes for a valid entry."
                        )

    return compliance_issues, compliance_counts

def validate_icd10_code(code):
    """
    Placeholder function for ICD-10 code validation.

    Args:
        code (str): ICD-10 code to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    # For demonstration purposes, assume all codes starting with 'C' are valid
    return code.startswith('C')

if __name__ == "__main__":
    # Load the dataset
    file_path = 'Hospital Patient Dataset Validata.csv'
    try:
        data = pd.read_csv(file_path)
        
        # Validate ICD-10 fields
        compliance_issues, compliance_counts = validate_icd10(data)

        # Display compliance issues
        if compliance_issues:
            print("Compliance Issues Found:")
            for issue in compliance_issues:
                print(issue)
        else:
            print("All ICD-10 fields are compliant.")

        # Compliance Summary
        total_rows = len(data)
        print(f"\nCompliance Summary:")
        for column, counts in compliance_counts.items():
            compliance_rate = (counts['valid'] / counts['total']) * 100 if counts['total'] > 0 else 100
            print(f"{column} Compliance: {compliance_rate:.2f}%")
    
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")