#include /home/nir/bin/c-ares/test/Makefile

CXX = g++
CC = gcc
LD = g++

ARES_SRC_DIR=/home/nir/bin/c-ares
# Where to find the built c-ares static library
ARES_BLD_DIR = /home/nir/lib/
ARESLIB = $(ARES_BLD_DIR)/libcares.a
CPPFLAGS = -I$(ARES_SRC_DIR) -DCARES_STATICLIB
CXXFLAGS = -Wall $(PTHREAD_CFLAGS) -std=gnu++11
LDFLAGS =
#LDLIBS = -lsock32


c-ares_example: c-ares_example.o
	$(LD) $(LDFLAGS) -o $@ $^  -L$(ARES_BLD_DIR) -lcares $(LDLIBS)


.cc.o:
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c $<
.c.o:
	$(CC) $(CPPFLAGS) $(CFLAGS) -c $<

clean:
	$(RM) $(OBJS) c-ares_example.o c-ares_example
