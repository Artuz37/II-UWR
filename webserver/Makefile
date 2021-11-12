ROOT = sudo
CC = g++
FLAGS = -std=c++17 -Wall -Wextra

main: main.o TCP.o
	$(ROOT) $(CC) $(FLAGS)  TCP.o  main.o -o webserver

main.o: main.cpp
	$(ROOT) $(CC) -c $(FLAGS) main.cpp -o main.o

TCP.o: TCP.cpp
	$(ROOT) $(CC) -c $(FLAGS) TCP.cpp -o TCP.o

clean:
	sudo rm -f *.o

distclean:
	sudo rm -f webserver
	sudo rm -f *.o


all : main