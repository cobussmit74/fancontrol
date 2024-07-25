from nicegui import ui
import seeed_dht
from grove.gpio import GPIO
import time as sleeptime
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler

onswitch = GPIO(5, GPIO.OUT)
offswitch = GPIO(16, GPIO.OUT)

fanRunTime=1
fanIsOn = False
fanOffTime = datetime.now()

def switchFanOn():
    global fanIsOn
    global fanOffTime

    onswitch.write(1)
    sleeptime.sleep(1)
    onswitch.write(0)

    fanIsOn = True

def switchFanOff():
    global fanIsOn

    offswitch.write(1)
    sleeptime.sleep(1)
    offswitch.write(0)

    fanIsOn = False

def increaseFanRunTime():
    global fanOffTime
    fanOffTime = datetime.now() + timedelta(minutes=fanRunTime)

def userSwtichFanOn():
    increaseFanRunTime()
    switchFanOn()

sensor = seeed_dht.DHT("11", 12)
currentHumidity, currentTemperature = sensor.read()

def readSensors():
    global currentHumidity
    global currentTemperature

    humi, temp = sensor.read()

    if humi < currentHumidity or humi > currentHumidity:
        increaseFanRunTime()

    currentHumidity = humi
    currentTemperature = temp

    if not fanIsOn and fanOffTime > datetime.now():
        switchFanOn()

    if fanIsOn and fanOffTime < datetime.now():
        switchFanOff()

scheduler = BackgroundScheduler()
scheduler.add_job(readSensors, 'interval', seconds=10)
scheduler.start()

ui.label('Bathroom Extractor Fan Monitor')
with ui.row():
    ui.label().bind_text_from(globals(), 'currentTemperature', backward=lambda t: f'Temp: {t}')
    ui.label().bind_text_from(globals(), 'currentHumidity', backward=lambda h: f'Humidity: {h}')
with ui.row():
    ui.button('Fan On', on_click=lambda: userSwtichFanOn())
    ui.button('Fan Off', on_click=lambda: switchFanOff())
with ui.row():
    ui.label().bind_text_from(globals(), 'fanIsOn', backward=lambda on: 'Fan is ON' if on else 'Fan is OFF')
    countdownLabel = ui.label('')

def refreshCountdownLabel():
    newText = ''
    if fanIsOn and fanOffTime > datetime.now():
       timeDiff = fanOffTime - datetime.now()
       newText = f'for {timeDiff}';
    
    countdownLabel.set_text(newText);

ui.timer(1.0, lambda: refreshCountdownLabel())

ui.run(show=False)
