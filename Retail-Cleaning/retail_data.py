import pandas as pd 
from create_pdf import PDF



#Load in the data
df = pd.read_csv("retail_store_sales.csv")
missing = df.isna().sum()


pdf = PDF()

#Page 1
preview = df[["Item","Price Per Unit","Quantity", "Total Spent"]]

overview = """
Dataset: Retail Dataset 

This report contains data
cleaning results and dataset
information.

Generated automatically using
Python and FPDF.
"""

pdf.cover_page(df = preview,title = "Cleaning Report",dataset = "Retail Store Sales",overview = overview, github = "https://github.com/Mpho048/Data-Cleaning")

print("Dataset info:\n")
df.info()
shape  = df.shape
print(f"\nDataset Shape: {shape}")

print("--- Missing Values BEFORE Cleaning ---")
print(missing)


#Page 2
pdf.dataset_information(df)



#Duplicates
duplicates = df.duplicated().sum()
df.drop_duplicates(inplace=True)

#Category formatting
cols  = ["Transaction ID","Category", "Customer ID","Payment Method","Location", "Item"]
def format_category(df,categories):# best play it safe
    for item in categories:
        df[item] = df[item].str.strip()
    return df
    
df = format_category(df,cols)           
df["Category"] = df["Category"].str.title()

##Price Per Unit × Quantity = Total Spent ##
price = df["Price Per Unit"].isna()
df.loc[price,"Price Per Unit"] = df.loc[price,"Total Spent"] / df.loc[price,"Quantity"]


category_item_map = df.groupby("Category")["Item"].unique().to_dict()


item_mask = df["Item"].isna()

single_items = {
    cat: str(items[0])
    for cat, items in category_item_map.items()
    if len(items) == 1
}

df.loc[item_mask, "Item"] = df.loc[item_mask, "Category"].map(single_items).fillna("Unknown_Item")


df["Discount Applied"] = (df["Discount Applied"].fillna(False).astype(bool))

df.dropna(subset = ["Quantity", "Total Spent"], inplace = True)

# --- 2. DATA TYPE ENFORCEMENT ---
df["Transaction Date"] = pd.to_datetime(df["Transaction Date"], errors = "coerce") 

print("\n\nShape of the dataset now:",df.shape)
print(df.isna().sum())


insight = (
    f"Original dataset shape: {shape[0]} rows and {shape[1]} columns.",

    f"Duplicate rows removed: {duplicates}",

    "Missing Price Per Unit values were recovered using:\n\tPrice Per Unit = Total Spent / Quantity",

    f"Missing Item values were recovered using category relationships.",  

    "Missing discount values were assumed as False.",

    "Rows missing Quantity or Total Spent were removed.",

    "Transaction Date converted to datetime format.",

    f"Final dataset shape after cleaning: {df.shape[0]} rows and {df.shape[1]} columns.",

    "Dataset is now structured and ready for analysis."
)

pdf.insights(insight,title="Key Cleaning Insights")

#save clean data
df.to_csv("Clean_ retail_data.csv",index = False )

#Save pdf report
pdf.output("Clean_retail_data.pdf")