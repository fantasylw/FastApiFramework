import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router import routers

from fastapi import FastAPI
from mongoengine import connect

from utils.logger import AppLogger


connect('case',host = '127.0.0.1:5000') # 连接数据库

log = AppLogger("main.log").get_logger()

app = FastAPI()


origins = [
    "http://localhost",
    "http://localhost:9528",
    "http://localhost:9530", "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


for item in routers.data:
    app.include_router(item[0], prefix=item[1], tags=item[2])




if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888, forwarded_allow_ips='*')
