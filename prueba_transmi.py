from RF24 import *
from gpiozero import Button, LED
from signal import pause
import subprocess
import threading
import time

# ==========================
# PINES
# ==========================
LED_VERDE = 17      # Pin físico 11
LED_AMARILLO = 23   # Pin físico 16
LED_ROJO = 24       # Pin físico 18
BOTON = 27          # Pin físico 13

# ==========================
# LEDs y botón
# ==========================
led_verde = LED(LED_VERDE)
led_amarillo = LED(LED_AMARILLO)
led_rojo = LED(LED_ROJO)

boton = Button(BOTON)

# ==========================
# NRF24
# ==========================
radio = RF24(22, 0)      # CE=GPIO22, CSN=CE0
direccion = b"00001"

if not radio.begin():
    raise RuntimeError("No se pudo inicializar el NRF24L01")

radio.setAutoAck(False)     # SOLO PARA PRUEBAS
radio.setPALevel(RF24_PA_HIGH)
radio.setDataRate(RF24_1MBPS)
radio.openWritingPipe(direccion)
radio.stopListening()

# ==========================
# Variables globales
# ==========================
parpadeando = False
proceso_grabacion = None

# ==========================
# Funciones LEDs
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
# Transmisión
# ==========================
def transmitir_archivo(nombre):
    global parpadeando

    inicio = time.time()

    apagar_todos()

    parpadeando = True
    hilo = threading.Thread(target=parpadear_todos)
    hilo.start()

    enviados = 0

    with open(nombre, "rb") as f:

        radio.write(b"START")
        time.sleep(0.01)

        while True:
            datos = f.read(32)

            if not datos:
                break

            radio.write(datos)
            enviados += 1

        radio.write(b"END")

    parpadeando = False
    hilo.join()

    tiempo = time.time() - inicio

    print(f"Paquetes enviados: {enviados}")
    print(f"Tiempo de envío: {tiempo:.2f} s")

    # Fin de transmisión
    led_rojo.on()
    time.sleep(2)

    apagar_todos()
    led_verde.on()


# ==========================
# Grabación
# ==========================
def iniciar_grabacion():
    global proceso_grabacion

    # Evita múltiples pulsaciones
    if proceso_grabacion is not None:
        return

    print("Grabando...")

    apagar_todos()
    led_amarillo.on()

    proceso_grabacion = subprocess.Popen([
        "arecord",
        "-D", "plughw:3,0",
        "-f", "S16_LE",
        "-r", "8000",
        "-c", "1",
        "prueba.wav"
    ])


def detener_grabacion():
    global proceso_grabacion

    if proceso_grabacion is None:
        return

    print("Deteniendo grabación...")

    proceso_grabacion.terminate()
    proceso_grabacion.wait()
    proceso_grabacion = None

    print("Enviando...")
    transmitir_archivo("prueba.wav")


# ==========================
# Programa principal
# ==========================
apagar_todos()
led_verde.on()

print("Sistema listo.")
print("Mantén presionado el botón para grabar.")

boton.when_pressed = iniciar_grabacion
boton.when_released = detener_grabacion

pause()