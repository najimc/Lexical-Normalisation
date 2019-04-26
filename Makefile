CC = gcc
CFLAGS = -fPIC -shared -Wall
TARGET_LIB = lib.so
SRC = algorithms.c

default: $(SRC)
	$(CC) $(CFLAGS) -o $(TARGET_LIB) $(SRC)

clean:
	-rm -f $(TARGET_LIB)
