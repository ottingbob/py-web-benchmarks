# Python benchmarks 🐍

The purpose of this project is to benchmark the findings of the different WSGI / ASGI python server & framework combinations available at this time. Its difficult to actually have a `best` implementation since there are so many permutations available with linux distos in docker, wsgi servers, and the server frameworks. For the sake of this benchmark I have tried to scope it to number of requests. The details are shown below (this is the same as benchmark-report.md).

uvicorn-3.7 Dockerfile source:
https://github.com/tiangolo/uvicorn-gunicorn-docker/blob/master/python3.7-alpine3.8/Dockerfile

## Python Benchmark Results

### Specs

Kernel: 5.3.1-arch1-1-ARCH
CPU: Intel i7-4710HQ (8) @ 3.500GHz 
Memory: 15.936 GiB

Benchmarked with the vegeta Golang HTTP Benchmarking library
https://github.com/tsenart/vegeta


###
### results from bjoern-3.7 benchmark
### 

`echo "GET http://localhost:7331/" | vegeta attack -duration=10s -workers=200 -rate=20000/s | tee results.bin | vegeta report`

Requests      [total, rate, throughput]         200000, 19999.53, 15080.74
Duration      [total, attack, wait]             10.034s, 10s, 33.361ms
Latencies     [min, mean, 50, 90, 95, 99, max]  57.229µs, 50.745ms, 61.509ms, 72.15ms, 78.203ms, 114.32ms, 3.069s
Bytes In      [total, mean]                     4085478, 20.43
Bytes Out     [total, mean]                     0, 0.00
Success       [ratio]                           75.66%
Status Codes  [code:count]                      0:48686  200:151314  
Error Set:
Get http://localhost:7331/: dial tcp 0.0.0.0:0->[::1]:7331: socket: too many open files


###
### results from bjoern-hug-3.7 benchmark
###

`echo "GET http://localhost:7331/" | vegeta attack -duration=10s -workers=100 -rate=10000/s | tee results.bin | vegeta report`

Requests      [total, rate, throughput]         99996, 9999.37, 6622.16
Duration      [total, attack, wait]             11.289s, 10s, 1.289s
Latencies     [min, mean, 50, 90, 95, 99, max]  67.869µs, 102.505ms, 74.284ms, 89.883ms, 91.877ms, 120.32ms, 11.168s
Bytes In      [total, mean]                     2467014, 24.67
Bytes Out     [total, mean]                     0, 0.00
Success       [ratio]                           74.76%
Status Codes  [code:count]                      0:25238  200:74758  
Error Set:
Get http://localhost:7331/v1/: dial tcp 0.0.0.0:0->[::1]:7331: socket: too many open files


###
### results from cherrypy-3.7 benchmark
###

`echo "GET http://localhost:7331/" | vegeta attack -duration=10s -workers=30 -rate=2000/s | tee results.bin | vegeta report`

Requests      [total, rate, throughput]         20000, 2000.11, 837.89
Duration      [total, attack, wait]             17.741s, 9.999s, 7.742s
Latencies     [min, mean, 50, 90, 95, 99, max]  99.482µs, 576.594ms, 9.274ms, 1.018s, 3.068s, 15.056s, 15.43s
Bytes In      [total, mean]                     386490, 19.32
Bytes Out     [total, mean]                     0, 0.00
Success       [ratio]                           74.33%
Status Codes  [code:count]                      0:5135  200:14865  
Error Set:
Get http://localhost:7331/: dial tcp 0.0.0.0:0->[::1]:7331: socket: too many open files


###
### results from gunicorn-3.7 benchmark
###

`echo "GET http://localhost:7331/" | vegeta attack -duration=10s -workers=200 -rate=20000/s | tee results.bin | vegeta report`

Requests      [total, rate, throughput]         192298, 19184.70, 1356.30
Duration      [total, attack, wait]             19.496s, 10.024s, 9.472s
Latencies     [min, mean, 50, 90, 95, 99, max]  85.102µs, 570.029ms, 356.393ms, 1.513s, 1.64s, 2.649s, 15.985s
Bytes In      [total, mean]                     211536, 1.10
Bytes Out     [total, mean]                     0, 0.00
Success       [ratio]                           13.75%
Status Codes  [code:count]                      0:165856  200:26442  
Error Set:
Get http://localhost:7331/: dial tcp 0.0.0.0:0->[::1]:7331: socket: too many open files
Get http://localhost:7331/: dial tcp 0.0.0.0:0->127.0.0.1:7331: socket: too many open files

`echo "GET http://localhost:7331/" | vegeta attack -duration=10s -workers=50 -rate=5000/s | tee results.bin | vegeta report`

Requests      [total, rate, throughput]         49999, 4998.69, 2316.89
Duration      [total, attack, wait]             15.85s, 10.002s, 5.848s
Latencies     [min, mean, 50, 90, 95, 99, max]  111.587µs, 215.354ms, 38.425ms, 1.037s, 1.074s, 3.192s, 15.383s
Bytes In      [total, mean]                     293784, 5.88
Bytes Out     [total, mean]                     0, 0.00
Success       [ratio]                           73.45%
Status Codes  [code:count]                      0:13276  200:36723  
Error Set:
Get http://localhost:7331/: dial tcp 0.0.0.0:0->[::1]:7331: socket: too many open files
Get http://localhost:7331/: dial tcp 0.0.0.0:0->127.0.0.1:7331: socket: too many open files

###
### results from uvicorn-3.7 benchmark
###

`echo "GET http://localhost:7331/" | vegeta attack -duration=10s -workers=100 -rate=10000/s | tee results.bin | vegeta report`

Requests      [total, rate, throughput]         99910, 9983.42, 7371.08
Duration      [total, attack, wait]             10.071s, 10.008s, 63.528ms
Latencies     [min, mean, 50, 90, 95, 99, max]  96.873µs, 106.155ms, 108.067ms, 207.078ms, 247.417ms, 307.98ms, 529.061ms
Bytes In      [total, mean]                     1261995, 12.63
Bytes Out     [total, mean]                     0, 0.00
Success       [ratio]                           74.30%
Status Codes  [code:count]                      0:25675  200:74235  
Error Set:
Get http://localhost:7331/: dial tcp 0.0.0.0:0->[::1]:7331: socket: too many open files
