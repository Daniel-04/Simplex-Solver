all: shared

shared: solver.c
	gcc -fPIC -shared -o libsimplex.so $^

clean:
	rm -f libsimplex.so
