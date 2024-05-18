from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from full_pipeline import full_pipeline, table_pipe
import shutil
import os
import pandas as pd
from typing import List
import io

app = FastAPI()

@app.post("/predict/")
async def run_full_pipeline(file: UploadFile = File(...)):
    try:
        with open(file.filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        result = full_pipeline(file.filename)
        
        return {"result": result}
    
    finally:
        os.remove(file.filename)


if not os.path.exists("uploads"):
    os.makedirs("uploads")
if not os.path.exists("outputs"):
    os.makedirs("outputs")

        
@app.post("/predict_table/")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_path = os.path.join("uploads", file.filename)
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())
        
        df = table_pipe(file_path)
        
        output_file_path = os.path.join("outputs", "output.xlsx")
        df.to_excel(output_file_path, index=False)
        
        return FileResponse(output_file_path, filename="output.xlsx")
    except Exception as e:
        return {"error": str(e)}
        
        
@app.get("/docs")
async def get_docs():
    return {"message": "SwaggerUI можно найти по адресу /docs"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="90.156.216.132", port=8000)
