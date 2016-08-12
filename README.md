# OS metrics reporter

### Description
Collects OS metrics and reports measurement to Riemann server.

### Installation
At this point no package or installer is provided. Simply clone git repository or download package of master branch and unpack. Install dependencies using pip
```
pip install -r requirements.txt
```
and run with parameters
```
python start.py -h $RIEMANN_HOST
```
This command starts the reporter and keeps sending metrics until stopped.

### Execution parameters
There are several execution parameters that can be provided to the start script:
```
-h riemann host (127.0.0.1 default)
-p riemann port (5555 default)
-i measurement and reporting period in SECONDS (1 default)
-d debug flag (logs at DEBUG level)
```

### Reconnection mechanism
Basic reconnection mechanism is implemented keeping reporter up and running even if riemann server is down. When connection can be established again it will reconnect. All measurements collected in the meantime is discarded.

<!-- ### Ftools package (WIP)
Ftools is a fincore wrapper that provides information on percentage of a file being cached.

#### Building ftools
On osx:
```
gcc -dynamiclib -I /usr/include/python2.7/ -l python2.7 -o ftools.dylib ftools.c
mv ftools.dylib ftools.so
```

On linux:
```
gcc -shared -I /usr/include/python2.7/ -l python2.7 -o ftools.so ftools.c
```
#### Future plans
Enable reporting of files cached through riemann -->
