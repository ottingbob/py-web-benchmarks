##### bjoern-3.7 benchmark

`echo 'GET http://localhost:7331/' | vegeta attack -duration=10s -workers=10 -rate=2500/s | tee results.bin | vegeta report`

Requests      [total, rate, throughput]         25000, 2500.08, 2500.05
Duration      [total, attack, wait]             10s, 10s, 143.489µs
Latencies     [min, mean, 50, 90, 95, 99, max]  92.528µs, 1.739ms, 165.896µs, 245.504µs, 285.568µs, 71.213ms, 151.986ms
Bytes In      [total, mean]                     675000, 27.00
Bytes Out     [total, mean]                     0, 0.00
Success       [ratio]                           100.00%
Status Codes  [code:count]                      200:25000  
Error Set:
