from paquetes_binarios import *

print('----- START -----')

start_bytes = serializar_start(
    1000,
    35
)

print(start_bytes)
print(deserializar_start(start_bytes))

print()

print('----- DATOS -----')

datos_bytes = serializar_datos(
    5,
    b'Hola'
)

print(datos_bytes)
print(deserializar_datos(datos_bytes))

print()

print('----- END -----')

end_bytes = serializar_end()

print(end_bytes)
print(deserializar_end(end_bytes))