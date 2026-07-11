Retail Sales Data Cleaning

Overview

This project demonstrates a complete data cleaning workflow for a retail sales dataset using Python and pandas. The project focuses on recovering missing information, improving data quality, and generating an automated PDF report.

Cleaning Tasks

- Removed duplicate records
- Standardized text columns
- Recovered missing product names
- Recovered missing unit prices
- Filled missing discount values
- Converted transaction dates to datetime format
- Removed incomplete transactions
- Generated an automated PDF report

Dataset

The dataset is not included in this repository because its license does not allow redistribution.

Please download the dataset named:

"dirty_cafe_sales.csv"

from Kaggle and place it inside this project folder before running the script.

Files

- "retail_data.py" – Main cleaning script
- "Clean_retail_data.pdf" – Generated PDF report
- "create_pdf.py" – Shared PDF report module

Dataset Source

Kaggle

Technologies

- Python
- pandas
- NumPy
- FPDF

How to Run

1. Download "dirty_cafe_sales.csv" from Kaggle.
2. Install the required packages:

pip install -r requirements.txt

3. Run the project:

python retail_data.py

Output

- Cleaned retail dataset
- Automated PDF cleaning report

Author

Mpho
