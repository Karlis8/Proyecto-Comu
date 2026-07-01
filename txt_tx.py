from RF24 import *
import time

radio = RF24(22,0)

radio.begin()
radio.setChannel(76)
radio.setDataRate(RF24_250KBPS)
radio.setPALevel(RF24_PA_LOW)
radio.setAutoAck(True)

direccion = b"TX_01"

radio.openWritingPipe(direccion)
radio.stopListening()

mensaje = b"Hola mundo"

ok = radio.write(
    mensaje
)

print("ACK:", ok)
