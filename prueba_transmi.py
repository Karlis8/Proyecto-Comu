from RF24 import *
import time

print("Creando radio...")

radio = RF24(22, 0)

print("Llamando a begin()...")

if not radio.begin():
    print("No se pudo inicializar el NRF24")
    quit()

print("NRF24 detectado")

radio.setChannel(76)
radio.setDataRate(RF24_1MBPS)
radio.setPALevel(RF24_PA_HIGH)

direccion = b"TX_01"

radio.openWritingPipe(direccion)
radio.stopListening()

radio.printPrettyDetails()

print("Comenzando transmisión...")

while True:

    ok = radio.write(
        b"Hola"
    )

    print("ACK:", ok)

    time.sleep(1)
