#autor: Miguel Ángel Robles Roldan
#https://github.com/ma-robles/taller-upy
#Ejemplo Access Point y bme280

import time
#importa biblioteca de funciones de red
import network
#importa biblioteca para sockets
import socket
#importa funciones de pines
from machine import Pin, I2C
import bme280

#crea un objeto de tipo WLAN AP
wlan = network.WLAN(network.AP_IF)
# configura la red
wlan.config(essid="rp2testWiFi", password="12344321")
#activa la red
wlan.active(True)

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
