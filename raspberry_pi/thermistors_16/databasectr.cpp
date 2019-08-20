#include "databasectr.h"


databasectr::databasectr(int NT):nt(NT){

  this->DBconfig();
}


databasectr::~databasectr(){
  this->mysql_disconnect();
  //delete mysql1;
  //delete value_int;
  //delete ch_enable;
  //std::cout<<"cacaca"<<std::endl;
}



int databasectr::DBconfig(){

  mysql1 = mysql_init(NULL);
  if(mysql1 == NULL){
    return 0;
  }
  //connect to the database
  if(mysql_real_connect(mysql1, DATABASE_IP, DATABASE_USERNAME, DATABASE_PASSWORD, DATABASE_NAME , 0, NULL, 0) == NULL){
    fprintf(stderr, "%s\n", mysql_error(mysql1));
  }
  else{
    printf("database connection successful.\n");  
    return 1;
  }

  
}



void databasectr::mysql_disconnect (void){
  mysql_close(mysql1);
  printf("disconnected from database.\n");
}



int databasectr::setDat(float * ther, float TT, float HH,float TT_HIH6130, float HH_HIH6130, float TT_Si7021, float HH_Si7021){
  

  std::ostringstream TTs;
  std::ostringstream HHs;
  std::ostringstream TTs_HIH6130;
  std::ostringstream HHs_HIH6130;
  std::ostringstream TTs_Si7021;
  std::ostringstream HHs_Si7021;
  std::ostringstream Ths[nt];
  std::ostringstream ThVals[nt];
  TTs<<TT;
  HHs<<HH;
  TTs_HIH6130<<TT_HIH6130;
  HHs_HIH6130<<HH_HIH6130;
  TTs_Si7021<<TT_Si7021;
  HHs_Si7021<<HH_Si7021;
  std::string comand;
  
  comand =  "INSERT INTO ";
  comand += TABLE_NAME;
  comand += " (";
  for(int i=0; i<nt ;i++){
    
   Ths[i]<<i;
   comand += "temp"+Ths[i].str()+", ";
  }
  
  
  //comand= "UPDATE 16chanboard SET Vmon = " + Vms.str() + " where id = " + mods.str() +"0"+ chns.str() + ";";
 comand += "Humidity_in, Temp_in, Humidity_HIH6130, Temp_HIH6130, Humidity_Si7021, Temp_Si7021, datetime) VALUES (";
   
   for(int i=0; i<nt ;i++){
      
     ThVals[i]<<ther[i];
      
    //std::cout<<Ths[i].str()<<std::endl;
  
    
     comand += ThVals[i].str()+", ";
    }
   
    comand += HHs.str() + ", " + TTs.str() + ", " + HHs_HIH6130.str() + ", " + TTs_HIH6130.str() + ", " + HHs_Si7021.str() + ", " + TTs_Si7021.str() + ", NOW());";
    
  const char *comandC = comand.c_str();

 
 
     //vector times;   //a vector of alarm times

    if(mysql1 != NULL)
      {
	//Retrieve all data from alarm_times
	if (mysql_query(mysql1, comandC))

	  {
	    fprintf(stderr, "%s\n", mysql_error(mysql1));
	    return -1;
	  }
      }
    
 return 0;  
}


int databasectr::setIm(int mod, int chn, float Im){

  std::ostringstream mods;
  std::ostringstream chns;
  std::ostringstream Ims;
  Ims<<Im;
  mods<<mod;
  chns<<chn;
  std::string comand;
  
  comand= "UPDATE Preshower_PS_v1 SET Imon = " + Ims.str() + " where id = " + mods.str() +"0"+ chns.str() + ";";
    
  const char *comandC = comand.c_str();

 
 
     //vector times;   //a vector of alarm times

    if(mysql1 != NULL)
      {
	//Retrieve all data from alarm_times
	if (mysql_query(mysql1, comandC))

	  {
	    fprintf(stderr, "%s\n", mysql_error(mysql1));
	    return -1;
	  }
      }
    
 return 0;
}
int databasectr::setT(float Tm){
  nt++;
  std::ostringstream Tms;
  Tms<<Tm;
  std::ostringstream nts;
  nts<<nt;
  std::string comand;
  
  comand= "UPDATE temperature SET temperature.Tmon=" + Tms.str() + "where Preshower_PS_v1.id="+nts.str()+ ";";
    
  const char *comandC = comand.c_str();

  char *value_int;
 
     //vector times;   //a vector of alarm times

    if(mysql1 != NULL)
      {
	//Retrieve all data from alarm_times
	if (mysql_query(mysql1, comandC))

	  {
	    fprintf(stderr, "%s\n", mysql_error(mysql1));
	    return 0;
	  }
      }
    
 return 1;
}


