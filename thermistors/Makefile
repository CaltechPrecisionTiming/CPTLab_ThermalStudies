#
# Makefile:
#	wiringPi - A "wiring" library for the Raspberry Pi
#	https://projects.drogon.net/wiring-pi
#
#	Copyright (c) 2012-2015 Gordon Henderson
#################################################################################
# This file is part of wiringPi:
#	Wiring Compatable library for the Raspberry Pi
#
#    wiringPi is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    wiringPi is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with wiringPi.  If not, see <http://www.gnu.org/licenses/>.
#################################################################################


#DEBUG	= -g -O0
DEBUG	= -O3
CC	= g++ -std=c++0x
INCLUDE	= -I/usr/local/include
CFLAGS	= $(DEBUG) -Wall $(INCLUDE) -Winline -pipe `mysql_config --libs` `mysql_config --cflags`
LDFLAGS	= -L/usr/local/lib -L/usr/lib/mysqlp 
LDLIBS    = -lwiringPi -lwiringPiDev -lpthread -lm -lmysqlclient

# Should not alter anything below this line
###############################################################################




SRC	=	cratecontrol.cpp gpiointerf.cpp databasectr.cpp configuration.c

OBJ	=	$(SRC:.cpp=.o)

BINS	=	$(SRC:.cpp=)

all: cratecontrol 

#gpiointerf.o: gpiointerf.cpp
#	echo [link]
#	$(CC) -c gpiointerf.cpp $(LDFLAGS) $(LDLIBS)


#cratecontrol.o: cratecontrol.cpp
#	echo [link]
#	$(CC) -c cratecontrol.cpp $(LDFLAGS) $(LDLIBS)

#databasectr.o: databasectr.cpp
#	echo [link]
#	$(CC)  -c  databasectr.cpp $(LDFLAGS) $(LDLIBS)

cratecontrol: cratecontrol.o gpiointerf.o databasectr.o configuration.o
	$(CC) -o $@ $^ $(LDFLAGS) $(LDLIBS)

.c.o:
	$Q echo [CC] $<
	$Q $(CC) -c $(CFLAGS) $< -o $@

#%.o: %.cpp
#	$(CC)  $(LDFLAGS) $(LDLIBS) -c $< -o $@

depend:
	makedepend -Y $(SRC)

# DO NOT DELETE
