from RF24 import *
import time

radio = RF24(25, 0)

if not radio.begin():
    print("No se pudo inicializar el NRF24")
    quit()

print("NRF24 detectado")

radio.setChannel(76)
radio.setDataRate(RF24_250KBPS)
radio.setPALevel(RF24_PA_HIGH)
radio.setAutoAck(True)

direccion = b"TX_01"

radio.openReadingPipe(1, direccion)
radio.startListening()

print("Esperando mensajes...")

while True:

    if radio.available():

        datos = radio.read(32)

        print("Recibido:")
        print(datos)

    time.sleep(0.01)
