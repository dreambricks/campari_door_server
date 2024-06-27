import csv
import time
import requests
import parameters


def send_log(status, project, additional, time_played):
    url = parameters.LOG_API + "/datalog/upload"
    data = {
        'status': status,
        'project': project,
        'additional': additional,
        'timePlayed': time_played
    }

    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            print('Requisição bem-sucedida')
            return True
        else:
            print('Falha na requisição:', response.status_code)
            return False
    except requests.exceptions.ConnectionError:
        print('Falha na conexão: Não foi possível conectar ao servidor')
        return False


def process_csv_and_send_logs(csv_filename, backup_filename):
    while True:
        rows_to_keep = []
        rows_to_backup = []

        with open(csv_filename, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                success = send_log(row['status'], row['project'], row['additional'], row['timePlayed'])
                if success:
                    rows_to_backup.append(row)
                else:
                    rows_to_keep.append(row)

        with open(csv_filename, mode='w', newline='') as file:
            fieldnames = ['status', 'project', 'additional', 'timePlayed']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows_to_keep)

        with open(backup_filename, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writerows(rows_to_backup)

        time.sleep(10)
