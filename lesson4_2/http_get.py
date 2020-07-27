import socket

def http_get(host, page):
    sock = socket.create_connection((host, 80))
    sock.sendall(('GET ' + page + ' HTTP/1.1\r\nHost: ' + host + '\r\n\r\n').encode())
    print(sock.recv(1000).decode())
    sock.close()

http_get('50.87.178.13', '/CScourses/03b1_minimal.html')