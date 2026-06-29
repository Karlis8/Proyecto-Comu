from protocolo import (
    crear_start,
    crear_paquete,
    crear_end
)

start = crear_start(
    tamano_archivo=10,
    cantidad_paquetes=3,
)

print(start)

print()

print(crear_paquete(0, b'Hola'))
print(crear_paquete(1, b' mun'))
print(crear_paquete(2, b'do'))

print()

print(crear_end())