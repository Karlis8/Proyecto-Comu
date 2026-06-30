from RF24 import *
import time

radio = RF24(17, 0)

if not radio.begin():
    print("Error NRF")
    exit()

radio.setChannel(76)
radio.setDataRate(RF24_1MBPS)
radio.setPALevel(RF24_PA_HIGH)

direccion = b"TX_01"

radio.openReadingPipe(1, direccion)
radio.startListening()

print("Esperando...")

while True:

    if radio.available():

        datos = radio.read(32)

        print(datos)
