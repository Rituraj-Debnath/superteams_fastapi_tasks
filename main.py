from fastapi import FastAPI, HTTPException
from pathlib import Path
import os

#pathlib is used to work with filesystems
# in pathlib / is path join parameter.
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


## query string endpoint for our filesystem
@app.get("/browse")
def browse(path : str):
    target = (ROOT_DIR / path).resolve()
    if not target.is_relative_to(ROOT_DIR):#the is_relative_to() checks that the target is inside the ROOT folder.
        raise HTTPException(status_code=400, detail="Invalid path")
    if not target.exists():
        raise HTTPException(status_code=404, detail="Path not found")
    # if target.is_dir(): #its very simple too
    #     return os.listdir(target)

    if target.is_dir():
        folder_items = []
        for i in os.scandir(target):
            folder_items.append({
                "name" : i.name,
                "type" : "file" if i.is_file() else "folder",
                "relative_path" : str(Path(path) / i.name)

        })
        return {
            "current_path" : path,
            "contents" : folder_items
        }

    # If file → return metadata
    if target.is_file():
        return {
            "name": target.name,
            "type": "file",
            "relative_path": path
        }



### some learnings ###

# after i test the query param i can see an extra slash \, so basically thats a json form of representation , json store that / or \ character in that way and thats actually means single slash. like root/dir1.

