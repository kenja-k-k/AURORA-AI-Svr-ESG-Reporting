from fastapi import FastAPI, HTTPException, UploadFile, File, Request
from pydantic import BaseModel
import asyncio
import os
import pandas as pd
from typing import Literal


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
def set_csv():
    global data, file_name, file_path

    if os.path.exists(file_path):
        data = pd.read_csv(file_path)
        return f"{file_name} set as source data."
    else:
        return f"No file labelled {file_name} found on the server. Please check the filename."        

#To upload the data from frontend AND use it as source data
@app.post("/upload_csv")
async def upload_csv(file: UploadFile = File(...)):
    global file_name, file_path, data
     
    #timestamp = datetime.now().astimezone().strftime("%Y-%m-%d_%H-%M-%S_%Z")
    #csv_path = f"./{timestamp}_{file.filename}" #save file to local dir
    file_name = file.filename
    file_path = f"./{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    data = set_csv() #data is now the uploaded csv
    """
    if "anomaly_flag" not in data.columns: #check if the anomaly_flag field even exists
        data["anomaly_flag"] = False
        data.to_csv(csv_path, index=False)
    """
    return {"status": "success", "message": f"Your csv has been uploaded, and saved to {file_path}"}

#Get the facility names
def facility_names():
    global data, names 
    if data.empty:
        return "Set a csv source data first"
    else:
        names = list(set(data["facility_names"]))
        return names 


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


"""
@app.get("/get_esg")
async def get_esg(facility_name: str):
    global data, file_path
"""
    

