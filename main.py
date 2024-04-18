from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import datetime
import random
import google_gemini_work


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
  
@app.post("/image_prompt")
async def image_prompt(file: UploadFile = File(...)):
    # Generating a unique filename with current time and a random number
    current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    random_number = random.randint(1000, 9999)
    filename = f"{current_time}_{random_number}_{file.filename}"

    # Save the file
    file_path = f"./saved_images/{filename}"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "wb+") as file_object:
        file_object.write(await file.read())
    
    # Return the name of the saved file
    return google_gemini_work.get_gemini_response("Get the coupon code from the image in a json format with key coupon_code","saved_images\\"+filename)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
