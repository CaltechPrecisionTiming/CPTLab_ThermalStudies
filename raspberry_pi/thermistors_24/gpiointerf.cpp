
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

gpiointerf::gpiointerf(int dev){
  for(int i = 0; i++; i<4)buff[i]=0x00;
  wiringPiSetup();

  pinMode(21, OUTPUT);  // /RST first ADC
  digitalWrite(21,1);
  
  pinMode(29, OUTPUT);  // RST first ADC
  digitalWrite(29,1);//
  
   pinMode(28, OUTPUT);  // /RST first ADC
  digitalWrite(28,1);
  
  pinMode(27, OUTPUT);  // RST first ADC
  digitalWrite(27,0);// !!!!!!! CHANGE IF YOU WANT TO USE THE 4TH!!!!
  
  pinMode(22, OUTPUT);
  pinMode(23, OUTPUT);
  pinMode(24, OUTPUT);
  pinMode(25, OUTPUT);
  

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
  THmemdir_HIH6130 = 0x27;
  THmemdir_Si7021 = 0x40;
  ADCmemdir = 0x10;
  val=666;
  for (int i=0;i<dev;i++) initialize(i);
}
void gpiointerf::initialize(int dev){
 activate(dev+1);
 std::cout<<"activated ADC "<<dev+1<<std::endl;
 if((Thandler = open(filename, O_RDWR)) < 0){
   std::cout<<"failed to open i2c port for T&H"<<std::endl;
 }
 if((Thandler2 = open(filename, O_RDWR)) < 0){
   std::cout<<"failed to open i2c port for T2&H2"<<std::endl;
 }
  if((Thandler_HIH6130 = open(filename, O_RDWR)) < 0){
   std::cout<<"failed to open i2c port for T_HIH6130&H_HIH6130"<<std::endl;
 }
  if((Thandler_Si7021 = open(filename, O_RDWR)) < 0){
   std::cout<<"failed to open i2c port for T_Si7021&H_Si7021"<<std::endl;
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
  if(ioctl(Thandler_HIH6130, I2C_SLAVE, THmemdir_HIH6130) < 0){
   std::cout<<"Unable to get bus access to talk to slave T_HIH6130&H_HIH6130"<<std::endl;
 }
  if(ioctl(Thandler_Si7021, I2C_SLAVE, THmemdir_Si7021) < 0){
   std::cout<<"Unable to get bus access to talk to slave T_Si7021&H_Si7021"<<std::endl;
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

void gpiointerf::TH_HIH6130(float& tt, float& hh){
  if((i2c_smbus_write_quick(Thandler_HIH6130, 0)) != 0){
    std::cout<<"error writing bit to HIH6130 slave"<<std::endl;
 }
 delay(100);

 if(read(Thandler_HIH6130, buff, 4) < 0){
   std::cout<<"unable to read from HIH6130 slave"<<std::endl;
 }
 
 else{
  // Send humidity measurement command(0xF5)
	//sleep(1);
  // Read 2 bytes of humidity data
  // Convert the first two digits (humidity), do not use first 2 bits
  humidity = ((((buff[0] & 0x3F) * 256) + buff[1]) * 100.0) / 16383.0;;
	//write(Thandler_Si7021, config, 1);
  // Read 2 bytes of temperature data
  // Convert the second two digits (temperature), do not use last 2 bits
  float temp = (((buff[2] & 0xFF) * 256) + (buff[3] & 0xFC)) / 4;
  temperature = (temp / 16384.0) * 165.0 - 40.0;
  //std::cout<<"Humidity:  "<<humidity<<" || ";
  //std::cout<<"Temperature :"<< temperature;
  tt= temperature;
  hh=humidity;
 }
}

void gpiointerf::TH_Si7021(float& tt, float& hh){
  
 if((i2c_smbus_write_quick(Thandler_Si7021, 0)) != 0){
   std::cout<<"error writing bit to Si7021 slave"<<std::endl;
 }
 delay(100);

	// Send humidity measurement command(0xF5)
	char config[1] = {0xF5};
	write(Thandler_Si7021, config, 1);
	sleep(1);

	// Read 2 bytes of humidity data
	// humidity msb, humidity lsb
	if(read(Thandler_Si7021, buff, 2) != 2)
	{
		printf("Error : unable to read humidity from Si  7021 slave\n");
	}
	else
	{
		// Convert the data
		humidity = (((buff[0] * 256 + buff[1]) * 125.0) / 65536.0) - 6;
	}

	// Send temperature measurement command(0xF3)
	config[0] = 0xF3;
	write(Thandler_Si7021, config, 1); 
	sleep(1);

	// Read 2 bytes of temperature data
	// temp msb, temp lsb
	if(read(Thandler_Si7021, buff, 2) != 2)
	{
		printf("Error :unable to read temperature from Si  7021 slave \n");
	}
	else
	{
		// Convert the data
		temperature = (((buff[0] * 256 + buff[1]) * 175.72) / 65536.0) - 46.85;
		 
	}
 
  tt= temperature;
  hh=humidity;
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

void gpiointerf::activate(int adc_num){
  
  //std::cout<<std::endl<<std::endl<<"Activating!!   "<<adc_num<<std::endl<<std::endl;
  if (adc_num == 1){
    digitalWrite(25,0);
    digitalWrite(24,1);
    digitalWrite(23,1);
    digitalWrite(22,1);
  } 
  if (adc_num == 2){
    digitalWrite(25,1);
    digitalWrite(24,0);
    digitalWrite(23,1);
    digitalWrite(22,1);
  }
  if (adc_num == 3){
    digitalWrite(25,1);
    digitalWrite(24,1);
    digitalWrite(23,0);
    digitalWrite(22,1);
  }
  if (adc_num == 4){
    digitalWrite(25,1);
    digitalWrite(24,1);
    digitalWrite(23,1);
    digitalWrite(22,0);
  }
}

void desconnect(){
  digitalWrite(1,0);
}

    
