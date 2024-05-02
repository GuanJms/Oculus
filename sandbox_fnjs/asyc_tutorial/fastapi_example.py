from fastapi import FastAPI
import time
import datetime
import asyncio

from colorama import init
from colorama import Fore, Back, Style

app = FastAPI()


@app.get("/")
async def root():
    start_time = datetime.datetime.now()
    print(
        Back.GREEN + Fore.WHITE + f"Hello world started at: {start_time} sec.",
        flush=True,
    )
    return {"message": "Hello World"}


