from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import urllib.error
import urllib.request
import re
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup

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


def parse(URL):
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    iconURL = [url.attrs['href'] for url in soup.find_all(
        'link', rel=re.compile('^.*icon.*$', re.IGNORECASE))]
    if not iconURL[0].startswith('http'):
        iconURL[0] = '{uri.scheme}://{uri.netloc}/'.format(
            uri=urlparse(URL)) + iconURL[0]
    print(iconURL)
    return iconURL


def download_file(url, dst_path):
    try:
        with urllib.request.urlopen(url) as web_file, open(dst_path, 'wb') as local_file:
            local_file.write(web_file.read())
    except urllib.error.URLError as e:
        print(e)


class Schema(BaseModel):
    url: str

    class Config:
        orm_mode = True


@app.post("/generate/")
def generateQR(req: Schema):
    dst_path = './favicon.png'
    url_icon = parse(req.url)[0]
    print(url_icon)
    download_file(url_icon, dst_path)
    return "succeeded"
