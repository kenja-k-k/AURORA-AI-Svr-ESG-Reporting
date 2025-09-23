# IMPORTS: Bringing in the tools we need
# -------------------------------

import pandas as pd               # Tool for handling tabular data (spreadsheets, CSVs)
from typing import Literal        # used in type hints to restrict a variable or return value to a fixed set of choices
import numpy as np                # Tool for working with numbers
from datetime import datetime

# -------------------------------------------------------------------------------------
# FUNCTION 1: Get/list facility names
# What it does: Returns a list of unique facility names available in the dataset. Useful to know which facilities can be queried.

def facility_names(data):
    #global data, names
    if data.empty:                                        # STEP 1: If dataset is empty → return warning
        return "Set a csv source data first"
    else:
        names = list(set(data["facility_name"]))          # STEP 2: Collect unique names from the "facility_name" column
        return names                                      # STEP 3: Output = list of facility names

# -------------------------------------------------------------------------------------
# FUNCTION 2: Trend detection
# What it does: Detects short-term trend of a chosen variable (e.g. emissions or efficiency). Uses the last 5 records of that facility.

def trends(facility_name: str, data, variable: str):
    filtered = data[data["facility_name"] == facility_name].dropna(subset=[variable])     # STEP 1: Filter dataset for the requested facility + variable (column)

    if filtered.empty:
        return "No data to get trends."

    last_5 = filtered[variable].tail(5)                          # STEP 2: Take last 5 raw values of the chosen variable

    # Compare first and last
    if last_5.iloc[-1] > last_5.iloc[0]:                         # STEP 3: Compare first vs last value → Rising / Falling / Stable
        return f"{variable} Rising"
    elif last_5.iloc[-1] < last_5.iloc[0]:
        return f"{variable} Falling!"
    else:
        return f"{variable} Stable"


# -------------------------------------------------------------------------------------
# FUNCTION 3: Relative Percent Changes
# What it does: Calculates % change for a chosen variable between consecutive records. Example: "emissions increased by 3% since the last entry".

def get_percent_changes(facility_name: str, data, variable: str): 
    """
    if variable not in data.columns:
        raise ValueError(f"Invalid variable. Please check the variable name")
    if facility_name not in facility_names(data):
        raise ValueError(f"Invalid facility name. Please check the facility name")
    """

    filtered = data[data["facility_name"] == facility_name].dropna(subset=[variable]).copy()     # STEP 1: Filter rows for facility + drop missing values

    filtered["percent_changes"] = filtered[variable].pct_change()*100                            # STEP 2: Calculate percent change from one record to the next
    filtered["percent_changes"] = filtered["percent_changes"].fillna(0)                          # STEP 3: Replace missing changes (first row) with 0
    changes = filtered[["date", "percent_changes"]]                                              # STEP 4: Output = table of dates + percent changes

    return f"The relative changes for {variable}, for the facility {facility_name} are as follows", changes

# -------------------------------------------------------------------------------------
# FUNCTION 4: Annual Statistics (yearly ESG summary)
# What it does: Summarizes annual performance metrics for a facility. Returns totals, means, and minimums for the last year.

def annual_stats(data: pd.DataFrame, facility_name: str, fallback: bool = True) -> dict:
    
    if data.empty:                                                                              # STEP 1: Validate dataset and facility
        raise ValueError("The dataset is empty. Please set the CSV data first.")
    
    if facility_name not in data["facility_name"].unique():
        raise ValueError(f"Facility '{facility_name}' not found in the dataset.")
    
    # We will not include outliers, therefore dont need anomalies
    data = data[(data["facility_name"] == facility_name) & (data["anomaly_flag"] == False)].copy()    # STEP 2: Keep only rows for this facility, excluding anomalies
    
    # Pandas really needs its own datetime dataframe
    data["date"] = pd.to_datetime(data["date"], format="%d/%m/%Y", dayfirst=True, errors="coerce")    # STEP 3: Ensure date column is in proper format + extract year
    data["year"] = data["date"].dt.year

    current_year = data["year"].max()     # STEP 4: Check the latest year, this will not work without datetime format. Pick last full year (target), or fallback to current year
    target_year = current_year - 1    #Add the last year as target 

    filtered = data[data["year"] == target_year]

    # back to current year if previous year has no data
    if fallback and filtered.empty:
        filtered = data[data["year"] == current_year]
    timeNow = datetime.now()
    formattedTime = timeNow.strftime("%Y-%m-%d %H:%M:%S")
    stats = {                                             # STEP 5: Calculate ESG metrics
        "facility_name": facility_name,
        "total_annual_emissions": filtered['co2_emitted_tonnes'].sum(),
        "mean_annual_emissions": filtered['co2_emitted_tonnes'].mean(),
        "mean_capture_efficiency": filtered['capture_efficiency_percent'].mean(),
        "mean_storage_integrity": filtered['storage_integrity_percent'].mean(),
        "minimum_capture_efficiency": filtered['capture_efficiency_percent'].min(),
        "minimum_storage_integrity": filtered['storage_integrity_percent'].min(),
        "total_captured_tonnes": filtered['co2_captured_tonnes'].sum(),
        "total_stored_tonnes": filtered['co2_stored_tonnes'].sum(),
        "date_time": formattedTime,
    }

    return stats                                          # STEP 6: Output = ESG summary dictionary

# -------------------------------------------------------------------------------------
# FUNCTION 5: Stats by Custom Date Range
# What it does: Calculates ESG metrics/stats for a custom range of dates.

def stats_by_range(data: pd.DataFrame, facility_name: str, start_date: str, end_date: str):
    """
    Dates for this function must be in dd/mm/yyyy.
    Caution: Pandas dataframe automatically assigns a date pattern, 
    so make sure to align the source formating and this function's format.
    This has caused some issues before.
    """

    if data.empty:                                                                             # STEP 1: Validate dataset + facility
        raise ValueError("No data found. Set the source CSV data before anything.")

    if facility_name not in data["facility_name"].unique():
        raise ValueError(f"Facility '{facility_name}' not found in the source csv.")

    filtered = data[(data["facility_name"] == facility_name) & (data["anomaly_flag"] == False)].copy() # STEP 2: Filter rows for facility, excluding anomalies
    
    filtered["date"] = pd.to_datetime(filtered["date"], format="%d/%m/%Y", dayfirst=True, errors="coerce") # Making sure that the dates col is properly formatted

    # Ensure valid start and end date
    """
    Using coerce for error for now, because this is poc.
    Might use different error becavior later on in production
    """
    start_date = pd.to_datetime(start_date, format="%d/%m/%Y", dayfirst=True, errors="coerce")      # STEP 3: Convert start/end dates to datetime
    end_date = pd.to_datetime(end_date, format="%d/%m/%Y", dayfirst=True, errors="coerce")

    if pd.isna(start_date) or pd.isna(end_date):
        raise ValueError("Invalid start_date or end_date format or both. Use ther dd/mm/yyyy format.")

    date_filtered = filtered[(filtered["date"] >= start_date) & (filtered["date"] <= end_date)]     # STEP 4: Filter dataset for that range

    if date_filtered.empty:
        return {"message": f"No data available for {facility_name} between {start_date.date()} and {end_date.date()}"}

    stats = {                                                                                       # STEP 5: Calculate metrics
        "Date range": f"{start_date.date()} to {end_date.date()}",
        "Total emissions": f"{date_filtered['co2_emitted_tonnes'].sum()} tonnes",
        "Mean emissions": f"{date_filtered['co2_emitted_tonnes'].mean()} tonnes",
        "Mean efficiency": f"{date_filtered['capture_efficiency_percent'].mean()} %",
        "Mean storage integrity": f"{date_filtered['storage_integrity_percent'].mean()} %",
        "Minimum efficiency": f"{date_filtered['capture_efficiency_percent'].min()} %",
        "Minimum storage integrity": f"{date_filtered['storage_integrity_percent'].min()} %"
    }

    return f"The metrics for the {facility_name} facility are as below", stats                     # STEP 6: Output = text + metrics dictionary

# -------------------------------------------------------------------------------------
# FUNCTION 6: Add Season Column
# What it does: Add a "season" column in a df based on month of the year. Example: Jan = Winter, Jul = Summer.

def add_season(data: pd.DataFrame) -> pd.DataFrame:
    data = data.copy()                                        # STEP 1: Copy dataset + ensure date is datetime
    # Ensure 'date' is datetime
    data["date"] = pd.to_datetime(data["date"], format="%d/%m/%Y", dayfirst=True, errors="coerce")
    data["month"] = data["date"].dt.month

    def month_to_season(month: int) -> str:                   # STEP 2: Map month → season
        if month in [12, 1, 2]:
            return "Winter"
        elif month in [3, 4]:
            return "Spring"
        elif month in [5, 6, 7, 8, 9]:
            return "Summer"
        elif month in [10, 11]:
            return "Autumn"
        else:
            return None  # in case of missing or invalid dates

    data["season"] = data["month"].apply(month_to_season)
    return data                                                      # STEP 3: Output = enriched dataset with new "season" column

# -------------------------------------------------------------------------------------
# FUNCTION 7: Compare with Global Benchmarks
# What it does: Compares facility performance with global benchmark values. Benchmarks are filtered by facility’s type and region.

def global_bench(data, bench, facility_name: str):
    filtered = data[data["facility_name"] == "facility_name"]        # STEP 1: Filter facility data
    filtered = add_season(filtered)
    fc_type = filtered["storage_site_type"].drop_duplicates().tolist()         # STEP 2: Extract facility attributes
    region = filtered["region"].drop_duplicates().tolist()
    benchmarks = bench[bench["storage_site_type"].isin(fc_type) & bench["region"].isin(region)]           # STEP 3: Filter global benchmarks by facility type + region
    
    #Will compare the entries to the benchmark and return facilities that underperformed
    return filtered, benchmarks                                                              # STEP 4: Output = (facility dataset with season, benchmark subset)
