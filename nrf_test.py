from RF24 import *

print("creando radio...")
radio = RF24(22, 0)

print("Llamando a begin()...")
resultado = radio.begin()

print("Resultado:", resultado)

if resultado:
    print("NRF24 detectado correctamente")