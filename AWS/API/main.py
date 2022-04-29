import os
from fastapi import FastAPI, UploadFile, File
from presignedURL import presignedURL
from feedback import feedback


app = FastAPI()

@app.get("/get/")
def signedURL(filename: str):
    return presignedURL(filename=filename, mode='get_object')


@app.get("/feedback/")
def feedback(filename: str):
    return feedback(filename=filename)
    

@app.post("/uploadfile")
async def create_upload_file(data: UploadFile = File(...)):
    print(data.filename)

    file_location = f"files/{data.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(data.file.read())

    os.system(f'sudo aws s3 cp {file_location} s3://handboll-ai-coach/videos/{data.filename}')
    os.system(f'rm {file_location}')

    return {"Filename": data.filename}