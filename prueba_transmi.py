from RF24 import *
from gpiozero import Button
import subprocess
import struct
import os
import time

BOTON = 27
ARCHIVO = "audio.wav"

boton = Button(BOTON)

radio = RF24(22, 0)

radio.begin()
radio.setChannel(76)
radio.setDataRate(RF24_250KBPS)
radio.setPALevel(RF24_PA_HIGH)
radio.setAutoAck(True)

direccion = b"TX_01"

radio.openWritingPipe(direccion)
radio.stopListening()


def transmitir_archivo(nombre):

    tam = os.path.getsize(nombre)

    print("Enviando", tam, "bytes")

    cabecera = b"START" + struct.pack("<I", tam)
    radio.write(cabecera)

    time.sleep(0.1)

    with open(nombre, "rb") as f:

        secuencia = 0

        while True:

            datos = f.read(27)

            if not datos:
                break

            paquete = struct.pack(
                "<IB",
                secuencia,
                len(datos)
            )

            paquete += datos

            ok = radio.write(paquete)

            if not ok:
                print("Error paquete", secuencia)

            secuencia += 1
            time.sleep(0.005)

    radio.write(b"END")

    print("Transmisión terminada")


print("Esperando botón...")

while True:

    boton.wait_for_press()

    print("Grabando...")

    subprocess.run([
        "arecord",
        "-f", "S16_LE",
        "-c", "1",
        "-r", "8000",
        "-d", "5",
        ARCHIVO
    ])

    print("Audio grabado")

    transmitir_archivo(ARCHIVO)

    print("Listo\n")

    time.sleep(1)
