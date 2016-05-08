build ftools.so

on mac:
gcc -dynamiclib -I /usr/include/python2.7/ -l python2.7 -o ftools.dylib ftools.c
mv ftools.dylib ftools.so

on linux:
gcc -shared -I /usr/include/python2.7/ -l python2.7 -o ftools.so ftools.c

