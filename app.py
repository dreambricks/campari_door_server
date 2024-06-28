import keyboard
from datetime import datetime
import parameters
import time
import threading
from log_sender import process_csv_and_send_logs, init_csv, csv_filename, backup_filename, save_csv
import print_script

ultima_tecla_tempo = 0
# ser = serial.Serial(parameters.SERIAL_PORT, parameters.SERIAL_BAUDRATE, timeout=5)

time.sleep(2)


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
            print_script.execute_ps1('runprint.ps1')
            save_csv()
            print("tecla apertada")
            ultima_tecla_tempo = current_datetime
    else:
        print("Fora do horário permitido")


threading.Thread(target=process_csv_and_send_logs, args=(csv_filename, backup_filename), daemon=True).start()

keyboard.on_press_key("left", on_left_arrow_press)
keyboard.wait("esc")
