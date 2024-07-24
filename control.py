from nicegui import ui
import seeed_dht
import grovepi
import time

onswitchPin = 5
offswitchPin = 16

grovepi.pinMode(onswitchPin,"OUTPUT")
grovepi.pinMode(offswitchPin,"OUTPUT")

grovepi.digitalWrite(onswitchPin,0)
grovepi.digitalWrite(offswitchPin,0)

def switchFanOn():
    grovepi.digitalWrite(onswitchPin,1)
    time.sleep(1);
    grovepi.digitalWrite(onswitchPin,0)

def switchFanOff():
    grovepi.digitalWrite(offswitchPin,1)
    time.sleep(1);
    grovepi.digitalWrite(offswitchPin,0)

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
