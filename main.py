from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pydantic import BaseModel
import openai
import os
import csv
import base64

from routes import talk, calc, csv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
cors_origin = os.getenv("CORS_ORIGIN")

app = FastAPI()

# ルート追加
app.include_router(talk.router)
app.include_router(calc.router)
app.include_router(csv.router)


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


@app.post("/testpost")
def simple_receive(message: Message):
    if message.message is None or message.message == "":
        res = "error!"
    elif "Open AI" in message.message:
        res = "Open AI included!"
    else:
        res = message.message

    return res


@app.post("/message/")
async def get_gpt_response(message: Message):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "あなたは元気な女の子キャラクターとして振舞ってください。"},
            {"role": "user", "content": "最初に「メッセージありがとう！」という一文を付け加えて下さい。"},
            {"role": "user", "content": message.message},
        ],
    )
    return {"message": response['choices'][0]['message']['content']}


@app.get("/")
def get_hello_world():
    return "Hello World"
