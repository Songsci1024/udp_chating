import socket, mysql.connector, time

#数据库需要手动配置，说明所有sql命令中的users都指的是当前数据库下的创建的一个表，没有该表需要先创建
#创建过程参考https://www.runoob.com/python3/python-mysql-connector.html
mydb = mysql.connector.connect(
    host = 'your_hostaddress',          #数据库主机地址，一般为localhost
    user = 'database user',             #用户名
    passwd = 'database password',       #密码
    database = 'database name'          #数据库名称
)
mycursor = mydb.cursor(buffered=True)    # 获取操作游标
log = open("log.txt", "a+")
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   #创建一个UDP套接字
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    address = ('0.0.0.0', 8000) #[IP, PORT]
    server.bind(address)
    Start_Work(server)
    log.write(time_format() + "stop working!\n")
    #让所有在线用户离线
    result = mysql_execute_return('SELECT username FROM users WHERE states = %s', \
                                        (1, ), 'more')
    if result:
        for x in result:
            mysql_execute_return('UPDATE users SET states = %s WHERE username = %s', \
                            (0, x[0]), 'no')
    server.close()
    log.close()
    print('服务器已关闭')
def Start_Work(server):
    while True:
        try:
            log.write(time_format() + "start working!\n")
            try:
                mesg, addr = server.recvfrom(1024)  #兼容windows平台（windows里的bug）
            except:
                continue
            mesglist = mesg.decode().split('\a')    #拆分数据,用'\a'作为分隔符，避免聊天内容因空格输出不全
            if mesglist[0] == "1":                  #注册
                Register(server, mesglist[1], mesglist[2], addr)
            elif(mesglist[0] == "2"):               #登陆
                Login(server, mesglist[1], mesglist[2], addr)
            elif(mesglist[0] == "3"):               #公聊
                Group_Chat(server, mesglist[1], mesglist[2], addr)
            elif(mesglist[0] == "4"):               #私聊
                Private_Chat(server, mesglist[1], mesglist[2], mesglist[3], addr)
            elif(mesglist[0] == "5"):               #退出
                Logged_Out(server, mesglist[1], addr)
            elif(mesglist[0] == '886') and (addr[0] == '127.0.0.1'):    #神秘指令：实际部署用管理员电脑静态IP，停止服务器工作
                server.sendto('stop'.encode(), addr)
                break
        except:
            break
#@功能：注册账号 @参数：服务器地址，用户列表，用户名，密码，客户端IP地址
def Register(server, username, password, addr):
    result = mysql_execute_return('SELECT username FROM users WHERE username = %s', \
                                        (username, ), 'one')
    if result:                                      #非空说明用户名在数据库中已有记录
        server.sendto('用户名已存在'.encode(), addr)
        return
    #不存在则创建，放入数据库中,显示已登录状态
    mysql_execute_return("INSERT INTO users (username, password, states, addr, port) \
                                    VALUES (%s, %s, %s, %s, %s)", \
                                    (username, password, 1, addr[0], addr[1]), 'no')
    server.sendto('用户创建成功'.encode(), addr)     #发回响应信息
    message = '\n' + username + '进入聊天室'
    result = mysql_execute_return('SELECT * FROM users WHERE username != %s AND states = %s', \
                                        (username, 1), 'more')
    if result:
        for x in result:
            server.sendto(message.encode(), (x[3], x[4]))       #广播用户进入聊天室的消息（给在线用户发消息）
    log.write(time_format() + username + ' 注册成功' + '\n')
    print(message)
#@功能：登录 @参数：同上
def Login(server, username, password, addr):
    message = '\n' + username + '进入聊天室'
    result = mysql_execute_return('SELECT * FROM users WHERE username = %s', \
                                        (username, ), 'one')
    print(result)
    if result:      #非空则说明注册过该用户名
        if result[1] != password:                  #mysql返回的一行是list类型，内嵌元组
            server.sendto('密码错误'.encode(), addr)
            return
        if result[2] == 1:
            if result[3] == addr[0]:               #同地登录不需要其他操作
                server.sendto('用户登录成功'.encode(), addr)
                return
            else:                                  #如果用户正在异地登录，先让用户下线 
                Logged_Out(server, username, (result[3], result[4]))
        mysql_execute_return('UPDATE users SET states = %s, addr = %s, port = %s WHERE username = %s', \
                                (1, addr[0], addr[1], username), 'no')  #更新当前用户信息
        server.sendto('用户登录成功'.encode(), addr)
        result = mysql_execute_return('SELECT * FROM users WHERE username != %s AND states = %s', \
                                            (username, 1), 'more')
        if result:
            for x in result:
                server.sendto(message.encode(), (x[3], x[4]))       #广播用户进入聊天室的消息（给在线用户发消息）
        log.write(time_format() + username + ' 登录成功,进入聊天室' + '\n')
        print(message)
    else:
        server.sendto('不存在该用户，请选择注册用户再进入聊天室'.encode(), addr)
# @功能：群聊 @参数 服务器地址，用户名，聊天内容，客户端IP地址+端口号
def Group_Chat(server, username, content, addr):
    message = '\n' + '[公聊]' + username + '->' + '\n' + content
    result = mysql_execute_return('SELECT * FROM users WHERE username != %s AND states = %s', \
                                            (username, 1), 'more')
    if result:
        for x in result:
            server.sendto(message.encode(), (x[3], x[4]))           #广播用户发出的消息（给在线用户发消息）
    print(message)
#@功能：私聊 @参数 同上      
def Private_Chat(server, username, pc_name, content, addr):
    message = '\n' + '[私聊]' + username + '@you' + '->' + '\n'+ content
    result = mysql_execute_return('SELECT * FROM users WHERE username = %s', \
                                        (pc_name, ), 'one')
    if result:                           #检查私聊好友是否存在
        if (pc_name != username) and (result[2] != 0):
            server.sendto(message.encode(), (result[3], result[4])) #发送消息给私聊好友
        else:
            server.sendto('私聊好友不在线'.encode(), addr)           #发送响应消息给发送用户
    else:    
        server.sendto('私聊好友不存在'.encode(), addr)
        return
#@功能：登出 @参数 服务器地址，用户名，要登出用户所在IP地址+端口号
def Logged_Out(server, username, addr):
    mysql_execute_return('UPDATE users SET states = %s WHERE username = %s', (0, username, ), 'no')
    message = '\n' + username + '离开聊天室'
    print(addr)
    result = mysql_execute_return('SELECT * FROM users WHERE username != %s AND states = %s', \
                                    (username, 1), 'more')
    if result:                          #广播用户离开聊天室的消息
        for x in result:
            server.sendto(message.encode(), (x[3], x[4]))
    server.sendto('exit'.encode(), addr)
    #记录登出信息
    log.write(time_format() + username + ' 离开聊天室' + '\n')
    print(message)
#功能：执行sql语句，返回查询到的结果
def mysql_execute_return(sql, value, number):
    try:
        # print(sql, value)
        if value[0] == None:
            mycursor.execute(sql)
        else:
            mycursor.execute(sql, value)
        mydb.commit()
        if number == 'more':            #返回所有的查询结果
            return mycursor.fetchall()
        elif number == 'one':           #返回一个查询结果
            return mycursor.fetchone() 
        else:                           #返回空值
            return None
    except Exception as e:
        print('执行sql语句失败', e)
        mydb.rollback()                 #执行失败，撤销之前的全部操作
#功能：返回格式化后的时间
def time_format():
    mesg_time = '[' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ']: '
    return mesg_time
if __name__ == "__main__":
    main()
