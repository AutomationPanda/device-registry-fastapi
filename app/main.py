import time

from fastapi import FastAPI
from starlette.responses import RedirectResponse


START_TIME = time.time()

app = FastAPI()


@app.get("/")
def get_root():
  return RedirectResponse("/status")


@app.get("/status")
def get_status():
  return {
    'online': True,
    'uptime': round(time.time() - START_TIME, 3)
  }