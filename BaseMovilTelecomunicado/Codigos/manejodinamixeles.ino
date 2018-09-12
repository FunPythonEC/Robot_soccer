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

/*
* Programa del robot en Arduino MEGA
* Codigo del robot
* ID_ROBOT: ID del robot
* DATA_INDEX: indice donde empiezan los datos del robot
* DATA_SIZE: tamaño de la trama
* funciones creadas: parpadearMotores, parpadearLed
*/

#include <DynamixelSerial1.h>
/*
*el ID_ROBOT en si se especifica por si es que se hace lo mismo con 2 o más robots
*DATA_INDEX es necesario para saber que datos va a coger el robor con este codigo
*DATA_SIZE es el tamaño de la lista que se envia por el codigo de controlpc.py
*/
#define MOTOR_LEFT 1
#define MOTOR_RIGHT 2
#define ID_ROBOT 1
#define DATA_INDEX 1
#define DATA_SIZE 4

/*
*se especifica una lista de enteros para poder ponerlos valores que se envian al los dinamixeles
*como inData[], además se necesita no solo especificar la velocidad sino tambien la
*direccion, por eso se ponen las variables velLeft y dirLeft
*/
int inData[DATA_SIZE];
int index=-1;
int dato;
int velLeft = 0;
int velRight = 0;
int dirLeft;
int dirRight;

void setup(){
  Serial3.begin(115200);
  
  Dynamixel.begin(1000000,2);  // Inicialize the servo at 1Mbps and Pin Control 2
  delay(1000);
  Dynamixel.setEndless(MOTOR_LEFT,ON);
  Dynamixel.setEndless(MOTOR_RIGHT,ON);

  Dynamixel.turn(1,LEFT,500);
  Dynamixel.turn(2,LEFT,500);
  delay(500);
  //Gira contra manecillas de reloj
  Dynamixel.turn(1,RIGTH,500);
  Dynamixel.turn(2,RIGTH,500);
  delay(500);
  Dynamixel.turn(1,LEFT,0);
  Dynamixel.turn(2,LEFT,0); 
}

void loop(){
  /*
  *debido a que en el serial se reciben los datos de byte en byte
  *es necesario tan solo identificar cuando comienza con 240
  *y cuando acaba, que seria cuando este es 247
  *para luego mandarlo a una funcion llama ValProcces()
  */
  while (Serial3.available()) {  
     int iByte = Serial3.read();
     if (iByte == 240){
         index = 0;
     }
  
     if (index>=0) {
         inData[index++] = iByte;  // adding to message
         if (iByte == 247) {
             ValProcces(inData);
             index = -1;
         }
     }
  }  
}

//Funcion para procesar pack, se encarga de escoger 
//los valores del robot y enviarlos a los dinamixeles
void ValProcces(int data[]){
  velLeft = (data[DATA_INDEX]-100)*10;
  velRight = (data[DATA_INDEX+1]-100)*10;
  if (velLeft > 0){
    dirLeft = RIGTH;
   }
   else{
    dirLeft = LEFT;
   }
  if (velRight>0){
    dirRight = LEFT;
  }
  else
  {
    dirRight = RIGTH;
  }
  velLeft = abs(velLeft);
  velRight = abs(velRight);
  Dynamixel.turn(MOTOR_LEFT, dirLeft, velLeft); 
  Dynamixel.turn(MOTOR_RIGHT, dirRight , velRight);   
}