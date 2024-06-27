import keyboard
from datetime import datetime
import parameters
import requests
import time
import serial
import csv
import threading
from log_sender import process_csv_and_send_logs

ultima_tecla_tempo = 0
# ser = serial.Serial(parameters.SERIAL_PORT, parameters.SERIAL_BAUDRATE, timeout=5)

time.sleep(2)

csv_filename = 'logs/key_press_log.csv'
backup_filename = 'logs/key_press_log_backup.csv'


def init_csv(filename):
    try:
        with open(filename, mode='x', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['status', 'project', 'additional', 'timePlayed'])
    except FileExistsError:
        pass


init_csv(csv_filename)
init_csv(backup_filename)


def on_left_arrow_press(event):
    current_time = datetime.now().time()
    start_time = datetime.strptime(parameters.START_TIME, "%H:%M").time()
    end_time = datetime.strptime(parameters.END_TIME, "%H:%M").time()

    global ultima_tecla_tempo
    current_datetime = time.time()

    if start_time <= current_time <= end_time:
        if current_datetime - ultima_tecla_tempo >= parameters.DELAY_TO_PRESS:
            # ser.write(b'1')
            save_csv()
            print("tecla apertada")
            ultima_tecla_tempo = current_datetime
    else:
        print("Fora do horário permitido")


def save_csv():
    time_played = datetime.now()
    formatted_time_played = time_played.strftime("%Y-%m-%dT%H:%M:%SZ")

    status = 'botao_pressionado'
    project = parameters.LOG_PROJECT_ID
    additional = ''
    time_played = formatted_time_played

    with open(csv_filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([status, project, additional, time_played])


threading.Thread(target=process_csv_and_send_logs, args=(csv_filename, backup_filename), daemon=True).start()

keyboard.on_press_key("left", on_left_arrow_press)
keyboard.wait("esc")
