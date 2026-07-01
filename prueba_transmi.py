from RF24 import *
import time

radio = RF24(22, 0)

if not radio.begin():
    print("No se pudo inicializar el NRF24")
    quit()

print("NRF24 detectado")

radio.setChannel(76)
radio.setDataRate(RF24_250KBPS)
radio.setPALevel(RF24_PA_HIGH)

direccion = b"TX_01"

radio.openWritingPipe(direccion)
radio.stopListening()

radio.printPrettyDetails()

print("Comenzando transmisión...")

while True:

    radio.write(
        b"Hola"
    )

    print("ENVIADO")

    time.sleep(1)
