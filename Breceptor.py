import time
import subprocess
import os
import RPi.GPIO as GPIO
from RF24 import *

import fragmentacion
import paquetes_binarios

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

radio = RF24(25, 0)

if not radio.begin():
    raise RuntimeError(
        "No se pudo inicializar NRF24"
    )

radio.setChannel(76)
radio.setDataRate(RF24_250KBPS)
radio.setPALevel(RF24_PA_HIGH)
radio.setAutoAck(True)

direccion = b"TX_01"

radio.openReadingPipe(
    1,
    direccion
)

radio.startListening()

paquetes = []
cantidad_esperada = 0
tamano_archivo = 0
recolectando = False

ultimo_parpadeo = time.time()
estado = False

print(
    "Esperando transmisión..."
)

try:

    while True:

        if time.time() - \
                ultimo_parpadeo >= 0.5:

            estado = not estado
            ultimo_parpadeo = time.time()

        if not recolectando:
            GPIO.output(
                LED_AMARILLO,
                estado
            )

        if radio.available():

            datos = radio.read(32)

            tipo = datos[0]

            if tipo == \
                    paquetes_binarios.TIPO_START:

                info = \
                    paquetes_binarios.deserializar_start(
                        datos
                    )

                paquetes = []

                cantidad_esperada = \
                    info[
                        'cantidad_paquetes'
                    ]

                tamano_archivo = \
                    info[
                        'tamano_archivo'
                    ]

                recolectando = True

                GPIO.output(
                    LED_AMARILLO,
                    GPIO.HIGH
                )

                print(
                    f"Tamaño: "
                    f"{tamano_archivo}"
                )

                print(
                    f"Paquetes esperados: "
                    f"{cantidad_esperada}"
                )

            elif tipo == \
                    paquetes_binarios.TIPO_DATOS \
                    and recolectando:

                paquete = \
                    paquetes_binarios.deserializar_datos(
                        datos
                    )

                paquetes.append(
                    paquete
                )

                if len(paquetes) % 100 == 0:
                    print(
                        f"Recibidos "
                        f"{len(paquetes)}"
                    )

            elif tipo == \
                    paquetes_binarios.TIPO_END \
                    and recolectando:

                recolectando = False

                GPIO.output(
                    LED_AMARILLO,
                    GPIO.LOW
                )

                print(
                    f"Paquetes recibidos: "
                    f"{len(paquetes)}"
                )

                if len(paquetes) != \
                        cantidad_esperada:

                    print(
                        f"Error: "
                        f"{len(paquetes)}/"
                        f"{cantidad_esperada}"
                    )

                    continue

                for _ in range(6):
                    GPIO.output(
                        LED_VERDE,
                        GPIO.HIGH
                    )
                    time.sleep(0.2)
                    GPIO.output(
                        LED_VERDE,
                        GPIO.LOW
                    )
                    time.sleep(0.2)

                audio = \
                    fragmentacion.reconstruir(
                        paquetes
                    )

                audio = \
                    audio[:tamano_archivo]

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

                os.remove(nombre)

                print(
                    "Audio reproducido"
                )

        time.sleep(0.001)

except KeyboardInterrupt:
    pass

finally:
    radio.stopListening()
    GPIO.cleanup()
