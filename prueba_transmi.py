from RF24 import *
import time

radio = RF24(22, 0)

if not radio.begin():
    print("Error NRF")
    exit()

radio.setChannel(76)
radio.setDataRate(RF24_1MBPS)
radio.setPALevel(RF24_PA_HIGH)

direccion = b"TX_01"

radio.openWritingPipe(direccion)
radio.stopListening()

while True:

    radio.write(
        b"Hola mundo"
    )

    print("Enviado")

    time.sleep(1)
