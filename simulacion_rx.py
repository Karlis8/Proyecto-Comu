import pickle

from fragmentacion import reconstruir

with open('canal.pkl', 'rb') as archivo:
    canal = pickle.load(archivo)

paquetes = []

for mensaje in canal:

    if mensaje['tipo'] == 'START':

        print('START recibido')
        print(mensaje)
        print()

    elif mensaje['tipo'] == 'DATOS':

        paquetes.append({
            'id': mensaje['id'],
            'datos': mensaje['datos']
        })

    elif mensaje['tipo']  == 'END':

        print('END recibido')
        print()

        #reconstruir los datos
        datos = reconstruir(paquetes)

        #guardar el archivo reconstruido
        with open('datos/mensaje_recibido.txt', 'wb') as archivo:
            archivo.write(datos)

        print('Archivo reconstruido correctamente.')   