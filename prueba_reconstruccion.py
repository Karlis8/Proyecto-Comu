from fragmentacion import reconstruir

paquetes = [
    {'id':2, 'datos': b'do'},
    {'id':0, 'datos': b'Hola'},
    {'id':1, 'datos': b' mun'},
]

mensaje = reconstruir(paquetes)

print(mensaje)