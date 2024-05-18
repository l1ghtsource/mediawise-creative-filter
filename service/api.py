from fastapi import FastAPI, File, UploadFile
from full_pipeline import full_pipeline
import shutil
import os

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


@app.get("/docs")
async def get_docs():
    return {"message": "SwaggerUI можно найти по адресу /docs"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)