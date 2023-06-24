from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os

# openai.api_key = os.getenv("OPENAI_API_KEY")
# cors_origin = os.getenv("CORS_ORIGIN")

app = FastAPI()

origins = [
    "https://explorer-assistant-shichisan21.vercel.app",
    "https://explorer-assistant.vercel.app",
    # "http://localhost:5173",
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
