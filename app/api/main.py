from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
import pprint
import time
import urllib.error
import urllib.request

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000/generate/",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,   # 追記により追加
    allow_methods=["*"],      # 追記により追加
    allow_headers=["*"]       # 追記により追加
)


def download_file(url, dst_path):
    try:
        # with urllib.request.urlopen("http://www.google.com/s2/favicons?domain="+url) as web_file:
        with urllib.request.urlopen("http://favicon.hatena.ne.jp/?url="+url) as web_file:
            data = web_file.read()
            with open(dst_path, mode='wb') as local_file:
                local_file.write(data)
    except urllib.error.URLError as e:
        print(e)


class Schema(BaseModel):
    url: str

    class Config:
        orm_mode = True


@app.post("/generate/")
def generateQR(req: Schema):
    dst_path = './favicon.png'
    download_file(req.url, dst_path)
    return "succeeded"
