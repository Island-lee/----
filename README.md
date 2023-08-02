# gala-gopher

### 什么是gala-gopher
gala-gopher一款结合eBPF、java agent等非侵入可观测技术的观测平台，其通过探针式架构可以轻松实现增加、减少探针。gala-gopher是gala项目内负责数据采集的组件，其为gala项目提供Metrics、Event、Perf等数据，便于gala项目完成系统拓扑的绘制、故障根因的定位。

### Use Cases


#### 网络监控

#### I/O监控

#### 应用性能监控

#### 应用性能Profiling

#### 网络拓扑采集

### 安装指南

#### RPM方式部署

- 获取rpm包

  gala-gopher目前已在openEuler 21.09（已停止维护）/openEuler 22.09（已停止维护）/openEuler 22.03-LTS-SP1发布，可以通过配置以上发布版本的正式repo源来获取rpm包；对于其他发布版本我们提供了以下方式来获取rpm包：

  - OBS 链接：网页手动下载对应架构的rpm包

  ```basic
  openEuler-20.03-LTS : https://117.78.1.88/package/show/home:zpublic:branches:openEuler:20.03:LTS:SP1/gala-gopher-20.03lts
  openEuler-20.03-LTS-SP1 : https://117.78.1.88/package/show/home:zpublic:branches:openEuler:20.03:LTS:SP1/gala-gopher
  EulerOS-V2R9 : https://117.78.1.88/package/show/home:zpublic:branches:openEuler:20.03:LTS:SP1/gala-gopher-v2r9
  ```

  - 每日构建repo源：配置为yum源后安装

  ```basic
  openEuler 22.03-LTS: http://121.36.84.172/dailybuild/openEuler-22.03-LTS/openEuler-22.03-LTS/EPOL/main/
  ```

- rpm安装

  ```bash
  yum install gala-gopher
  ```

- 运行

  通过 systemd 启动后台服务：

  ```bash
  systemctl start gala-gopher.service
  ```

#### 容器方式部署

- 获取容器镜像

  用户可以选择直接[获取官方容器镜像](#docker1)或自行[构建容器镜像](#docker2)

  <a id="docker1"></a>

  - 获取官方容器镜像

    在docker配置文件/etc/docker/daemon.json（文件不存在则需要新建）中追加如下内容来添加hub.oepkgs.net镜像仓库

    ```
    {
      "insecure-registries" : [ "hub.oepkgs.net" ]
    }
    ```

    完成后通过如下命令重启docker服务使配置生效：

    ```
    systemctl daemon-reload
    systemctl restart docker
    ```


    根据系统架构从对应仓库拉取指定版本的gala-gopher官方容器镜像（以openEuler 20.03 LTS SP1为例）：
    
    ```
    # x86
    docker pull hub.oepkgs.net/a-ops/gala-gopher-x86_64:20.03-lts-sp1
    
    # aarch64
    docker pull hub.oepkgs.net/a-ops/gala-gopher-aarch64:20.03-lts-sp1
    ```
    
    目前支持的镜像版本tag有：euleros-v2r9（仅支持x86），20.03-lts，20.03-lts-sp1，22.03-lts，22.03-lts-sp1

  <a id="docker2"></a>


  - 构建容器镜像

    获取gala-gopher的rpm包，获取方式详见[RPM方式部署](#RPM方式部署)。

    用于生成容器镜像的Dockerfile文件归档在[build目录](./build)，生成方法详见[如何生成gala-gopher容器镜像](doc/how_to_build_docker_image.md)。

- 创建并运行容器

  gala-gopher涉及两个配置文件：gala-gopher.conf和gala-gopher-app.conf。gala-gopher.conf主要用于配置探针的数据上报开关、探针参数、探针是否开启等；gala-gopher-app.conf是观测白名单，可以把用户感兴趣的进程名加入白名单，gala-gopher就会观测这个进程了。

  容器启动前需要用户自定义配置这两个配置文件，请在宿主机创建配置文件目录，并将[config目录](./config)下两个配置文件保存到该目录，示例如下：

  ```shell
  [root@localhost ~]# mkdir gopher_user_conf
  [root@localhost gopher_user_conf]# ll
  total 8.0K
  -rw-r--r--. 1 root root 3.2K Jun 28 09:43 gala-gopher.conf
  -rw-r--r--. 1 root root  108 Jun 27 21:45 gala-gopher-app.conf
  ```

  请按照[配置文件介绍](./doc/conf_introduction.md)自定义修改配置文件。在执行docker run命令时，需要将宿主机上自定义的配置文件目录和容器内/gala-gopher/user_conf目录映射，从而将自定义的配置信息同步到容器内。

  最后按照如下示例命令启动容器：

  ```shell
  docker run -d --name xxx -p 8888:8888 --privileged -v /etc/machine-id:/etc/machine-id -v /lib/modules:/lib/modules:ro -v /usr/src:/usr/src:ro -v /boot:/boot:ro -v /sys/kernel/debug:/sys/kernel/debug -v /sys/fs/bpf:/sys/fs/bpf -v /root/gopher_user_conf:/gala-gopher/user_conf/ -v /etc/localtime:/etc/localtime:ro -v /var/run/docker.sock:/var/run/docker.sock -v /var/lib/docker/overlay2:/var/lib/docker/overlay2 --pid=host gala-gopher:1.0.1
  ```

  成功启动容器后，通过docker ps可以看到正在运行的容器：

  ```shell
  [root@localhost build]# docker ps
  CONTAINER ID   IMAGE               COMMAND                  CREATED              STATUS              PORTS                    NAMES
  eaxxxxxxxx02   gala-gopher:1.0.1   "/bin/sh -c 'cp -f /…"   About a minute ago   Up About a minute   0.0.0.0:8888->8888/tcp   xxx
  ```

- 获取数据

  如上步骤docker run命令中所示，我们映射了宿主机8888端口和容器的8888端口，因而可以通过8888端口获取数据来验证gala-gopher是否运行成功：

  ```shell
  [root@localhost build]# curl http://localhost:8888
  ...
  gala_gopher_udp_que_rcv_drops{tgid="1234",s_addr="192.168.12.34",machine_id="xxxxx",hostname="eaxxxxxxxx02"} 0 1656383357000
  ...
  ```

  如上有指标数据输出则证明gala-gopher运行成功。





#### K8S deployment方式部署

#### 



#### 自动化脚本方式部署

- 获取部署工具

  1. 下载部署工具压缩包：wget https://gitee.com/Vchanger/a-ops-tools/repository/archive/master.zip --no-check-certificate (内网用户需要配置代理)
  2. 使用unzip解压压缩包后进入对应目录即可使用

- 执行工具脚本进行部署

  - rpm方式（仅支持openEuler 22.03 LTS/openEuler 22.03 LTS SP1)

    ```
    sh deploy.sh gopher -K <kafka服务器地址>
    ```

  - 容器镜像方式：

    ```
    sh deploy.sh gopher -K <kafka服务器地址> --docker --tag <容器镜像tag>
    ```

    注:目前支持的镜像版本tag有：euleros-v2r9（仅支持x86），20.03-lts，20.03-lts-sp1，22.03-lts，22.03-lts-sp1

  完成上述两步后gala-gopher即可进入运行状态。部署工具的使用约束说明与所有选项详细说明可参照[A-Ops-Tools部署工具手册](https://gitee.com/Vchanger/a-ops-tools#部署gala-gopher)

#### 系统集成API及方式

#### 配置方式及参数

[配置方式及参数](https://gitee.com/openeuler/gala-gopher/blob/master/doc/conf_introduction.md#配置文件介绍)

### 软件架构

gala-gopher集成了常用的native探针以及知名中间件探针；gala-gopher有良好的扩展性，能方便的集成各种类型的探针程序，发挥社区的力量丰富探针框架的能力；gala-gopher中的几个主要部件：

- gala-gopher框架

  gala-gopher的基础框架，负责配置文件解析、native探针/extend探针的管理、探针数据收集管理、探针数据上报对接、集成测试等；

- native探针

  原生探针，主要是基于linux的proc文件系统收集的系统观测指标；

- extend探针

  支持shell/java/python/c等不同语言的第三方探针程序，仅需满足轻量的数据上报格式即可集成到gala-gopher框架中；方便满足各种应用场景下的观测诉求；目前已实现知名中间件程序的探针观测及指标上报，如：lvs、nginx、haproxy、dnsmasq、dnsbind、kafka、rabbitmq等；

- 部署配置文件

  gala-gopher启动配置文件，可自定义具体使能的探针、指定数据上报的对接服务信息（kafka/prometheus等）

### 如何贡献

#### 基于源码构建

#### 构建rpm包

#### 探针开发指南

[探针开发指南](https://gitee.com/openeuler/gala-gopher/blob/master/doc/how_to_add_probe.md)

![devops](D:/GiteeCode/fork/gala-gopher/doc/pic/devops.JPG)

#### 如何新增探针

[如何新增native探针](https://gitee.com/openeuler/gala-gopher/blob/master/doc/how_to_add_probe.md#如何新增native探针)

[如何新增extends探针](https://gitee.com/openeuler/gala-gopher/blob/master/doc/how_to_add_probe.md#如何新增extends探针)

#### 如何裁剪探针

[如何实现探针裁剪](https://gitee.com/openeuler/gala-gopher/blob/master/doc/how_to_tail_probe.md)

### 路线图

#### 巡检能力

| 特性                             | 发布时间 | 发布版本                             |
| -------------------------------- | -------- | ------------------------------------ |
| TCP异常巡检                      | 22.12    | openEuler 22.03 SP1                  |
| Socket异常巡检                   | 22.12    | openEuler 22.03 SP1                  |
| 系统调用异常巡检                 | 22.12    | openEuler 22.03 SP1                  |
| 进程I/O异常巡检                  | 22.12    | openEuler 22.03 SP1                  |
| Block I/O异常巡检                | 22.12    | openEuler 22.03 SP1                  |
| 资源泄漏异常巡检                 | 22.12    | openEuler 22.03 SP1                  |
| 硬件（磁盘/网卡/内存）故障巡检   | 23.09    | openEuler 22.03 SP1, openEuler 23.09 |
| JVM异常巡检                      | 23.09    | openEuler 22.03 SP1, openEuler 23.09 |
| 主机网络栈（包括虚拟化）丢包巡检 | 23.09    | openEuler 22.03 SP1, openEuler 23.09 |

#### 可观测性

| 特性                                                         | 发布时间 | 发布版本                             |
| ------------------------------------------------------------ | -------- | ------------------------------------ |
| 进程级TCP观测能力                                            | 22.12    | openEuler 22.03 SP1                  |
| 进程级Socket观测能力                                         | 22.12    | openEuler 22.03 SP1                  |
| 分布式存储全栈I/O观测能力                                    | 22.12    | openEuler 22.03 SP1                  |
| 虚拟化存储I/O观测能力                                        | 22.12    | openEuler 22.03 SP1                  |
| Block I/O观测能力                                            | 22.12    | openEuler 22.03 SP1                  |
| 容器运行观测能力                                             | 22.12    | openEuler 22.03 SP1                  |
| Redis性能观测能力                                            | 22.12    | openEuler 22.03 SP1                  |
| PG性能观测能力                                               | 22.12    | openEuler 22.03 SP1                  |
| Nginx会话观测能力                                            | 22.12    | openEuler 22.03 SP1                  |
| Haproxy会话观测能力                                          | 22.12    | openEuler 22.03 SP1                  |
| Kafka会话观测能力                                            | 22.12    | openEuler 22.03 SP1                  |
| JVM性能观测能力                                              | 23.06    | openEuler 22.03 SP1, openEuler 23.09 |
| L7协议观测能力（HTTP1.X/MySQL/PGSQL/Redis/Kafka）            | 23.09    | openEuler 22.03 SP1, openEuler 23.09 |
| L7协议观测能力（HTTP1.X/MySQL/PGSQL/Redis/Kafka/MongoDB/DNS/RocketMQ） | 24.03    | openEuler 22.03 SP3，openEuler 24.03 |
| 通用应用性能观测能力                                         | 24.03    | openEuler 24.03                      |
| 全链路协议跟踪能力                                           | 24.09    | openEuler 24.09                      |

#### 性能profiling

| 特性                                    | 发布时间 | 发布版本                             |
| --------------------------------------- | -------- | ------------------------------------ |
| 系统性能Profiling（OnCPU、Mem）         | 23.03    | openEuler 23.09                      |
| 系统性能Profiling（OnCPU、Mem、OffCPU） | 23.04    | openEuler 22.03 SP1, openEuler 23.09 |
| 线程级性能Profiling（java、C）          | 23.06    | openEuler 22.03 SP1, openEuler 23.09 |

#### 版本兼容性

| 特性                        | 发布时间 | 发布版本                             |
| --------------------------- | -------- | ------------------------------------ |
| 支持内核Release版本跨度兼容 | 23.12    | openEuler 22.03 SP3, openEuler 24.03 |
| 支持内核大版本跨度兼容      | 24.09    | openEuler 24.09                      |
|                             |          |                                      |

#### 可编程&扩展能力

| 特性                           | 发布时间 | 发布版本            |
| ------------------------------ | -------- | ------------------- |
| 非侵入集成第三方探针           | 22.12    | openEuler 22.03 SP1 |
| 非侵入集成第三方eBPF源码       | 24.03    | openEuler 23.09     |
| 大语言驱动自动生成eBPF观测探针 | 24.09    | openEuler 24.09     |



#### 部署&集成能力

| 特性                             | 发布时间 | 发布版本                             |
| -------------------------------- | -------- | ------------------------------------ |
| 支持Prometheus exporter对接      | 22.12    | openEuler 22.03 SP1                  |
| 支持日志文件形式对接             | 22.12    | openEuler 22.03 SP1                  |
| 支持kafka client形式对接         | 22.12    | openEuler 22.03 SP1                  |
| 支持REST接口动态变更探针监控能力 | 23.06    | openEuler 22.03 SP1, openEuler 23.09 |
test
