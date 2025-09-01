import pandas as pd
from typing import Literal

def get_percent_changes(facility_name: str, data, 
            variable: Literal["co2_emitted_tonnes", 
                              "co2_captured_tonnes", 
                              "capture_efficiency_percent"]
                       ): 

    filtered = data[data["facility_name"] == facility_name].dropna(
        subset=[variable].copy()
    )

    filtered["percent_changes"] = filtered[variable].pct_change()*100
    return f"The relative changes for {variable}, for the facility {facility_name} are as follows", filtered["percent_changes"]