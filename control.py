from nicegui import ui
import seeed_dht

sensor = seeed_dht.DHT("11", 12)

ui.label('Bathroom Extractor Fan Monitor')
with ui.row():
    tempLabel = ui.label('Temp: ?')
    humidityLabel = ui.label('Humidity: ?')

def refresh():
    humi, temp = sensor.read()
    tempLabel.set_text(f'Temp: {temp}')
    humidityLabel.set_text(f'Humidity: {humi}')

refresh()
ui.timer(5.0, lambda: refresh())

ui.run()