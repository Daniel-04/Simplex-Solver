The parser tolerates a very loose LP file format:
``` shell
$ make
gcc -fPIC -shared -o libsimplex.so solver.c

$ cat examples/format.lp
mIniMizE x  -50y + 7  zeta
subject to
x + 3y <= 10
zeta - 4y =    5
x + zeta  -  y >= 1

$ python example.py examples/format.lp
c=[-1, 50, -7]
A=
-1 1 -1
0 -4 1
0 4 -1
1 3 0
b=[-1, 5, -5, 10]
Optimal Solution:
x[1] = 0.000000
x[2] = 3.333333
x[3] = 18.333333
Optimal Value: 38.333333

$ cat examples/brewery.lp
Maximise 13Ale + 23Lager
Subject to:
	5Ale + 15Lager <= 480
	4Ale + 4Lager <= 160
	35Ale + 20Lager <= 1190

$ python example.py examples/brewery.lp
c=[13, 23]
A=
35 20
4 4
5 15
b=[1190, 160, 480]
Optimal Solution:
x[1] = 12.000000
x[2] = 28.000000
Optimal Value: 800.000000
```
