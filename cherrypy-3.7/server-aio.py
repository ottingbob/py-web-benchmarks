from cheroot import wsgi

def app(environ, start_response):
  status = '200 OK'
  response_headers = [('Content-Type', 'text/plain')]
  start_response(status, response_headers)
  return [b'Hello world!']

server = wsgi.Server(
    bind_addr=('0.0.0.0', 7331),
    wsgi_app=app,
    request_queue_size=500,
    timeout=15
)

if __name__ == '__main__':
    try:
        server.start()
    except KeyboardInterrupt:
        pass
    finally:
        server.stop()