##### uvicorn-3.7 benchmark

`echo 'GET http://localhost:7331/' | vegeta attack -duration=20s -workers=10 -rate=5000/s | tee results.bin | vegeta report`

	Requests      [total, rate, throughput]         100000, 5000.04, 1159.34
	Duration      [total, attack, wait]             25.918s, 20s, 5.918s
	Latencies     [min, mean, 50, 90, 95, 99, max]  20.7µs, 2.706s, 44.967µs, 19.266s, 22.287s, 25.084s, 25.891s
	Bytes In      [total, mean]                     510816, 5.11
	Bytes Out     [total, mean]                     0, 0.00
	Success       [ratio]                           30.05%
	Status Codes  [code:count]                      0:69952  200:30048  
	Error Set:
	Get "http://localhost:7331/": dial tcp 0.0.0.0:0->127.0.0.1:7331: socket: too many open files
	