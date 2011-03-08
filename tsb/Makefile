obj = checkmedia.o tsb.o 
CFLAGS= -std=c99 -g -ggdb -Wall

tsb: $(obj)
	gcc $(CFLAGS) $(obj) -o tsb
checkmedia.o: checkmedia.c checkmedia.h
	gcc $(CFLAGS) -c checkmedia.c 
tsb.o:  tsb.c checkmedia.h
	gcc $(CFLAGS) -c tsb.c 

.PHONY:clean
clean:
	-rm tsb $(obj)
