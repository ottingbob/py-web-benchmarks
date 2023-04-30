##### cherrypy-3.7 benchmark

`echo 'GET http://localhost:7331/' | vegeta attack -duration=10s -workers=10 -rate=2500/s | tee results.bin | vegeta report`

Requests      [total, rate, throughput]         25000, 2500.14, 1092.64
Duration      [total, attack, wait]             18.024s, 9.999s, 8.025s
Latencies     [min, mean, 50, 90, 95, 99, max]  27.436µs, 440.431ms, 7.093ms, 1.484s, 2.509s, 7.251s, 15.548s
Bytes In      [total, mean]                     236328, 9.45
Bytes Out     [total, mean]                     0, 0.00
Success       [ratio]                           78.78%
Status Codes  [code:count]                      0:5306  200:19694  
Error Set:
Get "http://localhost:7331/": dial tcp 0.0.0.0:0->127.0.0.1:7331: socket: too many open files
