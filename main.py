import time

from fastapi import FastAPI


START_TIME = time.time()

app = FastAPI()


@app.get("/status")
def get_status():
  return {
    'online': True,
    'uptime': round(time.time() - START_TIME, 3)
  }