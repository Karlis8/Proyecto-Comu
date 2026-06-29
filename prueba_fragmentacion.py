from fragmentacion import fragmentar

mensaje = b"Hola mundo"

paquetes = fragmentar(mensaje, 4)

for p in paquetes:
    print(p)