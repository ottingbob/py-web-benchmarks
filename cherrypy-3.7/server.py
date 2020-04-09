import socket
from cheroot import wsgi

from app.main import app

import multiprocessing
import os

workers_per_core_str = os.getenv("WORKERS_PER_CORE", 2)
cores = multiprocessing.cpu_count()
workers_per_core = float(workers_per_core_str)
default_web_concurrency = int(workers_per_core * cores)

print(default_web_concurrency)

server = wsgi.Server(
    bind_addr=('0.0.0.0', 7331),
    wsgi_app=app,
    request_queue_size=500,
    server_name=socket.gethostname(),
    numthreads=default_web_concurrency,
    timeout=15
)

if __name__ == '__main__':
    try:
        server.start()
    except KeyboardInterrupt:
        pass
    finally:
        server.stop()