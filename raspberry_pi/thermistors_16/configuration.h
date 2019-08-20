#ifndef CONFIGURATION_file
#define CONFIGURATION_file

#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <fstream>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <string.h>
#include <unistd.h>

extern int USB_HV;
extern int USB_ard;
extern int NUM_MOD;
extern int NUM_CHN;
extern char filename[200];


extern char buf[200];
int ReadUntil(int fd, char tok);
int readconfig(char *file);

#endif
