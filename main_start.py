import time
import subprocess

def rodar():
    caminho = '/home/maeda/choque-termico/main.py'
    tempo_espera = 2

    time.sleep(tempo_espera)

    subprocess.run(['python', caminho])

rodar()