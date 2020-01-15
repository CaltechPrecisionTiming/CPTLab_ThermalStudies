#include <stdio.h>
#include <signal.h>
#include <unistd.h>
#include <cmath>
#include <stdlib.h>
#include <stdbool.h>
#include <fstream>
#include "gpiointerf.h"
#include "databasectr.h"
#include "configuration.h"

using namespace std;

#define NumTerm 8


databasectr *db; //objeto para el uso de SQL

gpiointerf *rp1; // objeto para el uso de wiring pi

float TT;
float HH;
float TT2;
float HH2;

 bool tempflag= false;
 //float temp;
 float temp[NumTerm];
 
//para el uso de ctl+C (salida elegante)
void sig_handler (int signo){
  if(signo == SIGINT) {
    std::cout<<"\Stopping data acquistion\n "<<std::endl;
    //delete db;
    delete rp1;
    exit(EXIT_SUCCESS);
  }
}

//alarma para sensar la temperatura
void handle_alarm(int sig){
  tempflag= true;

}

double adc2R(double c, double R=19e3, double Vref=2.5) {
  double V = c*Vref/4096;
  return V*R/(Vref-V);
}

double R2T(double R, double beta=3892.0, double T0=25.0, double R0=5e3) {
  T0 += 273.15;
  double r_inf = R0*exp(-beta/T0);
  double T = beta/log(R/r_inf);
  return T - 273.15;
}

double adc2T(double c) {
  return R2T(adc2R(c));
}


int main (void)
{
  std::cout<<"BTL CIT temperature and humidity monitoring system"<<std::endl;
  sleep(5);
  db= new databasectr(NumTerm);
  rp1= new gpiointerf();
  rp1->initialize();
  signal(SIGINT, sig_handler);
  
  signal(SIGALRM, handle_alarm);
  
  alarm(1); //cada cuanto tiempo sensa la temperatura y la humedad

  if(readconfig("config.conf")){
    std::cout<<"error al leer archivo de configuracion"<<std::endl;
  }
  //std::ofstream calibration;
  //calibration.open("test.txt", std::ios::out | std::ios::trunc);
  int cycles_till_init = 0;
  bool flag = true;
  while(1){
    
    sleep(5);
    if (cycles_till_init > 3){
      cycles_till_init = 0;
      rp1->initialize();
      std::cout<<"rp1 reinitialized"<<std::endl;
    }
    for(int i=0; i<NumTerm; i++){
      temp[i]=rp1->Temp(i);
      printf("%d: %.2f (%.0f) | ", i, adc2T(temp[i]), temp[i]);
    }
    for(int i=0; i<NumTerm-1; i++){
      if (temp[i] != temp[i+1]){
        flag = false;
      }
      else flag=true;
    }
    
    //std::cout<<"flag is "<<flag<<std::endl;
    if(flag){
      cycles_till_init++;
    }
    rp1->TH(TT, HH);
    //rp1->TH2(TT2,HH2);
    printf("Amb T: %.2f ||Amb Hum: %.1f", TT, HH);
    //std::cout<<"Temperature_ex = "<<TT2<<"|| Humidity_ex = "<<HH2;
    cout << endl;

    //db->setDat(temp,TT, HH,TT2,HH2);
    db->setDat(temp,TT, HH,00,00);
    //calibration << temp[0] <<std::endl;
  }
 //calibration.close();
return 0;
}

