from RF24 import *
import time
import os
import struct

radio = RF24(22, 0)

radio.begin()
radio.setChannel(76)
radio.setDataRate(RF24_250KBPS)
radio.setPALevel(RF24_PA_HIGH)
radio.setAutoAck(True)

direccion = b"TX_01"

radio.openWritingPipe(direccion)
radio.stopListening()

ARCHIVO = "audio.wav"

tamano = os.path.getsize(ARCHIVO)

print("Tamaño:", tamano)

# Paquete START
cabecera = b"START" + struct.pack("<I", tamano)

radio.write(cabecera)
time.sleep(0.1)

with open(ARCHIVO, "rb") as f:

    numero = 0

    while True:

        datos = f.read(28)

        if not datos:
            break

        paquete = struct.pack("<I", numero) + datos

        ok = radio.write(paquete)

        if ok:
            print("Paquete", numero, "OK")
        else:
            print("Paquete", numero, "FALLO")

        numero += 1

        time.sleep(0.005)

radio.write(b"END")

print("Archivo enviado.")
