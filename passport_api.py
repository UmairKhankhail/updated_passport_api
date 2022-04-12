
import uvicorn
from fastapi import FastAPI,UploadFile,File,Request,HTTPException
import re
from io import BytesIO
from passporteye import read_mrz
import uuid
from fastapi.responses import JSONResponse
from country_code import get_country_name
from face_crop import face_detection_crop
from fastapi.middleware.cors import CORSMiddleware
import os

app=FastAPI()

origins = [
    "*",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(ValueError)
async def value_error_exception_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"detail": 'Invalid file uplaoded.'},
    )


@app.exception_handler(ValueError)
async def value_error_exception_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=422,
        content={"detail": 'No file uplaoded.'},
    )
    
def clean_name(name):
    pattern = re.compile('([^\s\w]|_K)+')
    name = pattern.sub('', name)
    return name.strip()


user_info = {}

@app.post('/api/data')
async def data(file:UploadFile=File(...)):
        file.filename = f"{uuid.uuid4()}.png"
        contents = await file.read()  # <-- Important!
        mrz=read_mrz(contents)
        if mrz==None:
            raise HTTPException(status_code=500,detail='Invalid file uploaded.')
        else:
            
            mrz_data=mrz.to_dict()
            user_info['mrz_code']=mrz_data.get('raw_text')
            user_info['mrz_type']=mrz_data.get('mrz_type').upper()
            user_info['surname'] = clean_name(mrz_data.get('surname').upper())
            user_info['name'] = clean_name(mrz_data.get('names').upper())
            user_info['country'] =get_country_name(mrz_data.get('country'))
            if user_info['mrz_type']=='TD3':
                user_info['nationality'] = mrz_data.get('country')
            else:
                user_info['country'] = mrz_data.get('country')
            user_info['pass_number'] = mrz_data.get('number')
            user_info['sex'] = mrz_data.get('sex')
            user_info['date_of_birth']=mrz_data.get('date_of_birth')
            user_info['expiration_date']=mrz_data.get('expiration_date')
            user_info['CNIC_number']=clean_name(mrz_data.get('personal_number'))
            
        
        with open(f"./pictures/{file.filename}", "wb") as f:
            f.write(contents)
            f.close()   
            picture=face_detection_crop(f"./pictures/{file.filename}")
            os.remove(f"./pictures/{file.filename}")
        
        return {"data":user_info,"base64_image":picture}
