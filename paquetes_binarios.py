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