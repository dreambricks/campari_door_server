import keyboard
from datetime import datetime
import parameters
import requests
import time
import serial

ultima_tecla_tempo = 0
# ser = serial.Serial(parameters.SERIAL_PORT, parameters.SERIAL_BAUDRATE, timeout=5)

time.sleep(2)


def on_left_arrow_press(event):
    current_time = datetime.now().time()
    start_time = datetime.strptime(parameters.START_TIME, "%H:%M").time()
    end_time = datetime.strptime(parameters.END_TIME, "%H:%M").time()

    global ultima_tecla_tempo
    current_datetime = time.time()

    if start_time <= current_time <= end_time:
        if current_datetime - ultima_tecla_tempo >= parameters.DELAY_TO_PRESS:
            # ser.write(b'1')
            send_log()
            print("tecla apertada")
            ultima_tecla_tempo = current_datetime
    else:
        print("Fora do horário permitido")


def send_log():
    url = parameters.LOG_API + "/datalog/upload"

    time_played = datetime.now()
    formatted_time_played = time_played.strftime("%Y-%m-%dT%H:%M:%SZ")

    data = {
        'status': 'botao_pressionado',
        'project': parameters.LOG_PROJECT_ID,
        'additional': '',
        'timePlayed': formatted_time_played  # 2024-06-26T14:30:00Z
    }

    response = requests.post(url, data=data)

    if response.status_code == 200:
        print('Requisição bem-sucedida')
    else:
        print('Falha na requisição:', response.status_code)


keyboard.on_press_key("left", on_left_arrow_press)
keyboard.wait("esc")
