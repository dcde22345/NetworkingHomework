# 蔡世玄 113356043 資管碩一
import socket
import threading

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Q1 running on 8888 port
pars = ('127.0.0.1', 8888)
s.bind(pars)
s.listen(5)

def response_html():
    good_html = '<html><head><link href="style.css" rel="stylesheet" type="text/css"></head><body>good</body></html>'
    
    # HTTP 200 OK response header
    headers = "HTTP/1.1 200 OK\r\n"
    headers += "Content-Type: text/html\r\n"
    headers += f"Content-Length: {len(good_html)}\r\n"
    headers += "\r\n"
    return headers + good_html

def response_css():
    css_content = "Body {color: red;}"
    
    # HTTP 200 OK response header
    headers = "HTTP/1.1 200 OK\r\n"
    headers += "Content-Type: text/css\r\n"
    headers += f"Content-Length: {len(css_content)}\r\n"
    headers += "\r\n"
    
    # 返回完整的 HTTP 响应
    return headers + css_content

def response_redirect():
    # HTTP 301 Moved Permanently 响应头
    headers = "HTTP/1.1 301 Moved Permanently\r\n"
    headers += "Location: /good.html\r\n"
    headers += "Content-Type: text/html\r\n"
    headers += "Content-Length: 0\r\n"
    headers += "\r\n"
    
    # 返回完整的 HTTP 响应
    return headers

def response_not_found():
    # HTTP 404 Not Found 响应头
    headers = "HTTP/1.1 404 Not Found\r\n"
    headers += "Content-Type: text/html\r\n"
    headers += "Content-Length: 0\r\n"  # 没有附加内容
    headers += "\r\n"
    
    # 返回完整的 HTTP 响应
    return headers


def serveClient(clientsocket, address):
    # Q2. count how many packet are received
    print(f"New connection from {address}")
    count = 0

    while True:
        data = clientsocket.recv(1024)
        
        # 如果data為空則break
        if not data:
            break

        print("from client", data)
        print(count)

        # Q3-6 -----------------------------------------------
        if b'GET /good.html' in data:
            response = response_html()
        elif b'GET /style.css' in data:
            response = response_css()
        elif b'GET /redirect.html' in data:
            response = response_redirect()
        else:
            # request找不到對應的頁面
            response = response_not_found()
        
        clientsocket.sendall(response.encode())
        # -----------------------------------------------------
        
        # Q2. count+=1 after receive a packet----------------------------
        count+=1

        clientsocket.send(b'response')

        # 當收到兩個封包後則關閉連線
        if count == 2:
            # 跟client說要關掉連線了
            # 這時client會判斷還有沒有packet要送出
            clientsocket.send(b'close')
            count = 0
            break
        # ----------------------------------------------------------------

        if data == b'close':
            clientsocket.close()
            break

while True:
    (clientsocket, address) = s.accept()
    threading.Thread(target = serveClient, args = (clientsocket, address)).start()