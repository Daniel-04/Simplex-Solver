all: example
	./example

example: example.c solver.c
	gcc -o example $^

clean: example
	rm -f $^
