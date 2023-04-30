##### gunicorn-3.7 benchmark

`echo 'GET http://localhost:7331/' | vegeta attack -duration=10s -workers=10 -rate=2500/s | tee results.bin | vegeta report`

Requests      [total, rate, throughput]         25000, 2500.14, 2499.21
Duration      [total, attack, wait]             10.003s, 9.999s, 3.736ms
Latencies     [min, mean, 50, 90, 95, 99, max]  563.135µs, 4.519ms, 3.437ms, 6.136ms, 7.494ms, 53.812ms, 160.226ms
Bytes In      [total, mean]                     200000, 8.00
Bytes Out     [total, mean]                     0, 0.00
Success       [ratio]                           100.00%
Status Codes  [code:count]                      200:25000  
Error Set:
