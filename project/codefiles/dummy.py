import pandas as pd  
 
df=pd.read_csv("C:\\Users\\sachi\\OneDrive\\Data_science_project\\data1.csv",encoding="ISO-8859-1")
df1=pd.read_csv("C:\\Users\\sachi\\OneDrive\\Data_science_project\\data1.csv",encoding="ISO-8859-1")

print(df.info())
print(df.shape) # tell number of rows and columns
print(df.head(10)) # check first 10 rows

print(df.isnull().sum()) # print the number of missing values

print(df["Country"].nunique())# number of unique country
print(df["Country"].unique())# name of all unique country

print(df["StockCode"].value_counts()) # gives stockcode according to the country
print(df[["StockCode","Country","Quantity"]].value_counts())

#---------------handling the missing data----------------------

print(df.isnull().sum()) # give the numbes of missing values in each column

# fill the missing values with unknow
df["Description"].fillna("Not Available",inplace=True)
print(df.isnull().sum())

# replacing the missing values of customer column with 0

df["CustomerID"].fillna(0,inplace=True)
print(df.isnull().sum())

df1.dropna(subset=["CustomerID"],inplace=True)
print(df1.isnull().sum()) #means "Remove rows where the 'CustomerID' column has missing (NaN) values."



#----------conversion of data type if needed------------------#

df["InvoiceDate"]=pd.to_datetime(df["InvoiceDate"],errors="coerce")# error="coerce"--handle unwanted values to replace with nan
df["StockCode"]=df["StockCode"].apply(str)

print(df.dtypes)

#-----conert categorial datatype----------------# optimized and take less memory

df["Country"]=df["Country"].astype("category")
df["StockCode"]=df["StockCode"].astype("category")
print(df.dtypes)


#---------convert all objects column automatically
# give the list of all col which has datatype as object, then convert it into numeric ..
# if conversion fails...it convert it into category

for col in df.select_dtypes(include=["object"]).columns:
    try:
        df[col]=pd.to_numeric(df[col])
    except:
        df[col]=df[col].astype("category")

print(df.dtypes)
            


# remove the duplicate records

# to check if duplicated records present or not

duplicate_rows=df.duplicated().sum()
# df.duplicated() return the boolian series and .sum() will count all duplicate
print(f"The number of duplicate rows {duplicate_rows}")     

# diplay the duplicate rows

print(df[df.duplicated()])

print("\n\n")
print(df[df.duplicated(keep="first")])# print duplicate values only..not the original one
print(df[df.duplicated(keep=False)])  # print both original and duplicate values

# drop the duplicate values

df.drop_duplicates(inplace=True)
print(df)

#---------------remove duplicate values based on columns---------------------

print(df.info())
print(df.isnull().sum())

# ------------handle negative values---------------

negative_values=(df.select_dtypes(include=['number'])<0).sum()
print(negative_values)

print("\nRows with negative values\n")
print(df[df["Quantity"]<0])
print(df[df["UnitPrice"]<0])
print(df.loc[df["Quantity"] < 0,["CustomerID" ,"Quantity"]])

# Another option to handle the negative values

df["Quantity"]=df["Quantity"].apply(lambda x:0 if x<0 else x)
df["UnitPrice"]=df["UnitPrice"].apply(lambda x :0 if x<0 else x)
negative_values=(df.select_dtypes(include=['number'])<0).sum()
print(negative_values)



#  save the cleaned data into a new fil csv or excel

df.to_csv("cleaned_data.csv",index=False)
print(df.dtypes)
df.to_excel("cleaned_data.xlsx",index=False)


