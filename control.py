from nicegui import ui
import seeed_dht
from grove.gpio import GPIO
import time

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

ui.label('Bathroom Extractor Fan Monitor')
with ui.row():
    tempLabel = ui.label('Temp: ?')
    humidityLabel = ui.label('Humidity: ?')
with ui.row():
    ui.button('Fan On', on_click=lambda: switchFanOn())
    ui.button('Fan Off', on_click=lambda: switchFanOff())

def refresh():
    humi, temp = sensor.read()
    tempLabel.set_text(f'Temp: {temp}')
    humidityLabel.set_text(f'Humidity: {humi}')

refresh()
ui.timer(5.0, lambda: refresh())

ui.run()
