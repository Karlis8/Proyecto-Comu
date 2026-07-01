from RF24 import *
import struct
import subprocess

radio = RF24(25, 0)

radio.begin()
radio.setChannel(76)
radio.setDataRate(RF24_250KBPS)
radio.setPALevel(RF24_PA_HIGH)
radio.setAutoAck(True)

direccion = b"TX_01"

radio.openReadingPipe(1, direccion)
radio.startListening()

archivo = None

print("Esperando audio...")

while True:

    if radio.available():

        datos = bytes(radio.read(32))

        if datos.startswith(b"START"):

            tam = struct.unpack(
                "<I",
                datos[5:9]
            )[0]

            print("Recibiendo", tam, "bytes")

            archivo = open(
                "audio_recibido.wav",
                "wb"
            )

            continue

        if datos[:3] == b"END":

            if archivo:
                archivo.close()

            print("Audio recibido")

            subprocess.run([
                "aplay",
                "audio_recibido.wav"
            ])

            print("Reproducción terminada")

            continue

        if archivo:

            if len(datos) < 5:
                continue

            secuencia, longitud = struct.unpack(
                "<IB",
                datos[:5]
            )

            payload = datos[5:5+longitud]

            archivo.write(payload)
