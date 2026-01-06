from fastapi import FastAPI, HTTPException
from pathlib import Path
import os

app = FastAPI()

#setting the base folder of the NAS and resolve is creating it as absolute path
ROOT_DIR=Path("root-data").resolve()

@app.get("/")
def list_root():
    if not ROOT_DIR.exists():
        raise HTTPException(status_code=404, detail="Root folder not found")
    # else:  #it will be very minimal , only lists things.
    #     return os.listdir(ROOT_DIR) 
    item = []
    for i in os.scandir(ROOT_DIR):
        item.append({"name": i.name , "type": "folder" if i.is_dir() else "file"})

    return {
        "path" : "root-data",
        "Contents" : item
    }


