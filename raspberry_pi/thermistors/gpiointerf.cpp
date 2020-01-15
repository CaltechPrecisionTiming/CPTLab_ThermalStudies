
#include "gpiointerf.h"
#include <wiringPi.h>
#include <stdio.h>

//#define AD5593R_MODE_CONF (0 << 4)
#define AD5592R_REG_ADC_SEQ  0x02
#define AD5593R_MODE_ADC_READBACK (4 << 4)
#define AD5593R_reg_adc_inp 0x04
#define AD5593R_GPCR 0x03
#define AD5593R_REF 0x0B
#define AD5593R_REG_RB (7 << 4)

gpiointerf::gpiointerf(){



}
void gpiointerf::initialize(){

  dev=2;

  for(int i = 0; i++; i<4)buff[i]=0x00;
  wiringPiSetup();

  pinMode(29, OUTPUT);  // A0 first ADC
  digitalWrite(29,0);
  
  pinMode(28, OUTPUT);  // reset
  digitalWrite(28,1);//
  
  /*pullUpDnControl(4,PUD_DOWN);
  pullUpDnControl(5,PUD_DOWN);
  pullUpDnControl(6,PUD_DOWN);
  pullUpDnControl(3,PUD_DOWN);
  
  
  */
 //erno = wiringPiSPISetup(1,200000);
  pwup[1]=0x00;
  pwup[0]=0x80;

  THmemdir = 0x28;
  TH2memdir = 0x40;
  ADCmemdir = 0x10;
  val=666;

 if((Thandler = open(filename, O_RDWR)) < 0){
   std::cout<<"failed to open i2c port for T&H"<<std::endl;
 }
 if((Thandler2 = open(filename, O_RDWR)) < 0){
   std::cout<<"failed to open i2c port for T2&H2"<<std::endl;
 }
 //std::cout<<"than"<<Thandler<<std::endl;
 if((ADChandler = open(filename, O_RDWR)) < 0){
   std::cout<<"failed to open i2c port for ADC"<<std::endl;
 }
 //std::cout<<"adchan"<<ADChandler<<std::endl;
 
 if(ioctl(Thandler, I2C_SLAVE, THmemdir) < 0){
   std::cout<<"Unable to get bus access to talk to slave H&T"<<std::endl;
 }
 if(ioctl(Thandler2, I2C_SLAVE, TH2memdir) < 0){
   std::cout<<"Unable to get bus access to talk to slave H2&T2"<<std::endl;
 }
 if(ioctl(ADChandler, I2C_SLAVE, ADCmemdir) < 0){
   std::cout<<"Unable to get bus access to talk to slave ADC"<<std::endl;
 }


/////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////
 
 val= i2c_smbus_write_word_data(ADChandler, AD5593R_reg_adc_inp ,0xff00); 
 //std::cout<<"reg adc input "<< std::dec << val <<"   "<< std::hex  <<val<<"    "<< __swab16(val) <<std::endl;
 val = i2c_smbus_read_word_data(ADChandler, AD5593R_reg_adc_inp);
 std::cout<<"reg adc input "<< std::dec << val <<"   "<< std::hex  <<val<<"    "<< __swab16(val) <<std::endl;
 
 val= i2c_smbus_write_word_data(ADChandler,AD5593R_GPCR ,0x0000);
 val = i2c_smbus_read_word_data(ADChandler,  AD5593R_GPCR);
 std::cout << "GPCR "<< std::dec<< val <<"   "<< std::hex <<val<<"    "<< __swab16(val) <<std::endl;

 val= i2c_smbus_write_word_data(ADChandler,AD5593R_REF,0x0002); 
 val = i2c_smbus_read_word_data(ADChandler, AD5593R_REF);
 std::cout<<"ADC ref " << std::dec << val << std::hex <<"   "<< val <<"     "<<__swab16(val)<<std::endl;

}


//////////////////////////////////////////////////
/////////////////////////////////////////////////
  
gpiointerf::~gpiointerf(){
  
     digitalWrite(28,0);//reset ADC
 
}




void gpiointerf::TH(float& tt, float& hh){
  
 if((i2c_smbus_write_quick(Thandler, 0)) != 0){
   std::cout<<"error writing bit to i2c slave"<<std::endl;
 }
 delay(100);

 if(read(Thandler, buff, 4) < 0){
   std::cout<<"unable to read from slave"<<std::endl;
 }
 
 else{
  reading_hum = ( (buff[0] & 63 ) << 8 ) + buff[1];
  humidity = reading_hum / 163.84;
  //std::cout<<"Humidity:  "<<humidity<<" || ";
  reading_temp = (buff[2]<<6) + (buff[3]/4);
  temperature = reading_temp / 99.29 - 40;
  //std::cout<<"Temperature :"<< temperature;
  tt= temperature;
  hh=humidity;
 }

  //return temperature;
}

void gpiointerf::TH2(float& tt, float& hh){
  
 if((i2c_smbus_write_byte(Thandler2, 0xE3)) != 0){
   std::cout<<"error writing bit to i2c temperature2 slave"<<std::endl;
 }
 delay(100);

 if(read(Thandler2, buff, 3) < 0){
   std::cout<<"unable to read from temperature2 slave"<<std::endl;
 }
 
 else{

    reading_temp = (buff[0] * 256) + buff[1]; // combine both bytes into one big integer
    reading_temp = abs(reading_temp); // make it a float 
    temperature = ((reading_temp / 65536.0) * 175.72 ) - 46.85; // formula fr
    //std::cout<<"Temperature :"<< temperature;
    tt= temperature;


   if((i2c_smbus_write_byte(Thandler2, 0xE5)) != 0){
      std::cout<<"error writing bit to i2c humidity2 slave"<<std::endl;
    }
    delay(100);
    if(read(Thandler2, buff, 3) < 0){
   std::cout<<"unable to read from humidity2 slave"<<std::endl;
    }
    reading_hum = (buff[0]  * 256) + buff[1] ; // combine both bytes into one big integer
    reading_hum = abs(reading_hum); // make it a float
    reading_hum = ((reading_hum / 65536.0) * 125 ) - 6; // formula from datasheet
    //to get the compensated humidity; we need to read the temperature
    humidity = ((25 - temperature) * -0.15) + reading_hum;
    hh=humidity;
    
}
  //return temperature;
}



float gpiointerf::Temp(int chn){

  val= i2c_smbus_write_word_data(ADChandler,AD5592R_REG_ADC_SEQ,0x0100<<chn);
  
  //val= i2c_smbus_write_word_data(ADChandler,AD5592R_REG_ADC_SEQ,0x0200);
  
  if (val < 0)    return (float) val;
  
  val = i2c_smbus_read_word_data(ADChandler, AD5593R_MODE_ADC_READBACK);
  
  if (val < 0)    return (float) val;
  
  val =__swab16(val);
  
  //std::cout<<"thermistor "<< chn+1 << " = "<<(float)(val & 0x0fff)<<std::endl;
  
  return ((float)(val & 0x0fff));
  
}








void desconnect(){
  digitalWrite(1,0);
}

    
