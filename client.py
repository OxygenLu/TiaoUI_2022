import socket
import threading
from server_offline import ServerSocket


class Client:
    def __init__(self, app):
        self.app = app
        self.type = 'receiver'
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 声明socket类型，同时生成链接对象
        self.host = socket.gethostbyname(socket.gethostname())

    def start(self):
        threading.Thread(target=self.run).start()

    def run(self):
        self.start_server()
        while True:
            try:
                # self.client.connect(('zhude.guet.ltd', 12345))  # 建立一个链接，连接到服务器的端
                self.client.connect((self.host, 12345))  # 建立一个链接，连接到本地的端口
                break
            except:
                self.start_server()
                continue

        try:
            while True:
                if self.app.win.type == 'receiver':
                    print('等待接收...')
                    data = self.readline()  # 接收一个信息，并指定接收的大小 为1024字节
                    self.app.win.received.emit(data)
                    print('recv:', data)  # 输出我接收的信息
                # elif self.type == 'controller':
                #     msg = input() + '\n'
                #     self.send(msg.encode('utf8'))
        finally:
            self.client.close()  # 关闭这个链接

    def readline(self, size: int = 32 * 1024):
        buf = b''
        while len(buf) < size:
            recv = self.client.recv(1)  # 接收一个信息，并指定接收的大小最大为1字节
            if len(recv) == 0:
                raise Exception("unexpected end of stream")
            buf += recv
            if buf[-1] == 10:
                break
        buf = buf[:-1]
        return buf.decode('utf8')

    def send(self, data):
        if type(data) == str:
            data = (data + '\n').encode('utf8')
        self.client.send(data)

    def start_server(self):
        server = ServerSocket(self.host, 12345)
        server.start()
