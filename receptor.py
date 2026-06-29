import sys
import time
import RPi.GPIO as GPIO

# Importamos la nueva librería pyRF24
from diaries import * # Opcional por si necesitas constantes, pero la base es:
import RF24

# Importamos tus módulos adjuntos
import fragmentacion
import paquetes_binarios

# --- CONFIGURACIÓN DE LOS GPIOS (LEDs) ---
LED_VERDE = 12
LED_AMARILLO = 6

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(LED_VERDE, GPIO.OUT)
GPIO.setup(LED_AMARILLO, GPIO.OUT)

# Variables de estado para los LEDs
Decodificando = False
Sonido = False
Espera = True        # Por defecto inicia esperando señal
Recibiendo = False

# --- CONFIGURACIÓN DE LA ANTENA CON pyRF24 ---
# Parámetros: RF24(ce_pin, csn_pin)
# En Raspberry Pi, usando SPI0: el CE suele ser GPIO 17 (o 22) y el CSN suele ser 8 (CE0) o 7 (CE1)
radio = RF24.RF24(17, 8)

if not radio.begin():
    print("¡Error de hardware! No se pudo comunicar con el módulo nRF24L01.")
    sys.exit(1)

# Configuración del enlace de radio
radio.setPayloadSize(32)             # Payloads fijos de 32 bytes
radio.setChannel(76)                 # Canal de transmisión (debe coincidir con el TX)
radio.setDataRate(RF24.RF24_1MBPS)   # Velocidad de datos (RF24_250KBPS, RF24_1MBPS o RF24_2MBPS)
radio.setPALevel(RF24.RF24_PA_LOW)   # Potencia de amplificación (Baja para pruebas de escritorio)

# Dirección de lectura (Tubería 1). Debe coincidir con los bytes del TX.
direccion_rx = b"TX_01"
radio.openReadingPipe(1, direccion_rx)

# Comenzar a escuchar
radio.startListening()

# --- VARIABLES DE CONTROL DE RECEPCIÓN ---
paquetes_recibidos = []
cantidad_esperada = 0
recolectando = False
ultimo_parpadeo = time.time()
estado_intermitente = False

print("Receptor RF24 iniciado con éxito. Esperando datos...")

try:
    while True:
        # 1. Manejo asíncrono del parpadeo de los LEDs (Cada 0.5 segundos)
        if time.time() - ultimo_parpadeo >= 0.5:
            estado_intermitente = not estado_intermitente
            ultimo_parpadeo = time.time()

        # Lógica física del LED Verde
        if Sonido:
            GPIO.output(LED_VERDE, GPIO.HIGH)
        elif Decodificando:
            GPIO.output(LED_VERDE, estado_intermitente)
        else:
            GPIO.output(LED_VERDE, GPIO.LOW)

        # Lógica física del LED Amarillo
        if Recibiendo:
            GPIO.output(LED_AMARILLO, GPIO.HIGH)
        elif Espera:
            GPIO.output(LED_AMARILLO, estado_intermitente)
        else:
            GPIO.output(LED_AMARILLO, GPIO.LOW)

        # 2. Monitorear la antena con RF24
        if radio.available():
            # Leer los bytes del búfer (leemos los 32 bytes fijos configurados)
            paquete_crudo = radio.read(32)
            
            # Identificar el tipo de paquete por su primer byte
            tipo_byte = paquete_crudo[0]

            # CASO A: Paquete START
            if tipo_byte == paquetes_binarios.TIPO_START:
                # El formato >BIH ocupa 7 bytes en total
                info_start = paquetes_binarios.deserializar_start(paquete_crudo[:7])
                
                # Manejo por si acaso varía el nombre de la clave en tus pruebas
                cantidad_esperada = info_start.get('cantidad_paquetes') or info_start.get('cantidad_packages', 0)
                paquetes_recibidos = []
                recolectando = True
                
                # Actualizar estados de LEDs
                Espera = False
                Recibiendo = True
                print(f"\n[START] Recepción Iniciada.")
                print(f"-> Tamaño total del archivo: {info_start['tamano_archivo']} bytes.")
                print(f"-> Cantidad de paquetes a recibir: {cantidad_esperada}")

            # CASO B: Paquete de DATOS
            elif tipo_byte == paquetes_binarios.TIPO_DATOS and recolectando:
                paquete_datos = paquetes_binarios.deserializar_datos(paquete_crudo)
                paquetes_recibidos.append(paquete_datos)
                print(f"[DATOS] Paquete ID {paquete_datos['id']} guardado. ({len(paquetes_recibidos)}/{cantidad_esperada})")

            # CASO C: Paquete END
            elif tipo_byte == paquetes_binarios.TIPO_END and recolectando:
                print("[END] Fin de transmisión detectado.")
                recolectando = False
                Recibiendo = False
                Decodificando = True  # Cambiamos a verde intermitente en el procesado
                
                # Forzar encendido inmediato del LED verde para dar feedback visual
                GPIO.output(LED_VERDE, GPIO.HIGH)
                
                print("Reconstruyendo el archivo con fragmentacion.py...")
                datos_totales = fragmentacion.reconstruir(paquetes_recibidos)
                
                # Guardar el archivo en el disco de la Raspberry
                nombre_salida = "archivo_reconstruido.bin"
                with open(nombre_salida, "wb") as f:
                    f.write(datos_totales)
                
                print(f"¡Éxito! El archivo se guardó como '{nombre_salida}'.")
                
                # Volver al estado de reposo / espera original
                Decodificando = False
                Espera = True

        # Pequeña tregua al procesador (10ms) para evitar picos de uso de CPU al escuchar
        time.sleep(0.01)

except KeyboardInterrupt:
    print("\nDeteniendo el receptor de forma segura...")

finally:
    radio.stopListening()
    GPIO.cleanup()
    print("Pines GPIO liberados y radio en reposo.")
