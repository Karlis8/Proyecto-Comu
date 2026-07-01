from RF24 import *
import struct
import os
import time

radio = RF24(22, 0)

radio.begin()
radio.setChannel(76)
radio.setDataRate(RF24_250KBPS)
radio.setPALevel(RF24_PA_HIGH)
radio.setAutoAck(True)

direccion = b"TX_01"

radio.openWritingPipe(direccion)
radio.stopListening()

archivo = "audio.wav"

tam = os.path.getsize(archivo)

print("Enviando", tam, "bytes")

cabecera = b"START" + struct.pack("<I", tam)
radio.write(cabecera)

time.sleep(0.1)

with open(archivo, "rb") as f:

    secuencia = 0

    while True:

        datos = f.read(28)

        if not datos:
            break

        paquete = struct.pack("<I", secuencia)
        paquete += datos

        ok = radio.write(paquete)

        if not ok:
            print("Error paquete", secuencia)
        else:
            print("Paquete", secuencia)

        secuencia += 1
        time.sleep(0.005)

radio.write(b"END")

print("Transmisión terminada")
