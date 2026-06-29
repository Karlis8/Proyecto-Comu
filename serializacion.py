import pickle

def serializar(mensaje):
    """
    Convierte un objeto de Python en bytes
    """
    return pickle.dumps(mensaje)

def deserializar(datos):
    """
    Convierte bytes nuevanmente en python
    """
    return pickle.loads(datos)
