from fastapi import FastAPI
from presignedURL import presignedURL

app = FastAPI()

@app.get("/get/")
def signedURL(filename: str):
    return presignedURL(filename= filename, mode= 'get_object')



@app.get("/put/")
def signedURL(filename: str):
    return  presignedURL(filename= filename, mode= 'put_object')
