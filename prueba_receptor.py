from RF24 import *
import time

print("Creando radio...")

radio = RF24(17, 0)

print("Llamando a begin()...")

if not radio.begin():
    print("No se pudo inicializar el NRF24")
    quit()

print("NRF24 detectado")

radio.setChannel(76)
radio.setDataRate(RF24_1MBPS)
radio.setPALevel(RF24_PA_HIGH)

direccion = b"TX_01"

radio.openReadingPipe(1, direccion)
radio.startListening()

print("Listening:", radio.isListening())
print("Esperando mensajes...")

radio.printPrettyDetails()

while True:

    if radio.available():

        datos = radio.read(32)

        print("Recibido:")
        print(datos)

    time.sleep(0.01)
