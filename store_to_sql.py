import sqlite3
import pandas as pd

# 1. Read your cleaned CSV
df = pd.read_csv("Cleaned_Combined_Bird_Data.csv")

# 2. Connect to SQLite database (creates 'bird_conservation.db' automatically)
conn = sqlite3.connect("bird_conservation.db")

# 3. Store DataFrame into SQL table
df.to_sql("Fact_Bird_Observations", conn, if_exists="replace", index=False)
print("Successfully loaded 15,368 rows into SQL Table: Fact_Bird_Observations")

# 4. Run verification queries
cursor = conn.cursor()

print("\n--- Summary by Habitat (SQL Query) ---")
query1 = """
SELECT 
    Habitat_Source, 
    COUNT(*) AS Total_Sightings, 
    COUNT(DISTINCT Scientific_Name) AS Unique_Species,
    ROUND(AVG(Temperature), 1) AS Avg_Temp
FROM Fact_Bird_Observations
GROUP BY Habitat_Source;
"""
print(pd.read_sql(query1, conn))

conn.close()