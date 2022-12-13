#autor: Miguel Ángel Robles Roldan
#https://github.com/ma-robles/taller-upy
#Ejemplo generación de tabla HTML y actualización con datos de BME280
#realiza un escaneo de las redes y muestra la lista encontrada
#pide la contraseña y realiza la conexión

import time
#importa biblioteca de funciones de red
import network
#importa biblioteca para sockets
import socket
#importa funciones de pines
from machine import Pin, I2C
import bme280

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
#inicializa variables

#inicializa i2c
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=40000)

#inicializa bme280
bme = bme280.BME280(i2c=i2c)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(3)
while True:
    print('Esperando petición')
    try:
        cn, addr = s.accept()
    except:
        break
    print('Conectado a ', str(addr))
    request = cn.recv(1024)
    print('Petición:', str(request))
    #lectura de datos 
    T, P, RH = bme.values
    #definición de página
    página = """<!DOCTYPE html>
      <html lang="es"><head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1">
    </head>
    <body>
    <h1>Datos</h1>
    <table>
    <tr><th> Variable</th> <th>valor</th> <th>Unidad</th><tr>
    """
    #actualización de variables
    página+= "<tr><td>Temperatura</td><td>"+ T[0:-1]+ " </td><td> C </td></tr>"
    página+= "<tr><td>Humedad Relativa</td><td>" + RH[0: -1]+ " </td><td> % </td></tr>"
    página+= "<tr><td>Presión </td><td>" +P[0: -3]+" </td><td> hPa </td></tr>"
    #cierre
    página +="""
    </table>
    </body>
    </html>"""
    response = página
    cn.send(response)
    cn.close()
print('saliendo')
s.close()
