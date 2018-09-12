# Base Movil Telecomunicada con MicroPython y mando PS4

## Motivación del proyecto
El proyecto nació con el objetivo de participar en uno de los concursos de la universidad ESPOL en Ecuador, El Reto Del Pacífico, junto con la implementación de nuevas plataformas como es la de MicroPython. Plataforma con la cual además se buscó introducir a las personas en el mundo de la electrónica, programación y robótica, por ser una de las más divertidas e intuitivas como lo es tambien Python.

## Descripción
El proyecto basicamente trata sobre el manejo de una Base Movil orientada al uso en Fútbol Robótico a través de la implementación de distintas plataformas como Python (código en computadora), MicroPython (código del microcontrolador) y Arduino.

### Elementos de Control

* Computadora: Corre el código de Python que recibe y envía los datos del movimiento del mando.
* ESP-01: Microcontrolador con chip ESP8266, programado con MicroPython, capaz de establecer comunicación WiFi y transmición de datos. Recibe los datos vía WiFi de la computadora con el código de Python y los transmite por UART al Arduino.
* Arduino Mega 2560: Usado para el manejo de los motores Dinamixeles, recibe los datos de movimiento del ESP-01, via UART.

### Códigos
El proyecto consiste esta formado con los siguientes códigos:

* Python controlpc.py (código de computadora)
	* Se encarga de recibir los datos de un JoyStick de mando PS4 para el movimiento de los motores de la Base Móvil, el mando a utilizar puede ser otro, mientras la computadora lo reconozca. Usa la libreria de PyGame para poder obtener los datos de los JoySticks y poder despues mandarlos por un objeto socket vía WiFi al ESP-01.
* MicroPython main.py (código en ESP-01)
	* La versión de MicroPython usada en este caso es 1.8.7. Este código se encarga del recibimiento de datos por WiFi y el envio del dato por UART al Arduino.
* Arduino manejodinamixeles.ino (código en Arduino)
	* Se encarga de recibir los movimiento para los motores Dinamixeles por UART y el manejo de los mismos. Se usa la libreria de Dinamixel.

Para la estructura de la Base Móvil, se usaron Legos debido a que estos son intuitivos y fácil de usar para realizar prototipos, en el caso de querer replicar el mismo proyecto, aquello puede darse a gusto de cada persona.

## Procedimiento

### Diagrama General

![alt text](https://github.com/FunPythonEC/Futbol_soccer/blob/master/BaseMovilTelecomunicado/Imagenes/diagramaBaseMovil.png)

## Licencia
<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Licencia de Creative Commons" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br />Este obra está bajo una <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">licencia de Creative Commons Reconocimiento-NoComercial-CompartirIgual 4.0 Internacional</a>.
