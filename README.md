build ftools.so

on mac:
gcc -dynamiclib -I /usr/include/python2.7/ -l python2.7 -o ftools.dylib ftools.c
mv ftools.dylib ftools.so

on linux:
gcc -shared -I /usr/include/python2.7/ -l python2.7 -o ftools.so ftools.c

how to run:

clone repository and execute
python start.py

command line parameters:
-h riemann host
-p riemann port
-i interval for sending in seconds

at this point it runs in a while loop. this should be improved in a future version.
