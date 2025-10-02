from http.server import BaseHTTPRequestHandler
import json
import random
import string


class AuthHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        print(f"do_OPTIONS Request from client IP: {self.client_address[0]}")
        # 200还是204都可以使用，只是204规范一点
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        # Content-Type必须设置允许，否则默认应答text/html
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        print(f"do_POST Request from client IP: {self.client_address[0]}")
        if self.path == '/authsign':
            # 解析请求参数
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length) if content_length > 0 else b'{}'
            try:
                data = json.loads(post_data.decode('utf-8'))
            except json.JSONDecodeError:
                data = {}
            
            # 填充默认随机值
            if 'signData' not in data:
                data['signData'] = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            if 'key' not in data:
                data['key'] = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            
            # 连接字符串并返回
            result = data['signData'] + '+' + data['key']
            response_data = {'result': result}
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')
