//version para preshower NA64//
//UTFSM CCTVal SiLab//
//Lautaro Narvaez//
//Rimsky Rojas//
//Valparaiso Chile 2017//




#ifndef GPIOINTERF_H
#define GPIOINTERF_H

#include <iostream>
#include <wiringPi.h>
#include <stdio.h>
#include <wiringPiSPI.h>
#include <wiringPiI2C.h>
#include <linux/i2c-dev.h>
#include <linux/swab.h>

//#include <linux/i2c-dev.h>
//#ifndef I2C_FUNC_I2C
//#include <linux/i2c.h>
//#endif

//#include <linux/i2c.h>
#include <sys/ioctl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdint.h>

class gpiointerf
{
  public:
   gpiointerf();
   ~gpiointerf();

   
   void initialize();
   void TH(float&, float&);
   void TH2(float&, float&);
   float Temp(int);
   void disconnect();
   int erno;
   int dev;
   int Thandler, Thandler2, ADChandler;
   unsigned char buff[4];
   unsigned char THmemdir, ADCmemdir, TH2memdir;
   int reading_hum, reading_temp;
   double humidity, temperature;
   char *filename = "/dev/i2c-1";
   unsigned char pwup[2];
   uint32_t val;

   private:

};

#endif 
