from paquetes_binarios import *

start = serializar_start(
    1000,
    35
)

datos = serializar_datos(
    5,
    b'A'*29
)

end = serializar_end()

print('START:')
print(start)
print(len(start))

print()

print('DATOS:')
print(datos)
print(len(datos))

print()

print('END:')
print(end)
print(len(end))
