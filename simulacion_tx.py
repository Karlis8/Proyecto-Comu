import pickle
from fragmentacion import fragmentar
from protocolo import (
    crear_start,
    crear_paquete,
    crear_end
)

#abrir el archivo de prueba 
with open('datos/mensaje.txt','rb') as archivo:
    datos = archivo.read()

#fragmentar el archivo
tamano_paquete = 8
fragmentos = fragmentar(datos, tamano_paquete)

#crear paquete start
start = crear_start(
    tamano_archivo=len(datos),
    cantidad_paquetes=len(fragmentos)
)

print('------ START ------')
print(start)

print('\n------ DATOS ------')

#crear paquetes DATOS
paquetes = []

canal =[]

canal.append(start)

for fragmento in fragmentos:
    paquete = crear_paquete(
        fragmento['id'],
        fragmento['datos']
    )

    paquetes.append(paquete)
    canal.append(paquete)

    print(paquete)
#crear paquete END
end = crear_end()

print('\n------- END -------')
print(end)

canal.append(end)

with open('canal.pkl', 'wb') as archivo:
    pickle.dump(canal, archivo)

