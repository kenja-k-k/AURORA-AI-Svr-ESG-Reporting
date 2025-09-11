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

#For comparision with global 
def get_global_performance(data, variable: str):

        return None                   
