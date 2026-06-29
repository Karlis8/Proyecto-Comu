import struct

TIPO_START = 0
TIPO_DATOS = 1
TIPO_END = 2

def serializar_start(
        tamano_archivo,
        cantidad_paquetes):
    return struct.pack(
        '>BIH',
        TIPO_START,
        tamano_archivo,
        cantidad_paquetes
    )

def serializar_end():

    return struct.pack(
        '>B',
        TIPO_END
    )

def serializar_datos(
        id_paquete,
        datos):
    
    if len(datos) > 29:
        raise ValueError(
            'El payload excede los 29 bytes'
        )
    
    cabecera = struct.pack(
        '>BH',
        TIPO_DATOS,
        id_paquete
    )

    return cabecera + datos

def deserializar_start(paquete):

    _, tamano_archivo, cantidad_paquetes = \
        struct.unpack('>BIH', paquete)

    return {
        'tipo': 'START',
        'tamano_archivo': tamano_archivo,
        'cantidad_paquetes': cantidad_paquetes
    }

def deserializar_datos(paquete):

    tipo, id_paquete = struct.unpack(
        '>BH',
        paquete[:3]
    )

    datos = paquete[3:]

    return {
        'tipo': 'DATOS',
        'id': id_paquete,
        'datos': datos
    }

def deserializar_end(paquete):

    return {
        'tipo': 'END'
    }