#include <stdio.h>
#include <signal.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdbool.h>
#include <fstream>
#include "gpiointerf.h"
#include "databasectr.h"
#include "configuration.h"



#define NumTerm 8
#define NumADC 2
#define NumChn 16


databasectr *db; //objeto para el uso de SQL

gpiointerf *rp1; // objeto para el uso de wiring pi

float TT, HH;
float TT2, HH2;
float TT_HIH6130, HH_HIH6130;
float TT_Si7021, HH_Si7021; 

 bool tempflag= false;
 //float temp;

float temp[NumChn];
 
//para el uso de ctl+C (salida elegante)
void sig_handler (int signo){
  if(signo == SIGINT) {
    std::cout<<"\n good bye \n "<<std::endl;
    //delete db;
    delete rp1;
    exit(EXIT_SUCCESS);
  }
}





int main (void)
{
  std::cout<<"BTL CIT temperature and humidity monitoring system"<<std::endl;
  sleep(5);
  db= new databasectr(NumChn);
  rp1= new gpiointerf(NumADC);
  for (int n=0; n<NumADC; n++) rp1->initialize(n+1);
  signal(SIGINT, sig_handler);
  
  
  if(readconfig("config.conf")){
    std::cout<<"error al leer archivo de configuracion"<<std::endl;
  }
  
  bool flag = true;
  while(1){
    sleep(1);
    flag = true;
    for (int n=0; n<NumADC; n++){
      rp1->activate(n+1);
      for(int i=0; i<NumTerm; i++){
        int j = n*NumTerm + i;
        temp[j]=rp1->Temp(i);
        std::cout<<"temp"<< n*NumTerm + i<<" = "<<temp[j]<< "||";
      }
      for(int i=0; i<NumTerm; i++){
        int j = n*NumTerm + i; 
        if (temp[j] != temp[j+1]) flag = false;
      }
      if(flag == true){
        rp1->initialize(n+1);
        std::cout<<"ADC"<<n<<"reinitialized"<<std::endl;
      }
    }
    
    // Readout of temperature and humidity 
    rp1->TH(TT, HH);
    //rp1->TH2(TT2,HH2);
    rp1->TH_HIH6130(TT_HIH6130,HH_HIH6130);
    rp1->TH_Si7021(TT_Si7021,HH_Si7021); 
    
    std::cout<<"Temperature_in_1 = "<<TT<<"|| Humidity_in_1 = "<<HH<<" ||";
    //std::cout<<"Temperature_ex = "<<TT2<<"|| Humidity_ex = "<<HH2;
    std::cout<<"Temperature_HIH6130 = "<<TT_HIH6130<<"|| Humidity_HIH6130 = "<<HH_HIH6130<<" ||";
    std::cout<<"Temperature_Si7021 = "<<TT_Si7021<<"|| Humidity_Si7021 = "<<HH_Si7021<<" ||";
    std::cout<<std::endl;

    db->setDat(temp,TT, HH,TT_HIH6130,HH_HIH6130,TT_Si7021,HH_Si7021);
    //db->setDat(temp,00, 00,00,00);
  }
return 0;
}

