import time

from fastapi import FastAPI
from fastapi.responses import FileResponse, RedirectResponse


START_TIME = time.time()

app = FastAPI()


@app.get("/favicon.ico", include_in_schema=False)
def get_favicon():
  return FileResponse('app/favicon.ico')


@app.get("/")
def get_root():
  return RedirectResponse("/status")


@app.get("/status")
def get_status():
  return {
    'online': True,
    'uptime': round(time.time() - START_TIME, 3)
  }