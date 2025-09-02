import pandas as pd
from typing import Literal

#To get facility names___________________
def facility_names(data):
    #global data, names
    if data.empty:
        return "Set a csv source data first"
    else:
        names = list(set(data["facility_name"]))
        return names


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
