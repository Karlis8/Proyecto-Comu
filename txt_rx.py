from RF24 import *
import time

radio = RF24(25,0)

radio.begin()
radio.setChannel(76)
radio.setDataRate(RF24_250KBPS)
radio.setPALevel(RF24_PA_LOW)
radio.setAutoAck(True)

direccion = b"TX_01"

radio.openReadingPipe(1, direccion)
radio.startListening()

print("Esperando...")

while True:

    if radio.available():

        datos = radio.read(32)

        datos = bytes(datos)

        datos = datos.rstrip(
            b'\0'
        )

        print(
            datos.decode()
        )
