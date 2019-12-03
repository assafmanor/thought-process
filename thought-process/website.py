import functools
import http.server
import re

class Website:

    def __init__(self):
        self.handlers = {} # key = routing path (regex), value = the handler itself


    def route(self, path):
        def decorator(f):
            self.handlers[path] = f
            @functools.wraps(f)
            def wrapper(*args, **kwargs):
                return f(*args, **kwargs)
            return wrapper
        return decorator


    def handler_factory(self, handlers):
            
        # Handler class definition
        class Handler(http.server.BaseHTTPRequestHandler):
            def __init__(self, request, client_address, server):
                self.handlers = handlers
                super().__init__(request, client_address, server)
            
            def do_GET(self):
                for pattern in self.handlers:
                    match = re.fullmatch(pattern, self.path)
                    if match:
                        break
                else: # path did not match any pattern
                    self.__send_404()
                    return
                args = match.groups()
                handler = self.handlers[pattern]
                # call the handler with args as arguments
                status_code, body = handler(*args)
                if status_code == 404:
                    self.__send_404()
                else:
                    self.__show_page(status_code, body.encode())


            def __send_404(self):
                self.send_response(404)
                self.end_headers()

            
            def __show_page(self, status_code, encoded_body):
                self.send_response(status_code)
                self.send_header('Content-Type', 'text/html')
                self.send_header('Content-Length', len(encoded_body))
                self.end_headers()
                self.wfile.write(encoded_body)
                    
        # Handler class definition end

        return Handler


    def run(self, address):
        http_server = http.server.HTTPServer(address, self.handler_factory(self.handlers))
        try:
            http_server.serve_forever()
        except KeyboardInterrupt:
            http_server.server_close()
        return 0
