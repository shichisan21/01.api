from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pydantic import BaseModel
import openai
import os
import csv
import base64

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
cors_origin = os.getenv("CORS_ORIGIN")

app = FastAPI()

origins = [
    "https://explorer-assistant-shichisan21.vercel.app",
    "https://explorer-assistant.vercel.app",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Message(BaseModel):
    message: str


class CSVData(BaseModel):
    csvData: str


@app.get("/")
def Hello():
    return {"Hello": "World!"}


@app.post("/message/")
async def get_gpt_response(message: Message):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message.message},
        ],
    )
    return {"message": response['choices'][0]['message']['content']}


@app.post("/upload-csv/")
async def process_csv(data: CSVData):

    base64_data = data.csvData
    decoded_bytes = base64.b64decode(base64_data)
    decoded_content = decoded_bytes.decode("utf-8")
    csv_data = csv.reader(decoded_content.splitlines(), delimiter=",")

    # CSVデータの処理を行う
    # ここでは例として、各行の内容を表示するだけとします
    for row in csv_data:
        print(row)

    return {"message": "CSV file received and processed successfully"}
