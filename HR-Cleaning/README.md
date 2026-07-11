HR Data Cleaning

Overview

This project demonstrates a complete data cleaning workflow using Python and pandas on an HR Attrition dataset. The goal was to improve data quality by correcting inconsistencies, handling missing values, validating records, and automatically generating a professional PDF report.

Cleaning Tasks

- Removed duplicate records
- Standardized department names
- Standardized attrition values
- Trimmed whitespace
- Filled missing values
- Removed rows with missing critical information
- Corrected invalid age values
- Corrected negative numeric values
- Investigated monthly income outliers using the IQR method
- Generated an automated PDF report

Files

- "hr_cleaning.py" – Main cleaning script
- "Clean_hr_report.pdf" – Generated PDF report
- "hr_attrition_dirty.csv" – Original dataset
- Clean_hr_data.csv - Cleaned dataset
- "create_pdf.py" – Shared PDF report module

Technologies

- Python
- pandas
- NumPy
- FPDF

How to Run

1. Install the required packages:

pip install -r requirements.txt

2. Run the project:

python hr_cleaning.py

Output

- Cleaned HR dataset
- Automated PDF cleaning report

Author

Mpho
