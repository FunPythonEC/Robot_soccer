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
"""


#Usamos la librería Pygame con la cual obtenemos los datos del control PS4
import time
import pygame
import struct
import socket
import sys

"""
Inicializo la trama con cabecera 240 y fin 247, los demas datos corresponden a la velocidad 0 de los motores
En este caso se definió que 100 seria el valor con el que Arduino definiría que no hay movimiento en las
llantas mientras que 0 es la maxima velocidad en reversa y 200 la maxima velocidad hacia delante.
la trama se define como [240,velIzqR1, velDerR1, velIzqR2, velDerR2, 247]
de tal manera que los datos de la posición 2 y 3 le corresponden a la base 1, mientras que los dos
siguientes a la segunda
en este caso el codigo de la computadora ha sido realizado para un solo robot
por lo que la lista dataSerial es de la siguiente manera
"""
dataSerial = [240,100,100,247]

#SOCKETS
#Se crea el objeto socket necesario para la conexion
Robot1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

"""
CONEXION ROBOTS
ROBOT 1
En connect se especifica la IP que le da el router o estación WiFi
al ESP para poder establecer la conexión y el puerto que depende de
la elección de cada persona
"""
Robot1.connect(("IP_BaseMovil",123))
print("Robot1 Conectado")
time.sleep(1)

"""
La siguiente parte del codigo es proporcionada por la pagina de Pygame
para poder coger los datos del mando PS4 los cuales son ademas mostrados
en pantalla aunque solo para los joysticks ya que es lo que se usa
"""
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)

class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def Print(self, screen, textString):
        textBitmap = self.font.render(textString, True, BLACK)
        screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10


pygame.init()

# Set the width and height of the screen [width,height]
size = [500, 700]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("My Game")

#Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Initialize the joysticks
pygame.joystick.init()

# Get ready to print
textPrint = TextPrint()


axis_data = None
# -------- Main Program Loop -----------
while done==False:


    # EVENT PROCESSING STEP
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop

        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
        #if event.type == pygame.JOYAXISMOTION and (event.axis == 1 or event.axis == 3):
        #    axis_data[event.axis] = round(event.value, 2)
        if event.type == pygame.JOYBUTTONDOWN:
            print("Joystick button pressed.")
        if event.type == pygame.JOYBUTTONUP:
            print("Joystick button released.")


        # DRAWING STEP
        # First, clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.
        screen.fill(WHITE)
        textPrint.reset()

        # Get count of joysticks
        joystick_count = pygame.joystick.get_count()

        textPrint.Print(screen, "Number of joysticks: {}".format(joystick_count) )
        textPrint.indent()

#ojo        dataSerial = [254]

        # For each joystick:
        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()

            textPrint.Print(screen, "Joystick {}".format(i) )
            textPrint.indent()

            # Get the name from the OS for the controller/joystick
            name = joystick.get_name()
            textPrint.Print(screen, "Joystick name: {}".format(name) )

            # Usually axis run in pairs, up/down for one, and left/right for
            # the other.
            axes = joystick.get_numaxes()
            textPrint.Print(screen, "Number of axes: {}".format(axes) )
            textPrint.indent()

            #LISTA PARA PAQUETE DE DATOS CON CABECERA
            #con estos metodos get_axis(int)
            #obtenemos los datos de los joysticks
            axisLeft = joystick.get_axis(1)
            axisRight = joystick.get_axis(3)

            textPrint.Print(screen, "Axis left {} value: {:>6.3f}".format(1, axisLeft))
            textPrint.Print(screen, "Axis right {} value: {:>6.3f}".format(3, axisRight))


            #Hacemos la conversión para los datos obtenidos de la palanca, notese
            #que para ello debe observar antes que datos envia la que usa para luego
            #poder definir la conversión ya que el rango de valores puede variar.
            velLeft = int(100.0 - (axisLeft**3 * 100.0))

            velRight = int(100.0 - (axisRight**3 * 100.0))


            if axisLeft==0:

                velLeft=101

            if axisRight==0:

                velRight=101

            #en el caso de que se pueda o se quiera tener un boton de disparo
            #se puede especificar de esta manera
            Shot=joystick.get_button(1)

            #definimos los valores de la trama
            if (i==0):
                dataSerial[1] = velLeft
                dataSerial[2] = velRight
                
                dataSerial[3] = velLeft
                dataSerial[4] = velRight
            print(dataSerial)
            
            textPrint.unindent()

            buttons = joystick.get_numbuttons()
            #textPrint.print(screen, "Number of buttons: {}".format(buttons) )
            textPrint.indent()

            for i in range(buttons):
                button = joystick.get_button( i )
                #textPrint.print(screen, "Button {:>2} value: {}".format(i,button) )
            textPrint.unindent()

            # Hat switch. All or nothing for direction, not like joysticks.
            # Value comes back in an array.
            hats = joystick.get_numhats()
            #textPrint.print(screen, "Number of hats: {}".format(hats) )
            textPrint.indent()

            for i in range( hats ):
                hat = joystick.get_hat( i )
                #textPrint.print(screen, "Hat {} value: {}".format(i, str(hat)) )
            textPrint.unindent()
            textPrint.unindent()

        #Con la libreria de struct hacemos un paquete de bytes con los datos
        #de movimiento para los motores que luego es enviado al ESP01
        dfSerial=struct.pack("4B", *dataSerial)

        # Limit to 20 frames per second
        clock.tick(20)

        #Con el socket de la base movil definida se usa el metodo send para enviar
        #el paquete de datos de la trama, se lo encierra en un try en caso de que
        #haya un error en el envio
        try:
            Robot1.send(dfSerial)
        except Exception:
            pass

        print(dfSerial)

        pygame.display.flip()


Robot1.close()
pygame.quit ()