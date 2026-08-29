import pandas as pd

forest_file = "Bird_Monitoring_Data_FOREST.XLSX"
grassland_file = "Bird_Monitoring_Data_GRASSLAND.XLSX"

print("1/3 Loading and merging all 11 Forest sheets...")
xls_f = pd.ExcelFile(forest_file)
forest_dfs = [pd.read_excel(xls_f, sheet_name=s).assign(Habitat_Source="Forest") for s in xls_f.sheet_names]
df_forest = pd.concat(forest_dfs, ignore_index=True)

print("2/3 Loading and merging all 11 Grassland sheets...")
xls_g = pd.ExcelFile(grassland_file)
grass_dfs = [pd.read_excel(xls_g, sheet_name=s).assign(Habitat_Source="Grassland") for s in xls_g.sheet_names]
df_grass = pd.concat(grass_dfs, ignore_index=True)

# Standardize column naming
df_forest = df_forest.rename(columns={"NPSTaxonCode": "Taxon_Code"})
df_grass = df_grass.rename(columns={"TaxonCode": "Taxon_Code"})

# Combine
df = pd.concat([df_forest, df_grass], ignore_index=True)

# Clean text whitespace and nulls
text_cols = ["Admin_Unit_Code", "Sub_Unit_Code", "Plot_Name", "Location_Type", "Observer", 
             "ID_Method", "Distance", "Sex", "Common_Name", "Scientific_Name", "AOU_Code"]
for c in text_cols:
    if c in df.columns:
        df[c] = df[c].fillna("Undetermined").astype(str).str.strip()

# Standardize booleans
for b in ["PIF_Watchlist_Status", "Regional_Stewardship_Status", "Flyover_Observed"]:
    if b in df.columns:
        df[b] = df[b].apply(lambda x: True if str(x).strip().upper() in ["TRUE", "1", "YES", "Y", "1.0"] else False)

# Clean numeric & dates
df["Temperature"] = pd.to_numeric(df["Temperature"], errors="coerce")
df["Humidity"] = pd.to_numeric(df["Humidity"], errors="coerce")
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df["Year"] = pd.to_numeric(df["Year"], errors="coerce").fillna(df["Date"].dt.year).astype(int)

# Remove exact duplicates
df_clean = df.drop_duplicates().reset_index(drop=True)

print("3/3 Saving master dataset to your folder...")
df_clean.to_excel("Cleaned_Combined_Bird_Data.xlsx", index=False)
df_clean.to_csv("Cleaned_Combined_Bird_Data.csv", index=False)

print(f"Done! Created 'Cleaned_Combined_Bird_Data.xlsx' with {len(df_clean):,} clean rows!")