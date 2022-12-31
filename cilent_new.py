import socket
import json

ADDRESS = ('127.0.0.1', 8712)
# 如果开多个客户端，这个client_type设置不同的值，比如客户端1为linxinfa，客户端2为linxinfa2
client_type = 'linxinfa'


def send_data(client, cmd, **kv):
    global client_type
    jd = {}
    jd['COMMAND'] = cmd
    jd['client_type'] = client_type
    jd['data'] = kv

    jsonstr = json.dumps(jd)
    print('send: ' + jsonstr)
    client.sendall(jsonstr.encode('utf8'))


def input_client_type():
    return input("注册客户端，请输入名字 :")


if __name__ == '__main__':
    client_type = input_client_type()
    client = socket.socket()
    client.connect(ADDRESS)
    print(client.recv(1024).decode(encoding='utf8'))
    send_data(client, 'CONNECT')

    while True:
        a = input("请输入要发送的信息:")
        send_data(client, 'SEND_DATA', data=a)


