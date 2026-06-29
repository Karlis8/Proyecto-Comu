import sys
import time
import board
import digitalio
from circuitpython_nrf24l01.rf24 import RF24

# Importamos tus módulos adjuntos
import fragmentacion
import paquetes_binarios

# --- CONFIGURACIÓN DE LOS GPIOS (LEDs) ---
# Usamos digitalio de Blinka para mantener compatibilidad con la librería de la antena
led_verde = digitalio.DigitalInOut(board.D12)
led_verde.direction = digitalio.Direction.OUTPUT

led_amarillo = digitalio.DigitalInOut(board.D6)
led_amarillo.direction = digitalio.Direction.OUTPUT

# Variables de estado para los LEDs
Decodificando = False
Sonido = False
Espera = True        # Por defecto espera una señal
Recibiendo = False

# --- CONFIGURACIÓN DE LA ANTENA NRF24L01 ---
# Asegúrate de conectar los pines SPI correspondientes de la Raspberry Pi
spi = board.SPI()
csn = digitalio.DigitalInOut(board.D8)  # Pin CE0 (GPIO 8)
ce = digitalio.DigitalInOut(board.D17)  # Puedes usar el GPIO 17 para el CE

nrf = RF24(spi, csn, ce)
nrf.open_rx_pipe(1, b"TX_01") # Dirección de tubería de lectura (debe coincidir con el transmisor)
nrf.payload_size = 32         # nRF24L01 trabaja de forma óptima con payloads fijos (máx 32 bytes)
nrf.listen = True             # Colocar la antena en modo escucha

# --- VARIABLES DE CONTROL DE RECEPCIÓN ---
paquetes_recibidos = []
cantidad_esperada = 0
recolectando = False
ultimo_parpadeo = time.time()
estado_intermitente = False

print("Receptor nRF24L01 iniciado. Esperando datos...")

try:
    while True:
        # 1. Manejo del parpadeo de LEDs (Cada 0.5 segundos de forma asíncrona)
        if time.time() - ultimo_parpadeo >= 0.5:
            estado_intermitente = not estado_intermitente
            ultimo_parpadeo = time.time()

        # Lógica física del LED Verde
        if Sonido:
            led_verde.value = True
        elif Decodificando:
            led_verde.value = estado_intermitente
        else:
            led_verde.value = False

        # Lógica física del LED Amarillo
        if Recibiendo:
            led_amarillo.value = True
        elif Espera:
            led_amarillo.value = estado_intermitente
        else:
            led_amarillo.value = False

        # 2. Monitorear la antena nRF24L01
        if nrf.available():
            # Leer el buffer de la antena
            paquete_crudo = nrf.read()
            
            # Identificar el tipo de paquete por el primer byte (TIPO_START, TIPO_DATOS, TIPO_END)
            tipo_byte = paquete_crudo[0]

            # CASO A: Paquete START
            if tipo_byte == paquetes_binarios.TIPO_START:
                info_start = paquetes_binarios.deserializar_start(paquete_crudo[:7]) # >BIH ocupa 7 bytes
                cantidad_esperada = info_start['cantidad_packages'] if 'cantidad_packages' in info_start else info_start['cantidad_paquetes']
                paquetes_recibidos = []
                recolectando = True
                
                # Actualizar estados de LEDs
                Espera = False
                Recibiendo = True
                print(f"\n[START] Iniciando recepción. Tamaño archivo: {info_start['tamano_archivo']} bytes. Paquetes esperados: {cantidad_esperada}")

            # CASO B: Paquete de DATOS
            elif tipo_byte == paquetes_binarios.TIPO_DATOS and recolectando:
                # Quitamos los bytes de relleno (padding) si la antena entregó los 32 bytes completos
                # El paquete de datos binario tiene una cabecera de 3 bytes (>BH) + payload (máx 29 bytes)
                paquete_datos = paquetes_binarios.deserializar_datos(paquete_crudo)
                paquetes_recibidos.append(paquete_datos)
                print(f"[DATOS] Recibido paquete ID: {paquete_datos['id']} ({len(paquetes_recibidos)}/{cantidad_esperada})")

            # CASO C: Paquete END
            elif tipo_byte == paquetes_binarios.TIPO_END and recolectando:
                print("[END] Fin de transmisión recibido por antena.")
                recolectando = False
                Recibiendo = False
                Decodificando = True # Activamos parpadeo verde mientras procesamos
                
                # Forzar actualización visual rápida del procesamiento
                led_verde.value = True 
                
                # Reconstrucción de los datos usando tu módulo fragmentacion.py
                print("Reconstruyendo archivo de datos...")
                datos_totales = fragmentacion.reconstruir(paquetes_recibidos)
                
                # Guardar el archivo reconstruido
                nombre_salida = "archivo_recibido.bin"
                with open(nombre_salida, "wb") as f:
                    f.write(datos_totales)
                
                print(f"¡Archivo guardado exitosamente como '{nombre_salida}'!")
                
                # Volver al estado de espera original
                Decodificando = False
                Espera = True

        # Un leve retraso para no sobrecargar el hilo de ejecución de la CPU
        time.sleep(0.01)

except KeyboardInterrupt:
    print("\nDeteniendo receptor...")
finally:
    nrf.listen = False
    led_verde.value = False
    led_amarillo.value = False
    print("Pines e hilos liberados limpiamente.")
