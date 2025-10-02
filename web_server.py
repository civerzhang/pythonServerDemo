from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import ssl

# 设置工作目录为html文件夹
os.chdir(os.path.join(os.path.dirname(__file__), 'html'))

PORT = 8088
server_address = ('', PORT)
httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)

# 配置 HTTPS
# certfile = 'localhost.pem'
# keyfile = 'localhost.key'
# httpd.socket = ssl.wrap_socket(httpd.socket, certfile=certfile, keyfile=keyfile, server_side=True)

print(f"HTTPS server started on port {PORT}")
httpd.serve_forever()
