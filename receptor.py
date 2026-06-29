import RPi.GPIO as GPIO
from time import sleep

# --- CONFIGURACIÓN DE PINES ---
LED_VERDE = 12
LED_AMARILLO = 6

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(LED_VERDE, GPIO.OUT)
GPIO.setup(LED_AMARILLO, GPIO.OUT)

# --- VARIABLES DE CONTROL (Modifica estos valores para probar) ---
Decodificando = True   # Si es True -> Verde parpadea
Sonido = False         # Si es True -> Verde se queda fijo (Prioridad)

Espera = False         # Si es True -> Amarillo parpadea
Recibiendo = True      # Si es True -> Amarillo se queda fijo (Prioridad)

# Variable auxiliar para alternar el parpadeo (True / False)
estado_intermitente = False

print("Programa corriendo... Presiona Ctrl+C para salir.")

try:
    while True:
        # Alternamos el estado intermitente en cada ciclo (cada 0.5 segundos)
        estado_intermitente = not estado_intermitente

        # ==========================================
        # LÓGICA DEL LED VERDE (Pin 12)
        # ==========================================
        if Sonido:
            GPIO.output(LED_VERDE, GPIO.HIGH)       # Encendido fijo
        elif Decodificando:
            GPIO.output(LED_VERDE, estado_intermitente)  # Intermitente
        else:
            GPIO.output(LED_VERDE, GPIO.LOW)        # Apagado si nada es verdadero

        # ==========================================
        # LÓGICA DEL LED AMARILLO (Pin 6)
        # ==========================================
        if Recibiendo:
            GPIO.output(LED_AMARILLO, GPIO.HIGH)     # Encendido fijo
        elif Espera:
            GPIO.output(LED_AMARILLO, estado_intermitente) # Intermitente
        else:
            GPIO.output(LED_AMARILLO, GPIO.LOW)      # Apagado si nada es verdadero

        # Pausa de 0.5 segundos que dicta el ritmo del parpadeo
        sleep(0.5)

except KeyboardInterrupt:
    print("\nPrograma detenido por el usuario.")
finally:
    GPIO.cleanup() # Buena práctica: limpia los pines al salir
    print("Pines GPIO liberados.")

