-- ==========================================================
-- BIRD SPECIES OBSERVATION ANALYSIS - SQL QUERIES
-- Database Table: Fact_Bird_Observations
-- ==========================================================

-- Query 1: Habitat Comparison (Forest vs Grassland Diversity & Temperature)
SELECT 
    Habitat_Source, 
    COUNT(*) AS Total_Sightings, 
    COUNT(DISTINCT Scientific_Name) AS Unique_Species,
    ROUND(AVG(Temperature), 1) AS Avg_Temperature
FROM Fact_Bird_Observations
GROUP BY Habitat_Source;

-- Query 2: Top 10 Most Observed Bird Species Overall
SELECT 
    Common_Name,
    Scientific_Name,
    COUNT(*) AS Total_Observations,
    COUNT(DISTINCT Admin_Unit_Code) AS Parks_Present
FROM Fact_Bird_Observations
GROUP BY Common_Name, Scientific_Name
ORDER BY Total_Observations DESC
LIMIT 10;

-- Query 3: Partners in Flight (PIF) Watchlist Species (At-Risk Priority)
SELECT 
    Admin_Unit_Code,
    Common_Name,
    Scientific_Name,
    COUNT(*) AS Watchlist_Sightings
FROM Fact_Bird_Observations
WHERE PIF_Watchlist_Status = 1 OR PIF_Watchlist_Status = 'True'
GROUP BY Admin_Unit_Code, Common_Name, Scientific_Name
ORDER BY Watchlist_Sightings DESC;

-- Query 4: Identification Method Breakdown (Acoustic vs Visual)
SELECT 
    ID_Method,
    COUNT(*) AS Total_Sightings,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM Fact_Bird_Observations), 2) AS Percentage_Share
FROM Fact_Bird_Observations
GROUP BY ID_Method
ORDER BY Total_Sightings DESC;

-- Query 5: Annual Observation Trend Across Park Units
SELECT 
    Year,
    COUNT(DISTINCT Admin_Unit_Code) AS Active_Parks,
    COUNT(DISTINCT Observer) AS Active_Observers,
    COUNT(*) AS Total_Observations
FROM Fact_Bird_Observations
GROUP BY Year
ORDER BY Year ASC;