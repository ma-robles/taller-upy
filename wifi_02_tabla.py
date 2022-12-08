#autor: Miguel Ángel Robles Roldan
#https://github.com/ma-robles/taller-upy
#Ejemplo generación de tabla WiFi con MicroPython
#realiza un escaneo de las redes y muestra la lista encontrada
#pide la contraseña y realiza la conexión
#si la contraseña es incorrecta o no es posible contectar, la IP es 0.0.0.0

import time
#importa biblioteca de funciones de red
import network
#importa biblioteca para sockets
import socket

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
página+="""
<tr><td>Temperatura</td><td>30.2</td><td> C </td></tr>
<tr><td>Humedad Relativa</td><td> 40 </td><td> % </td></tr>
<tr><td>Presión </td><td> 777 </td><td> hPa </td></tr>
"""
página +="""
</table>
</body>
</html>"""
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
    response = página
    cn.send(response)
    cn.close()
s.close()
