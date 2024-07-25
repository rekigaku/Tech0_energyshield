from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Device(BaseModel):
    device_id: int
    device_name: str
    manufacture: str
    basic_price: float
    symptoms_id: int
    effect_id: int
    device_photo: str

@app.post("/devices/")
def create_device(device: Device):
    return device
