def fragmentar(datos,
               tamano_paquete):

    paquetes = []

    for i in range(
            0,
            len(datos),
            tamano_paquete):

        numero = len(paquetes)

        payload = datos[
            i:i+tamano_paquete
        ]

        paquetes.append({
            'id': numero,
            'datos': payload
        })

    return paquetes


def reconstruir(paquetes):

    paquetes = sorted(
        paquetes,
        key=lambda p: p['id']
    )

    datos = b''

    for paquete in paquetes:
        datos += paquete['datos']

    return datos
