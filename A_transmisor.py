from RF24 import *
from gpiozero import Button, LED
from signal import pause
import subprocess
import threading
import time

# ==========================
# LEDs y botón
# ==========================

LED_VERDE = 17
LED_AMARILLO = 23
LED_ROJO = 24
BOTON = 27

led_verde = LED(LED_VERDE)
led_amarillo = LED(LED_AMARILLO)
led_rojo = LED(LED_ROJO)

boton = Button(BOTON)

# ==========================
# Radio
# ==========================

radio = RF24(22, 0)

if not radio.begin():
    raise RuntimeError(
        "No se pudo inicializar NRF24"
    )

radio.setChannel(76)
radio.setDataRate(RF24_250KBPS)
radio.setPALevel(RF24_PA_HIGH)
radio.setAutoAck(True)

direccion = b"1Node"

radio.openWritingPipe(direccion)
radio.stopListening()

# ==========================
# Protocolo
# ==========================

START_BYTE = 0xAA
PAYLOAD_SIZE = 27
PACKET_SIZE = 32
SEQ_END = 0xFFFF

# ==========================
# Variables
# ==========================

parpadeando = False
proceso_grabacion = None


# ==========================
# LEDs
# ==========================

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


# ==========================
# Paquetes
# ==========================

def build_packet(seq, data_chunk):

    seq_high = (seq >> 8) & 0xFF
    seq_low = seq & 0xFF

    length = len(data_chunk)

    padded = data_chunk.ljust(
        PAYLOAD_SIZE,
        b"\x00"
    )

    crc = (
        START_BYTE
        + seq_high
        + seq_low
        + length
        + sum(padded)
    ) & 0xFF

    return (
        bytes([
            START_BYTE,
            seq_high,
            seq_low,
            length
        ])
        + padded
        + bytes([crc])
    )


def build_all_packets(datos):

    packets = []

    for i in range(
            0,
            len(datos),
            PAYLOAD_SIZE):

        chunk = datos[
            i:i+PAYLOAD_SIZE
        ]

        seq = i // PAYLOAD_SIZE

        packets.append(
            build_packet(
                seq,
                chunk
            )
        )

    packets.append(
        build_packet(
            SEQ_END,
            b""
        )
    )

    return packets


# ==========================
# Transmisión
# ==========================

def transmitir_archivo(nombre):

    global parpadeando

    with open(
            nombre,
            "rb"
    ) as f:

        datos = f.read()

    paquetes = build_all_packets(
        datos
    )

    print(
        f"Enviando "
        f"{len(paquetes)} paquetes"
    )

    parpadeando = True

    hilo = threading.Thread(
        target=parpadear_todos
    )

    hilo.start()

    for i, paquete in enumerate(
            paquetes):

        ok = radio.write(
            paquete
        )

        if not ok:
            print(
                f"Fallo "
                f"{i}"
            )

        time.sleep(0.003)

    parpadeando = False
    hilo.join()

    led_rojo.on()
    time.sleep(2)

    apagar_todos()
    led_verde.on()

    print(
        "Transmisión terminada"
    )


# ==========================
# Grabación
# ==========================

def iniciar_grabacion():

    global proceso_grabacion

    if proceso_grabacion:
        return

    apagar_todos()
    led_amarillo.on()

    print(
        "Grabando..."
    )

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

    print(
        "Enviando..."
    )

    transmitir_archivo(
        "prueba.wav"
    )


# ==========================
# Main
# ==========================

led_verde.on()

print(
    "Sistema listo"
)

boton.when_pressed = \
    iniciar_grabacion

boton.when_released = \
    detener_grabacion

pause()
