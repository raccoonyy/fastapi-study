from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
  	# allow_origin_regex="https://.*\.example\.org",
    allow_credentials=True,  # 기본값은 False. 
    allow_methods=["*"],  # 기본값이 ['GET']임에 주의!
    allow_headers=["*"],  # 기본값이 []임에 주의! 
)

@app.get("/")
async def main():
    return {"message": "Hello world"}
