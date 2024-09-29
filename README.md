## 创建一个简单的微服务案例

- 监控检测和服务注册：**consul**

- 数据存储：**mysql**

- 后端语言：**python**

- web框架：**flask**

### 实施

#### 1. consul

本次采用单机模式，下载consul包后直接启动即可。

```shell
#解压
unzip consul_1.19.2_linux_amd64.zip -d /usr/bin/
#运行
consul agent -server -ui -bootstrap-expect=1 -data-dir=./data -datacenter=dc1 -node=node10 -client=0.0.0.0 -bind=192.168.83.104
```

参数说明：

- -server： 以 server 身份启动；不加该参数默认是 client
- -ui：可以访问 UI 界面
- -bootstrap-expect：集群期望的节点数，只有节点数量达到这个值才会选举 leader
- -data-dir：数据存放的目录
- -datacenter：数据中心名称，默认是 dc1
- -node：节点的名称
- -client：客户端访问 Consul 的绑定地址；默认为 127.0.0.1，只能本地访问
- -bind：集群内部通信绑定的地址，默认为 0.0.0.0

#### 2.mysql 

安装数据库完成初始化配置，并创建数据库

```mysql
CREATE DATABASE user_service_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE order_service_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

#### 3.运行测试

```shell
#安装依赖
pip3 install -r requirements.txt
nohup python3 order_server.py &
nohup python3 user_server.py &
nohup python3 api_gateway.py &
#访问入网的5000端口即可
```

#### 4.效果图

###### UI

![image-20240929165529989](F:\Microservice Demo\images\image-20240929165529989.png)

###### consul

![image-20240929165606409](F:\Microservice Demo\images\image-20240929165606409.png)