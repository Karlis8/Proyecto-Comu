import struct

TIPO_START = 0
TIPO_DATOS = 1
TIPO_END = 2


def serializar_start(tamano_archivo,
                     cantidad_paquetes):

    return struct.pack(
        '>BIH',
        TIPO_START,
        tamano_archivo,
        cantidad_paquetes
    )


def serializar_datos(id_paquete,
                     datos):

    if len(datos) > 29:
        raise ValueError(
            'Payload mayor a 29 bytes'
        )

    cabecera = struct.pack(
        '>BH',
        TIPO_DATOS,
        id_paquete
    )

    return cabecera + datos


def serializar_end():
    return struct.pack(
        '>B',
        TIPO_END
    )


def deserializar_start(paquete):

    _, tamano_archivo, cantidad_paquetes = \
        struct.unpack(
            '>BIH',
            paquete[:7]
        )

    return {
        'tipo': 'START',
        'tamano_archivo': tamano_archivo,
        'cantidad_paquetes': cantidad_paquetes
    }


def deserializar_datos(paquete):

    _, id_paquete = struct.unpack(
        '>BH',
        paquete[:3]
    )

    return {
        'tipo': 'DATOS',
        'id': id_paquete,
        'datos': paquete[3:]
    }


def deserializar_end(paquete):

    return {
        'tipo': 'END'
    }
