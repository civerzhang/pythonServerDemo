from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import ssl

# 设置工作目录为html文件夹
os.chdir(os.path.join(os.path.dirname(__file__), 'html'))

PORT = 8088
server_address = ('', PORT)
httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)

# 配置 HTTPS
certfile = 'C:\\Users\\arnoz\\IdeaProjects\\untitled\\localhost.pem'
keyfile = 'C:\\Users\\arnoz\\IdeaProjects\\untitled\\localhost.key'
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile=certfile, keyfile=keyfile)
httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

print(f"HTTPS server started on port {PORT}")
httpd.serve_forever()
