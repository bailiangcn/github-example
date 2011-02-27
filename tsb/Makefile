tsb: checkmedia.o tsb.o
	gcc -std=c99 tsb.o checkmedia.o -o tsb
checkmedia.o: checkmedia.c checkmedia.h
	gcc -std=c99 -c checkmedia.c 
tsb.o: tsb.c checkmedia.h
	gcc -std=c99 -c tsb.c 

clean:
	-rm tsb *.o
.PHONY:clean
