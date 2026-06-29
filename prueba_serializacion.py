from protocolo import crear_paquete
from serializacion import (
    serializar,
    deserializar
)

mensaje = crear_paquete(
    0,
    b'Hola'
)

print('Mensaje original')
print(mensaje)

print()

datos = serializar(mensaje)

print('Bytes transmitidos:')
print(datos)

print()

mensaje_recibido = deserializar(datos)

print('Mensaje recuperado:')
print(mensaje_recibido)

print()

print('Cantidad de bytes:')
print(len(datos))