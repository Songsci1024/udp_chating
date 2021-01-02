# udp_chating
说明：基于UDP的C/S模式下的简单聊天室 **（Linux和windows都已兼容）**

#### 实现功能：

- 用户注册：要求服务器端在用户注册好账号后存储账号信息到**数据库**或者其他存储文件中。
- 用户登录：要求客户端基于UDP发送账号和密码给服务器，服务器端通过存储本地的账号信息与接收到的信息比较，匹配的话则登录成功，发回响应
- 公聊：要求客户端发送消息后，服务器能广播消息到所有在线的用户。
- 私聊：要求客户端指定目标好友发送消息，服务器能对应一个目标进行转发消息

#### python库介绍

- `Socket`：套接字库，它提供了标准的 `BSD Sockets API`，可以访问底层操作系统 Socket 接口的全部方法。

- `mysql.connector`：MySQL 官方提供的驱动器，用来连接使用Mysql。

- `time`: 处理时间的标准库。`time`库能够表达计算机时间，提供获取系统时间并格式化输出的方法，提供系统级精确计时功能（可以用于程序性能分析）。常用函数：时间获取：`time()`、`ctime()`、`gmtime()`，时间格式化：`strftime()`、`strptime()`
- `Sys`：该模块提供了一些接口，用于访问 Python 解释器自身使用和维护的变量，同时模块中还提供了一部分函数，可以与解释器进行比较深度的交互。该模块主要使用`sys.argv`用于获取命令行参数信息
- `Threading`:作用是提供创建并处理线程的函数，本实验用于多线程的消息接收和发送两个作用

python额外安装库：**mysql-connector**

#### 运行程序

- 服务器端：`python server.py`

- 客户端：`python client.py [IP] [PORT]`,仅限局域网测试，IP和端口号指的是服务器监听套接字的配置，测试使用`IP=127.0.0.1`，`PORT=8000`，端口号可修改服务器端代码改变

- 管理员：在服务器端运行客户端代码即可，`python client.py 127.0.0.1 8000`

- 数据库MySql设置：需要在服务器端的代码中给出数据库主机地址、用户名、密码和数据库名称，这里需要**手动配置**。

#### 使用方法

客户端成功运行后，输入1为注册，2为登录，之后输入用户名和密码。等待服务器发回响应后即可。

进入聊天室后，默认是公屏聊天，直接输入文字发送即可。

私聊：输入**PC**回车后，输入私聊好友名称和聊天内容。

#### 实例运行截图

![image-20210102223100483](https://raw.githubusercontent.com/Abandon339/Note_Book_picture/master/img/image-20210102223100483.png)

![image-20210102223107570](https://raw.githubusercontent.com/Abandon339/Note_Book_picture/master/img/image-20210102223107570.png)

![image-20210102223028185](https://raw.githubusercontent.com/Abandon339/Note_Book_picture/master/img/image-20210102223028185.png)

![image-20210102223151483](https://raw.githubusercontent.com/Abandon339/Note_Book_picture/master/img/image-20210102223151483.png)

![image-20210102223212282](https://raw.githubusercontent.com/Abandon339/Note_Book_picture/master/img/image-20210102223212282.png)

![image-20210102223218619](https://raw.githubusercontent.com/Abandon339/Note_Book_picture/master/img/image-20210102223218619.png)

![image-20210102223231681](https://raw.githubusercontent.com/Abandon339/Note_Book_picture/master/img/image-20210102223231681.png)

Log文件，记录注册和登录信息:

![image-20210102223245344](https://raw.githubusercontent.com/Abandon339/Note_Book_picture/master/img/image-20210102223245344.png)
