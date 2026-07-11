import pandas as pd 
from create_pdf import PDF 


#Load in the data
df = pd.read_csv("EbayPcLaptopsAndNetbooksUnclean.csv")
original_df = df.copy()

shape=df.shape
missing=df.isna().sum()
duplicates=df.duplicated().sum()

print("Dataset info:\n")
df.info()
print(f"\nDataset Shape: {shape}")
print(f"\nNumber of duplicates:{duplicates}\n")

print("--- Missing Values BEFORE ---")  
print(missing)


#Remove duplicate
df = df.drop_duplicates()
print(df.shape)


currency = df["Price"].str.extract(r'([^\d])')

df["Price"] = df["Price"].str.extract(
r'(\d+\.?\d*)').astype(float)

df.insert(loc = 2,column =  "Currency",value = currency)

df.rename(columns={"Price": "Price Value"}, inplace=True)


resolution =  df["Maximum Resolution"].str.extract(r'(\d+)\s*x\s*(\d+)')

df["Resolution Width"] = resolution[0].astype(float)


df["Resolution Height"] = resolution[1].astype(float)


df["Screen Size"]= df["Screen Size"].astype(str).str.extract(r"([\d\.]+)").astype(float)

df["Release Year"]= df["Release Year"].astype(str).str.extract(r"(\d{4})")

numeric=df.select_dtypes(
include="number")

df[numeric.columns] = numeric.fillna(numeric.median())

categorical=df.select_dtypes(
exclude="number")

df[categorical.columns] =categorical.fillna("Unknown")

#Remove useless columns
drop_cols=["Seller Note","Condition","Maximum Resolution"]
df=df.drop(columns=drop_cols)

print(f"Dataset shape: {df.shape}")
print("--- Missing Values AFTER Cleaning ---")
print(df.isna().sum())

#Save clean data
df.to_csv("Clean_pclaptop_data.csv",index = False)


#Make a pdf

pdf = PDF(bg_color = (25, 55, 109),header_text = "Laptop Data Cleaning Report")

#Page 1 
overview = """
Dataset: PC & Laptop Dataset 

This report contains data
cleaning results and dataset
information.

Generated automatically using
Python and FPDF.
 """
preview = original_df[["Price","Ram Size", "Maximum Resolution","Screen Size",  "Release Year"]]

pdf.cover_page(
title = "eBay PC & Laptop Dataset Cleaning Report",
df = preview,
overview = overview, 
dataset = "Laptop Dataset", 
github = "https://github.com/Mpho048/Data-Cleaning")

#Page 2
pdf.dataset_information(original_df)


#Page 3
summary = [
"Loaded and inspected the dataset.",

"Removed duplicate records.",

"Extracted the currency symbol from the price column.",

"Converted product prices to numeric values." ,

"Split maximum screen resolution into width and height columns.",

"Converted screen size measurements to numeric values.",

"Standardized release year values.",

"Filled missing numeric values using the median.",

"Filled missing categorical values with 'Unknown'.",

f"Final dataset shape after cleaning: {df.shape[0]} rows and {df.shape[1]} columns.",

"Removed unnecessary columns (Seller Note, Condition, and Maximum Resolution).",

"Verified the dataset after cleaning.",

"Prepared the dataset for exploratory data analysis."

]

pdf.insights(title = "Data Cleaning Summary",findings = summary)

pdf.output("Clean_laptop_data.pdf")