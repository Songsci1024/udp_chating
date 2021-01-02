import sys, socket, threading
def main():
    if len(sys.argv)<3:
        print('参数错误')
        return
    address = (sys.argv[1], int(sys.argv[2]))   #sys.argv[0]指的是程序的所在文件路径
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   #创建一个UDP套接字
    while True:
        operation = input('选择操作类型（1.register 2.login): ')
        if (operation != '1') & (operation != '2'):
            print('输入错误')
            continue
        username = input('输入用户名: ')
        password = input('输入密码： ')
        message = operation + '\a' + username + '\a' + password
        client.sendto(message.encode(), address)
        data, addr = client.recvfrom(1024)  #接受服务器的提示信息
        if(data.decode() == '用户创建成功' ) or (data.decode() == '用户登录成功'):
            print('进入聊天室\n（输入quit退出，输入PC私聊，默认公聊)')
            break
        else:
            print(data.decode())
    #多线程，thread1用于发送数据，thread2用于接收数据
    thread1 = threading.Thread(target=send_info, args=(client, username, address, ))
    thread2 = threading.Thread(target=recv_info, args=(client, username, ))
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()  #等待收发线程都结束
    client.close()
    return
def send_info(client, username, address):
    while True:
        message = '\n' + '[公聊]' + username + '(me)' + '->' + '\n'
        x = input(message)
        if(x == 'PC'):      #私聊
            pc_name = input('输入私聊对象的用户名: ')
            content = input('输入聊天内容: ')
            message = '4\a' + username + '\a' + pc_name + '\a' + content
            client.sendto(message.encode(), address)
        elif(x == 'quit'):  #退出聊天室
            message = '5\a' + username
            client.sendto(message.encode(), address)
            break
        elif(x == 'root_server_stop'):
            message = '886\a' + username
            client.sendto(message.encode(), address)
            break
        else:               #默认公聊
            message = '3\a' + username + '\a' + x
            client.sendto(message.encode(), address)
def recv_info(client, username):
    while True:
        mesg, addr = client.recvfrom(1024)
        if(mesg.decode() == 'exit'):    #send_info中发送quit命令，服务器响应返回exit消息
            print('您已离开聊天室，欢迎下次再来')
            break
        elif(mesg.decode() == 'stop'):
            print('您已关闭聊天室服务器')
            break  
        print(mesg.decode() + '\n' + '[公聊]' + username + '(me)' + '->')

if __name__ == "__main__":
    main()

