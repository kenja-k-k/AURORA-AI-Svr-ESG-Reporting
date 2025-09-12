from fastapi import FastAPI, HTTPException, UploadFile, File, Query
from fastapi import Request
from fastapi.responses import StreamingResponse
import asyncio
from pydantic import BaseModel
import pandas as pd
import os
import base64
from io import BytesIO
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone, timedelta
from typing import Literal, Optional

#Refactor from modules
from insights import get_percent_changes, trends, global_bench, annual_stats, stats_by_range
#from rag import RAGPipeline


app = FastAPI()
#rag = RAGPipeline()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



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


data = pd.DataFrame()
csv_path = None


#To set a csv as data___________________
def set_csv():
    global data, file_name, file_path

    if file_path is None or not os.path.exists(file_path):
        raise FileNotFoundError(f"No file named {file_name}.csv found on the server. Please check the filename.")
    
    data = pd.read_csv(file_path)
    return f"{file_name} set as source data."        

#Use an existing csv as data___________________
@app.post("/use_csv")
def use_csv(name: str):
    global file_name, file_path

    file_name = name
    file_path = f"./{file_name}.csv"

    try:
        msg = set_csv()
        return {"status": "success", "message": msg}
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

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

    set_csv() #data is now the uploaded csv
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
async def train_model(lr:float = 0.01, depth:int = 5, verbosity= -1): #verbose is really nor needed, but use it if you dev
    parameters = {
        "objective"     : "regression",
        "metric"        : "rmse",
        "learning_rate" : lr,
        "boosting_type" : "gbdt",
        "num_leaves"    : (2**depth)-1,
        "verbosity"     : verbosity
    }

 
#ESG insights for the data. This can use a number of metrics______________________
@app.get("/get_esg")
async def get_esg(facility_name: Literal["Alpha CCS Plant", 
                                         "Beta Capture Hub", 
                                         "Delta Storage", 
                                         "Epsilon Capture"],

                  report_type: Literal["Percent changes", 
                                       "Relative performance to global"],

                  variable: Literal["co2_emitted_tonnes", 
                                    "co2_captured_tonnes", 
                                    "capture_efficiency_percent"]
                  ):

    global data, file_path

    match report_type:
          case "Percent changes":
              return get_percent_changes(facility_name, data, variable)

          case "Relative performance to global":
              return get_global_performance(facility_name, data, variable)   

                            
#Get trends for the data. This can use a number of metrics______________________
@app.get("/get_trend")
async def get_trends(facility_name: Literal["Alpha CCS Plant", 
                                          "Beta Capture Hub", 
                                          "Delta Storage", 
                                          "Epsilon Capture"],

                   variable: Literal["co2_emitted_tonnes", 
                                     "co2_captured_tonnes", 
                                     "capture_efficiency_percent"]
                  ):

    global data, file_path
    
    report_type ="Percent changes"
    
    return trends(facility_name, data, variable)


#Get annual metrics for a facility_______________
"""

@app.get("/get_annual_stats")
def get_annual_stats(facility_name:str):
    global data, file_path

    return annual_stats(data, facility_name)
"""


#Get stats for a given period______________
@app.get("/get_stats_by_range")
async def get_stats_by_range(
                        facility_name: str,
                        start_date: Optional[str] = Query(None, description="Optional, but must be in dd/mm/yyyy"),
                        end_date: Optional[str] = Query(None, description="Optional, but must be in dd/mm/yyyy"),
                        annual: bool = True
                      ):
    global data, file_path

    if annual or (not start_date and not end_date):
        return annual_stats(data, facility_name) #Return this, if the annual flag is on
    else:
        return stats_by_range(data, facility_name, start_date, end_date)
    


"""


rag = RAGPipeline(
    embedding_model_name="sentence-transformers/all-MiniLM-L6-v2",
    llm_model_name="microsoft/phi-3-mini-128k-instruct",
    db_path="./chroma_db",
    device="cpu"  # change to "cuda" if you have GPU
)


@app.get("/get_text_query")
def get_text_query(query: str = Query(..., description="User question")):
   
    if not query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    try:
        answer = rag.answer_question(query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating answer: {str(e)}")

    return {"query": query, "answer": answer}
"""
