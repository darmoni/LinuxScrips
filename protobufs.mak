

CXX = g++
CC = gcc
LD = g++

CXXFLAGS = -Wall $(PTHREAD_CFLAGS) -std=gnu++11
LDFLAGS =
#LDLIBS = -lsock32

.cc.o:
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c $<
.c.o:
	$(CC) $(CPPFLAGS) $(CFLAGS) -c $<

SRC_DIR=/home/nir/VirtualProjects/venv_bin_p3/local_bin
DST_DIR=/home/nir/VirtualProjects/venv_bin_p3/local_bin

$(DST_DIR)/addressbook_pb2.py: $(SRC_DIR)/addressbook.proto
	protoc -I=$(SRC_DIR) --python_out=$(DST_DIR) $(SRC_DIR)/addressbook.proto


$(DST_DIR)/addressbook3_pb2.py: $(SRC_DIR)/addressbook3.proto
	protoc -I=$(SRC_DIR) --python_out=$(DST_DIR) $(SRC_DIR)/addressbook3.proto

all: $(DST_DIR)/addressbook_pb2.py $(DST_DIR)/addressbook3_pb2.py $(DST_DIR)/ACD_pb2.py

$(DST_DIR)/ACD_pb2.py: $(SRC_DIR)/ACD.proto
	protoc -I=$(SRC_DIR) --python_out=$(DST_DIR) $<
