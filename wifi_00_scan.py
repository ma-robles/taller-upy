#autor: Miguel Ángel Robles Roldan
#https://github.com/ma-robles/taller-upy
#Ejemplo de conección a red WiFi con MicroPython
#realiza un escaneo de las redes y muestra la lista encontrada
#pide la contraseña y realiza la conexión
#si la contraseña es incorrecta o no es posible contectar, la IP es 0.0.0.0

import time
#importa biblioteca de funciones de red
import network

#crea un objeto de tipo WLAN
wlan = network.WLAN(network.STA_IF)
#activa la red
wlan.active(True)
#realiza una exploración de las redes WiFi
aps = wlan.scan()
#imprime las redes encontradas
for i,ap in enumerate(aps):
    print(i,')', ap[0].decode())
#asigna el SSID de acuerdo a la selección hecha
ans = int(input('Selecciona Red WiFi:'))
SSID = aps[ans][0].decode()
#solicita password
password = input('Ingresa contraseña para '+SSID +':')
#conecta con los datos proporcionados
wlan.connect(SSID, password)
time.sleep(3)
while not wlan.isconnected() and wlan.status() >=0:
    print('*')
    time.sleep(1)
#imprime IP
print('IP:', wlan.ifconfig()[0])
