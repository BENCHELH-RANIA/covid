
from fastapi.responses import JSONResponse
import numpy as np
import json
import uvicorn
import pandas as pd
from fastapi import FastAPI, HTTPException

app = FastAPI()


def load_data():
    covid=pd.read_csv("data.csv")
    covid["Date"]=pd.to_datetime(covid["Date"],format="%d-%m-%Y")
    latest=covid[covid["Date"] == "2020-11-30"][["Country","Confirmed","Recovered","Deaths","Active"]]
    return covid,latest
covid= load_data()

@app.get("/get_data", response_model=None)
async  def get_data():
    try:
        data =load_data()

        # Convert DataFrame to a list of dictionaries
        data_dict_list = json.loads(data.to_json(orient="records", default_handler=str))

        return JSONResponse(content=data_dict_list, status_code=200)
    except Exception as e:
        # Handle exceptions appropriately, e.g., returning an HTTP error response
        return JSONResponse(content={"error": str(e)}, status_code=500)