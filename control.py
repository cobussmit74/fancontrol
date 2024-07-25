from nicegui import ui
import seeed_dht
from grove.gpio import GPIO
import time
from apscheduler.schedulers.background import BackgroundScheduler

onswitch = GPIO(5, GPIO.OUT)
offswitch = GPIO(16, GPIO.OUT)

onswitch.write(0)
offswitch.write(0)

def switchFanOn():
    onswitch.write(1)
    time.sleep(1)
    onswitch.write(0)

def switchFanOff():
    offswitch.write(1)
    time.sleep(1)
    offswitch.write(0)

sensor = seeed_dht.DHT("11", 12)
currentHumidity, currentTemperature = sensor.read()

def readSensors():
    global currentHumidity
    global currentTemperature

    humi, temp = sensor.read()
    
    currentHumidity = humi
    currentTemperature = temp

scheduler = BackgroundScheduler()
scheduler.add_job(readSensors, 'interval', seconds=5)
scheduler.start()

ui.label('Bathroom Extractor Fan Monitor')
with ui.row():
    ui.label().bind_text_from(globals(), 'currentTemperature', backward=lambda t: f'Temp: {t}')
    ui.label().bind_text_from(globals(), 'currentHumidity', backward=lambda h: f'Humidity: {h}')
with ui.row():
    ui.button('Fan On', on_click=lambda: switchFanOn())
    ui.button('Fan Off', on_click=lambda: switchFanOff())

ui.run(show=False)
