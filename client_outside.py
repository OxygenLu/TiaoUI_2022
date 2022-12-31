import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 声明socket类型，同时生成链接对象
client.connect(('localhost', 12345))  # 建立一个链接，连接到本地的端口

# 选择角色
print("请选择角色：（0接收 1发送）")
flag = input()
role = 'receiver\n' if flag == '0' else 'sender\n'
client.send(role.encode('utf8'))  # 发送一条信息 python3 只接收btye流
client.send((input('请输入客户端名称：')+'\n').encode('utf8'))

while True:
    if flag == '0':
        print('等待接收...')
        data = client.recv(1024)  # 接收一个信息，并指定接收的大小 为1024字节
        print('recv:', data.decode())  # 输出我接收的信息
    else:
        msg = input("输入命令：") + '\n'
        client.send(msg.encode('utf8'))
        print("已发送")
