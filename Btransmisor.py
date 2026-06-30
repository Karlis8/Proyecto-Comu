from RF24 import *
from gpiozero import Button, LED
from signal import pause
import subprocess
import threading
import time

import fragmentacion
import paquetes_binarios

LED_VERDE = 17
LED_AMARILLO = 23
LED_ROJO = 24
BOTON = 27

led_verde = LED(LED_VERDE)
led_amarillo = LED(LED_AMARILLO)
led_rojo = LED(LED_ROJO)

boton = Button(BOTON)

radio = RF24(22, 0)

if not radio.begin():
    raise RuntimeError(
        "NRF24 no encontrado"
    )

radio.setChannel(76)
radio.setDataRate(RF24_1MBPS)
radio.setPALevel(RF24_PA_HIGH)
radio.setAutoAck(True)

direccion = b"TX_01"

radio.openWritingPipe(direccion)
radio.stopListening()

parpadeando = False
proceso_grabacion = None


def apagar_todos():
    led_verde.off()
    led_amarillo.off()
    led_rojo.off()


def parpadear_todos():
    global parpadeando

    while parpadeando:
        led_verde.toggle()
        led_amarillo.toggle()
        led_rojo.toggle()
        time.sleep(0.2)

    apagar_todos()


def transmitir_archivo(nombre):

    global parpadeando

    with open(nombre, 'rb') as f:
        datos = f.read()

    paquetes = fragmentacion.fragmentar(
        datos,
        29
    )

    tamano = len(datos)
    cantidad = len(paquetes)

    print(
        f"Enviando {cantidad} paquetes"
    )

    apagar_todos()

    parpadeando = True
    hilo = threading.Thread(
        target=parpadear_todos
    )
    hilo.start()

    radio.write(
        paquetes_binarios.serializar_start(
            tamano,
            cantidad
        )
    )

    time.sleep(0.05)

    for paquete in paquetes:

        datos_serializados = \
            paquetes_binarios.serializar_datos(
                paquete['id'],
                paquete['datos']
            )

        radio.write(
            datos_serializados.ljust(
                32,
                b'\0'
            )
        )

    radio.write(
        paquetes_binarios.serializar_end()
    )

    parpadeando = False
    hilo.join()

    led_rojo.on()
    time.sleep(2)

    apagar_todos()
    led_verde.on()

    print("Transmisión terminada")


def iniciar_grabacion():

    global proceso_grabacion

    if proceso_grabacion:
        return

    apagar_todos()
    led_amarillo.on()

    proceso_grabacion = \
        subprocess.Popen([
            "arecord",
            "-D",
            "plughw:3,0",
            "-f",
            "S16_LE",
            "-r",
            "8000",
            "-c",
            "1",
            "prueba.wav"
        ])


def detener_grabacion():

    global proceso_grabacion

    if proceso_grabacion is None:
        return

    proceso_grabacion.terminate()
    proceso_grabacion.wait()
    proceso_grabacion = None

    transmitir_archivo(
        "prueba.wav"
    )


led_verde.on()

print("Sistema listo")

boton.when_pressed = iniciar_grabacion
boton.when_released = detener_grabacion

pause()
