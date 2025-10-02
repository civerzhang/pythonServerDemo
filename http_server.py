from http.server import HTTPServer
from auth_handler import AuthHandler
import ssl

PORT = 30002
server_address = ('', PORT)
httpd = HTTPServer(server_address, AuthHandler)

# 配置 HTTPS
# certfile = 'localhost.pem'
# keyfile = 'localhost.key'
# httpd.socket = ssl.wrap_socket(httpd.socket, certfile=certfile, keyfile=keyfile, server_side=True)

print(f"HTTPS server started on port {PORT}")
httpd.serve_forever()
