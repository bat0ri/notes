from fastapi import FastAPI
from pydantic import BaseModel
from uvicorn import run as server


app = FastAPI()


class Status(BaseModel):
    status: str = 'ok'


@app.get('/')
async def status():
    return Status()

if __name__ == "__main__":
    server(app=app, host="0.0.0.0", port=8000)