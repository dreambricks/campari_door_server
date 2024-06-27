import subprocess


def execute_ps1(script_path):
    try:
        # Executa o script PowerShell
        result = subprocess.run(["powershell", "-ExecutionPolicy", "Unrestricted", "-File", script_path],
                                capture_output=True, text=True, check=True)
        return {"stdout": result.stdout, "stderr": result.stderr}
    except subprocess.CalledProcessError as e:
        # Retorna a saída e o erro se a execução falhar
        return {"stdout": e.stdout, "stderr": e.stderr}


# Exemplo de uso
if __name__ == "__main__":
    script_path = "caminho/para/seu/script.ps1"
    output = execute_ps1(script_path)
    print("Saída:")
    print(output["stdout"])
    print("Erro:")
    print(output["stderr"])
