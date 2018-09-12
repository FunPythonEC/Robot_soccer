
"""
MIT License

Copyright (c) 2017 FunPython

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Programado en la version 1.8.7 de MicroPython
puede que en otras versiones no esten implementados
los metodos incluidos en este codigo
librerias usadas para controlar los pines, la red WiFi
los puertos y tiempos
"""

from machine import UART
import network
import socket
import time

"""
Response() funcion utilizada para agarrar los
datos enviados por el codigo externo.
"""
def response(connfd):
    while True:
        bytesRecv = connfd.recv(1024)
        if bytesRecv != None:
            """
            decode() necesario para poder convertir
            los datos de bytes a ascii para luego
            enviarlos por UART
            """
            strRecv = bytesRecv.decode()
            #con write() mandamos el dato al arduino
            uart.write(strRecv)

"""
Se inicializa un objeto UART para el envio de datos
por serial, en este caso debido a que el ESP-01
solo tiene un pin TX, este se especifica como el pin 0
""" 
uart = UART(0, 115200)
uart.init(115200, bits=8, parity=None, stop=1)

"""
Se habilita la conexion wifi para el ESP-01
con el objeto WLAN de network
"""
nic = network.WLAN(network.STA_IF)
nic.active(True)


while nic.isconnected():
    #connect(), nos ayuda a conectarnos, se especifica
    #nombre de red y clave.
    nic.connect('SSID', 'PASSWORD')
    time.sleep(1)

print(nic.isconnected())
print(nic.ifconfig())

"""
Se inicializa un socket, necesario para que el esp escuche
datos enviados por un codigo externo.
"""
s = socket.socket()
"""
bind() ayuda a conectarse al puerto del codigo
por el que se envian los datos
"""
s.bind(("",123))
#listen() es el metodo para escuchar los datos.
s.listen(1)

#se pone un while True: para escuchar y enviar los datos de manera constante
while True:
    cl, addr = s.accept()
    response(cl) #funcion para decidir que hacer con la nueva conexion
    cl.close()
