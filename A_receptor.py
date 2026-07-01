import time
import subprocess
import os
import RPi.GPIO as GPIO
from RF24 import *

# ==========================
# LEDs
# ==========================

LED_VERDE = 12
LED_AMARILLO = 6

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(
    LED_VERDE,
    GPIO.OUT
)

GPIO.setup(
    LED_AMARILLO,
    GPIO.OUT
)

# ==========================
# Radio
# ==========================

radio = RF24(25, 0)

if not radio.begin():
    raise RuntimeError(
        "No se pudo inicializar NRF24"
    )

radio.setChannel(76)
radio.setDataRate(RF24_250KBPS)
radio.setPALevel(RF24_PA_HIGH)
radio.setAutoAck(True)

direccion = b"1Node"

radio.openReadingPipe(
    1,
    direccion
)

radio.startListening()

# ==========================
# Protocolo
# ==========================

START_BYTE = 0xAA
PAYLOAD_SIZE = 27
PACKET_SIZE = 32
SEQ_END = 0xFFFF

# ==========================
# CRC
# ==========================

def verify_crc(packet):

    crc = sum(
        packet[:31]
    ) & 0xFF

    return crc == packet[31]


def parse_packet(packet):

    if len(packet) != 32:
        return None

    if packet[0] != START_BYTE:
        return None

    if not verify_crc(packet):
        return None

    seq = (
        packet[1] << 8
    ) | packet[2]

    length = packet[3]

    if length > PAYLOAD_SIZE:
        return None

    data = packet[
        4:4+length
    ]

    return seq, data


# ==========================
# Espera
# ==========================

ultimo = time.time()
estado = False

print(
    "Esperando..."
)

try:

    while True:

        if time.time() - ultimo > 0.5:

            estado = not estado
            ultimo = time.time()

            GPIO.output(
                LED_AMARILLO,
                estado
            )

        if radio.available():

            GPIO.output(
                LED_AMARILLO,
                GPIO.HIGH
            )

            print(
                "Recibiendo..."
            )

            buffer = {}

            while True:

                if radio.available():

                    paquete = \
                        radio.read(
                            PACKET_SIZE
                        )

                    resultado = \
                        parse_packet(
                            paquete
                        )

                    if resultado is None:
                        continue

                    seq, datos = \
                        resultado

                    if seq == SEQ_END:
                        break

                    buffer[
                        seq
                    ] = datos

            print(
                f"Paquetes: "
                f"{len(buffer)}"
            )

            audio = bytearray()

            if buffer:

                max_seq = max(
                    buffer.keys()
                )

                for seq in range(
                        max_seq + 1):

                    if seq in buffer:
                        audio.extend(
                            buffer[seq]
                        )
                    else:
                        audio.extend(
                            bytes(
                                PAYLOAD_SIZE
                            )
                        )

            nombre = \
                "/tmp/audio.wav"

            with open(
                    nombre,
                    "wb"
            ) as f:

                f.write(audio)

            GPIO.output(
                LED_VERDE,
                GPIO.HIGH
            )

            subprocess.run([
                "aplay",
                "-D",
                "plughw:1,0",
                nombre
            ])

            GPIO.output(
                LED_VERDE,
                GPIO.LOW
            )

            os.remove(
                nombre
            )

            print(
                "Audio reproducido"
            )

        time.sleep(
            0.001
        )

except KeyboardInterrupt:
    pass

finally:
    radio.stopListening()
    GPIO.cleanup()
