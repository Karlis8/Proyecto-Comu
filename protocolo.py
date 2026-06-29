def crear_start(tamano_archivo,
                cantidad_paquetes):
    return {
        'tipo':'START',
        'tamano_archivo': tamano_archivo,
        'cantidad_paquetes': cantidad_paquetes
    }
def crear_paquete(id_paquete, datos):

    return {
        'tipo': 'DATOS',
        'id': id_paquete,
        'datos': datos
    }
def crear_end():

    return{
        'tipo': 'END'
    }
    