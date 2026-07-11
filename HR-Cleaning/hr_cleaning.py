import pandas as pd
from create_pdf import PDF 
import numpy as np 

#Load the data
df = pd.read_csv("hr_attrition_dirty.csv")
original_df = df.copy()

print("Data Info:")
df.info()

duplicates=df.duplicated().sum()
print(f"\nNumber of duplicates:{duplicates}\n")
print(f'Dataset shape :{df.shape}')

print("--- Missing Values BEFORE Cleaning ---")
missing = df.isna().sum()
print(missing)
print()

# Cleaning data
df = df.drop_duplicates()
    
categorical=df.select_dtypes(
exclude="number") 

def clean_text_columns(df,categories):# best play it safe
    for item in categories:
        df[item] = df[item].str.strip()
    return df 

df = clean_text_columns(df,categorical.columns)


df["business_travel"] = df["business_travel"].fillna('Unknown')


df["department"] = df["department"].str.title()

df["department"] = df["department"].fillna("Unknown")

department = {
"Fin":"Finance", 
"Slaes": "Sales",
"Mktg": "Marketing", 
"R&D": "Research & Development", 
"Ops": "Operations",
"H.R": "Human Resources", 
"It": "IT Dept",
"It Dept": "IT Dept",
"Humanresources" : "Human Resources"
}

df["department"] = df["department"].replace(department)


negative = ["job_satisfaction","performance_rating","work_life_balance","num_companies_worked","job_level"]

def fix_negative_values(df,numbers):
    """Turn negative value in to positive values by using abs()"""
    for item in numbers:
        df[item] = df[item].abs()
    return df

df = fix_negative_values(df,negative)


age_mask = ((df["age"] <= 0) | (df["age"] > 77) | (df["age"] < 18))

df.loc[age_mask,"age"] = df["age"].median()


df["attrition"]  = df["attrition"].str.title() 
att_map = {
"N":"No",
"Y":"Yes",
"True":"Yes",
"False":"No",
"1":"Yes",
"0":"No",
"Stayed": "No",
"Left": "Yes",
"Unknown" : np.nan,
"Maybe" : np.nan,
}
df["attrition"] = df["attrition"].replace(att_map)


df.dropna(subset = ["attrition","employee_id"],inplace = True)

# Outliers in monthly_income
Q1 = df["monthly_income"].quantile(0.25)

Q3 = df["monthly_income"].quantile(0.75)

IQR = Q3 - Q1

lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

outliers = df[
    (df["monthly_income"] < lower) |
    (df["monthly_income"] > upper)
]

print(f"\nNumber of outliers: {len(outliers)}\n")

print(f"Dataset shape: {df.shape}")
print("--- Missing Values AFTER Cleaning ---")
print(df.isna().sum())

#Save clean data
df.to_csv("Clean_hr_data.csv",index = False )


#Generate a PDF Report
pdf = PDF(bg_color = (25, 55, 109),header_text = "Cleaning HR Attrition Data")

overview = """
Dataset: HR Dataset 

This report contains data
cleaning results and dataset
information.

Generated automatically using
Python and FPDF.
 """
preview = original_df[["employee_id", "age","department","monthly_income", "attrition"]][9:]

#Page 1
pdf.cover_page(title = "HR Attrition Cleaning Report",dataset = "HR Dataset",overview = overview,df = preview,github = "https://github.com/Mpho048/Data-Cleaning")

#Page 2
pdf.dataset_information(original_df)


insights = [
"Removed duplicate records.",

f"Shape of the data after cleaning,rows: {df.shape[0]} and columns: {df.shape[1]}.",

"Trimmed leading and trailing whitespace from text columns.",

"Standardized department names.",

"Corrected inconsistent attrition values.",

"Replaced invalid department entries.",

"Filled missing values where appropriate.",

"Removed records with missing employee IDs or attrition status.",

"Corrected invalid age values using the median age.",

"Converted negative numeric values to positive values where applicable.",

f"Investigated potential outliers in monthly income and only {len(outliers)} where detected",
]

pdf.insights(title = "Data Cleaning Summary",findings = insights)

pdf.output("Clean_hr_report.pdf")

    
                  