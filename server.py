import io
import json
import uvicorn
import requests
from PIL import Image
from fastapi import FastAPI, Body, UploadFile, File
from pymongo import MongoClient
from pydantic import BaseModel
from bson.json_util import dumps


app = FastAPI()
client = MongoClient("mongodb+srv://isuru:isuru123@cluster0.uiinj08.mongodb.net/?retryWrites=true&w=majority")

#bear token for upload the image to the drive

class AccessToken(BaseModel):
    token:str

AccessToken.token ="ya29.a0Ael9sCPYyCIFIfoaWoFDZiV9cimfLGjH2B8VBTKJ4drKheUdKa7BefI72sPRs38EBsLgAUPzqtRZRek9ts9efCIUpz-4uwE_SQlG3IFln-cDn0SGrCIBbRL0KEO-Kf4XI3rZenbNpjWXkkIjdq0KgxBpabpjaCgYKAagSARASFQF4udJhMTXeNbdXByEDnxbVez2-aQ0163isuru"


headers = {
        "Authorization": "Bearer "+AccessToken.token
}

class Data(BaseModel):
    image_url: str
    date_time: str
    diesease_name: str


@app.post("/cindoc/change/token")
async def updateToken(accessToken: AccessToken):
    ata =accessToken.json()
    #insert data to the db
    map=json.loads(ata)
    headers["Authorization"]="Bearer "+map['token']

    response = {'token updated': headers["Authorization"]}
    return response

@app.get("/ping")
def root():
    return "I am running!"

@app.get("/cindoc/history/all")
def getData():
    db = client.get_database('cinDoc')
    records = db.History
    print(list(records.find()))
    data = records.find()
    json_data = dumps(data)
    return {"data": json.loads(json_data)}

@app.post("/cindoc/history/insert/image")
async def uploadImage(image: UploadFile = File(...)):
    # get image data
    with open(image.filename, "wb") as buffer:
        buffer.write(await image.read())
    im = Image.open(image.filename)
    print(image.filename)
    print(im.format)
    print(headers)

    # upload image

    para = {
        "name": image.filename,
        "parents": ["1NWUBPbsNaBv1n9JOoIUIq4vLWR7RnJTp"]
    }

    files = {
        'data': ('metadata', json.dumps(para), 'application/json;charset=UTF-8'),
        'file':open('./'+image.filename,'rb')

    }
    r = requests.post("https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
        headers=headers,
        files=files
    )

    response = r.json()
    print(response)
    image_url = response['id']
    print(image_url)

    response = {'image_url': "https://drive.google.com/file/d/"+image_url+"/view?usp=share_link"}
    return response


@app.post("/cindoc/history/insert")
async def insertData(data: Data):
    ata =data.json()
    cinDocDB = client.get_database('cinDoc')
    records = cinDocDB.History

    #insert data to the db
    map=json.loads(ata)
    new_record ={
        'image_url': map["image_url"],
        'date_time': map["date_time"],
        'diesease_name': map["diesease_name"]
    }
    records.insert_one(new_record)
    response = {'message': 'Data added successfully'}
    return response

if __name__ == '__main__':
    uvicorn.run(app,port=8081,host='0.0.0.0')