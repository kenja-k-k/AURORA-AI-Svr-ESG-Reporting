from fastapi import FastAPI, HTTPException, UploadFile, File, Request
from pydantic import BaseModel
import asyncio
import os
import pandas as pd

# Expected format for requests___________________________
class GlobalInput(BaseModel):
    date                        : str
    facility_id                 : str
    facility_name               : str
    country                     : str
    region                      : str
    storage_site_type           : str
    co2_emitted_tonnes          : float | None = None
    co2_captured_tonnes         : float | None = None
    co2_stored_tonnes           : float | None = None
    capture_efficiency_percent  : float | None = None
    storage_integrity_percent   : float | None = None
    #anomaly_flag                :
#___________________________

#To set a csv as data___________________
def set_csv(csv_name: str):
    global data, file_path
    file_path = fr".\{csv_name}"

    if os.path.exists:
        global data = pd.read_csv(file_path)
        return f"{csv_name} set as source data."
    else:
        return f"No file labelled {csv_name} found on the server. 
                 Please check the filename."        
    

#Train the model, IF needed___________________
@app.get("/train_model")
async def train_model(lr:float = 0.01, depth:int = 5, verbosity: -1|1|0 = -1): #verbose is really nor needed, but use it if you dev
    parameters = {
        "objective"     : "regression",
        "metric"        : "rmse",
        "learning_rate" : lr,
        "boosting_type" : "gbdt",
        "num_leaves"    : (2**depth)-1,
        "verbosity"     : verbosity
    }

@app.get("/get_esg")
async def get_esg(facility_name: str):
    global data, file_path

    

