import pandas as pd
import mysql.connector

# 📌 Load Cleaned CSV (Fix dtype issue)
df = pd.read_csv(
    r"C:\Users\sachi\OneDrive\Data_science_project\project\data\cleaneddata.csv",
    dtype={"InvoiceNo": str},  # Ensure InvoiceNo is string
    low_memory=False
)

# 📌 MySQL Connection Setup
conn = mysql.connector.connect(
    host="127.0.0.1",
    user="Sachin",
    password="841239",
    database="sales_data"
)
cursor = conn.cursor()

# 📌 Drop Table If Exists
cursor.execute("DROP TABLE IF EXISTS orders")

# 📌 Create Table
create_table_query = """
CREATE TABLE orders (
    InvoiceNo VARCHAR(20),
    StockCode VARCHAR(20),
    Description TEXT,
    Quantity INT,
    UnitPrice DECIMAL(10,2),
    CustomerID DECIMAL(10,0),
    Country VARCHAR(50),
    TotalPrice DECIMAL(12,2),
    Year INT,
    Month INT,
    Day INT,
    Time TIME
);
"""
cursor.execute(create_table_query)

# 📌 Insert Query (Fixing column order)
insert_query = """
INSERT INTO orders (InvoiceNo, StockCode, Description, Quantity, UnitPrice, CustomerID, Country, TotalPrice, Year, Month, Day, Time)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

# ⚡ **Optimized Batch Insert (50,000 rows at a time)**
all_values = [tuple(row) for row in df.itertuples(index=False, name=None)]
batch_size = 50000

for i in range(0, len(all_values), batch_size):
    cursor.executemany(insert_query, all_values[i:i+batch_size])
    conn.commit()  # Save batch to DB
    print(f"✅ Inserted {i+batch_size} rows...")

# 📌 Close Connection
cursor.close()
conn.close()

print("🎉✅ Data Insertion Complete!")
