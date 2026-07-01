from RF24 import *
import struct

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
tam_esperado = 0
bytes_recibidos = 0

print("Esperando archivo...")

while True:

    if radio.available():

        datos = bytes(radio.read(32))
        datos = datos.rstrip(b'\0')

        if datos.startswith(b"START"):

            tam_esperado = struct.unpack(
                "<I",
                datos[5:9]
            )[0]

            print("Tamaño:", tam_esperado)

            archivo = open(
                "audio_recibido.wav",
                "wb"
            )

            bytes_recibidos = 0
            continue

        if datos == b"END":

            if archivo:
                archivo.close()

            print("Archivo completo")
            print(
                "Recibidos:",
                bytes_recibidos
            )

            break

        if archivo:

            numero = struct.unpack(
                "<I",
                datos[:4]
            )[0]

            payload = datos[4:]

            archivo.write(payload)

            bytes_recibidos += len(payload)

            print(
                "Paquete",
                numero
            )
