eBay PC & Laptop Data Cleaning

Overview

This project demonstrates a complete data cleaning workflow for an eBay PC & Laptop dataset. The dataset was cleaned and standardized to prepare it for exploratory data analysis and machine learning.

Cleaning Tasks

- Removed duplicate records
- Extracted currency symbols
- Converted prices to numeric values
- Split screen resolution into width and height columns
- Standardized screen size measurements
- Standardized release year values
- Filled missing numeric values using the median
- Filled missing categorical values
- Removed unnecessary columns
- Generated an automated PDF report

Files

- "ebay_laptop_cleaning.py" – Main cleaning script
- "Clean_laptop_data.pdf" – Generated PDF report
- "EbayPcLaptopsAndNetbooksUnclean.csv" – Original dataset
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

python ebay_laptop_cleaning.py

Output

- Cleaned laptop dataset
- Automated PDF cleaning report

Author

Mpho
