import os
import sys
import ctypes
import time


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def run_as_admin():
    if sys.version_info[0] == 3 and sys.version_info[1] >= 5:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)


def stop_spooler_service():
    os.system("net stop spooler")


def start_spooler_service():
    os.system("net start spooler")


def clear_print_queue():
    spool_directory = r"C:\Windows\System32\spool\PRINTERS"
    try:
        for file_name in os.listdir(spool_directory):
            file_path = os.path.join(spool_directory, file_name)
            os.remove(file_path)
    except Exception as e:
        print(f"Erro ao limpar a fila de impressão: {e}")


def main():
    # Parar o serviço de spooler de impressão
    stop_spooler_service()
    time.sleep(2)  # Aguardar um pouco para garantir que o serviço parou

    # Limpar a fila de impressão
    clear_print_queue()

    # Reiniciar o serviço de spooler de impressão
    start_spooler_service()
    time.sleep(2)  # Aguardar um pouco para garantir que o serviço iniciou

    print("Fila de impressão limpa com sucesso!")


def run_main():
    if is_admin():
        main()
    else:
        print("Solicitando privilégios de administrador...")
        run_as_admin()


if __name__ == "__main__":
    run_main()
