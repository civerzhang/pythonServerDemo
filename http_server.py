from http.server import HTTPServer
from auth_handler import AuthHandler
import ssl

PORT = 30002
server_address = ('', PORT)
httpd = HTTPServer(server_address, AuthHandler)

# 配置 HTTPS
certfile = 'C:\\Users\\arnoz\\IdeaProjects\\untitled\\localhost.pem'
keyfile = 'C:\\Users\\arnoz\\IdeaProjects\\untitled\\localhost.key'
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile=certfile, keyfile=keyfile)
httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

print(f"HTTPS server started on port {PORT}")
httpd.serve_forever()
