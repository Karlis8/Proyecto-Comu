import subprocess
import os
import time

ARCHIVO = "audio.wav"

print("Grabando...")

resultado = subprocess.run(
    [
        "arecord",
        "-f", "S16_LE",
        "-c", "1",
        "-r", "8000",
        "-d", "5",
        ARCHIVO
    ]
)

print("Código de retorno:", resultado.returncode)

# Esperar un poquito por si el sistema aún está cerrando el archivo
time.sleep(0.5)

if not os.path.exists(ARCHIVO):
    print("ERROR: No se creó audio.wav")
    print("Directorio actual:", os.getcwd())
    print("Archivos en la carpeta:")
    print(os.listdir("."))
else:
    print("audio.wav creado correctamente")
    print("Tamaño:", os.path.getsize(ARCHIVO), "bytes")

    transmitir_archivo(ARCHIVO)
