import pandas as pd
from typing import Literal
import numpy as np

#To get facility names___________________
def facility_names(data):
    #global data, names
    if data.empty:
        return "Set a csv source data first"
    else:
        names = list(set(data["facility_name"]))
        return names

#For trends over a period of time
def trends(facility_name: str, data, variable: str):
    # Filter rows for facility and column
    filtered = data[data["facility_name"] == facility_name].dropna(subset=[variable])

    if filtered.empty:
        return "No data to get trends."

    # Use last 5 raw values
    last_5 = filtered[variable].tail(5)

    # Compare first and last
    if last_5.iloc[-1] > last_5.iloc[0]:
        return f"{variable} Rising"
    elif last_5.iloc[-1] < last_5.iloc[0]:
        return f"{variable} Falling!"
    else:
        return f"{variable} Stable"


#For relative percent changes__________
def get_percent_changes(facility_name: str, data, variable: str): 
    """
    if variable not in data.columns:
        raise ValueError(f"Invalid variable. Please check the variable name")
    if facility_name not in facility_names(data):
        raise ValueError(f"Invalid facility name. Please check the facility name")
    """

    filtered = data[data["facility_name"] == facility_name].dropna(subset=[variable]).copy()

    filtered["percent_changes"] = filtered[variable].pct_change()*100
    filtered["percent_changes"] = filtered["percent_changes"].fillna(0)
    changes = filtered[["date", "percent_changes"]]

    return f"The relative changes for {variable}, for the facility {facility_name} are as follows", changes

#For annual statistics
def annual_stats(data: pd.DataFrame, facility_name: str, fallback: bool = True) -> dict:
    
    if data.empty: 
        raise ValueError("The dataset is empty. Please set the CSV data first.")
    
    if facility_name not in data["facility_name"].unique():
        raise ValueError(f"Facility '{facility_name}' not found in the dataset.")
    
    # We will not include outliers, therefore dont need anomalies
    data = data[(data["facility_name"] == facility_name) & (data["anomaly_flag"] == False)].copy()
    
    # Pandas really needs its own datetime dataframe
    data["date"] = pd.to_datetime(data["date"], format="%d/%m/%Y", dayfirst=True, errors="coerce")
    data["year"] = data["date"].dt.year

    current_year = data["year"].max() #Check the latest year, this will not work without datetime format
    target_year = current_year - 1    #Add the last year as target 

    filtered = data[data["year"] == target_year]

    # back to current year if previous year has no data
    if fallback and filtered.empty:
        filtered = data[data["year"] == current_year]

    stats = {
        "Total annual emissions": f"{filtered['co2_emitted_tonnes'].sum()} tonnes",
        "Mean annual emissions": f"{filtered['co2_emitted_tonnes'].mean()} tonnes",
        "Mean efficiency": f"{filtered['capture_efficiency_percent'].mean()} %",
        "Mean storage integrity": f"{filtered['storage_integrity_percent'].mean()} %",
        "Minimum efficiency": f"{filtered['capture_efficiency_percent'].min()} %",
        "Minimum storage integrity": f"{filtered['storage_integrity_percent'].min()} %"
    }

    return stats

#Get stats for a give range of dates.
def stats_by_range(data: pd.DataFrame, facility_name: str, start_date: str, end_date: str):
    """
    Dates for this function must be in dd/mm/yyyy.
    Caution: Pandas dataframe automatically assigns a date pattern, 
    so make sure to align the source formating and this function's format.
    This has caused some issues before.
    """

    if data.empty: 
        raise ValueError("No data found. Set the source CSV data before anything.")

    if facility_name not in data["facility_name"].unique():
        raise ValueError(f"Facility '{facility_name}' not found in the source csv.")

    filtered = data[(data["facility_name"] == facility_name) & (data["anomaly_flag"] == False)].copy() #Dont want anomalies here, so

    
    filtered["date"] = pd.to_datetime(filtered["date"], format="%d/%m/%Y", dayfirst=True, errors="coerce") # Making sure that the dates col is properly formatted

    # Ensure valid start and end date
    """
    Using coerce for error for now, because this is poc.
    Might use different error becavior later on in production
    """
    start_date = pd.to_datetime(start_date, format="%d/%m/%Y", dayfirst=True, errors="coerce")  
    end_date = pd.to_datetime(end_date, format="%d/%m/%Y", dayfirst=True, errors="coerce")

    if pd.isna(start_date) or pd.isna(end_date):
        raise ValueError("Invalid start_date or end_date format or both. Use ther dd/mm/yyyy format.")

    # Filter by date range
    date_filtered = filtered[(filtered["date"] >= start_date) & (filtered["date"] <= end_date)]

    if date_filtered.empty:
        return {"message": f"No data available for {facility_name} between {start_date.date()} and {end_date.date()}"}

    stats = {
        "Date range": f"{start_date.date()} to {end_date.date()}",
        "Total emissions": f"{date_filtered['co2_emitted_tonnes'].sum()} tonnes",
        "Mean emissions": f"{date_filtered['co2_emitted_tonnes'].mean()} tonnes",
        "Mean efficiency": f"{date_filtered['capture_efficiency_percent'].mean()} %",
        "Mean storage integrity": f"{date_filtered['storage_integrity_percent'].mean()} %",
        "Minimum efficiency": f"{date_filtered['capture_efficiency_percent'].min()} %",
        "Minimum storage integrity": f"{date_filtered['storage_integrity_percent'].min()} %"
    }

    return f"The metrics for the {facility_name} facility are as below", stats 

#Add a season column in a df
def add_season(data: pd.DataFrame) -> pd.DataFrame:
    data = data.copy()
    # Ensure 'date' is datetime
    data["date"] = pd.to_datetime(data["date"], format="%d/%m/%Y", dayfirst=True, errors="coerce")
    data["month"] = data["date"].dt.month

    # Map months to seasons
    def month_to_season(month: int) -> str:
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
    return data

#For comparision with global 
def global_bench(data, bench, facility_name: str):
    filtered = data[data["facility_name"] == "facility_name"]
    filtered = add_season(filtered)
    fc_type = filtered["storage_site_type"].drop_duplicates().tolist()
    region = filtered["region"].drop_duplicates().tolist()
    benchmarks = bench[bench["storage_site_type"].isin(fc_type) & bench["region"].isin(region)]
    
    #Will compare the entries to the benchmark and return facilities that underperformed
    return filtered, benchmarks     
