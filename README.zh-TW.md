# 加拉地鼠

### 什麼是gala-gopher

gala-gopher一款結合eBPF、java agent等非侵入可觀測技術的觀測平台，其通過探針式架構可以輕鬆實現增加、減少探針。 gala-gopher是gala項目內負責數據採集的組件，其為gala項目提供Metrics、Event、Perf等數據，便於gala項目完成系統拓撲的繪製、故障根因的定位。

### 用例

#### 網絡監控

#### 輸入輸出控制

#### 應用性能監控

#### 應用性能Profiling

#### 網絡拓撲採集

### 安裝指南

#### RPM方式部署

-   獲取rpm包

    gala-gopher目前已在openEuler 21.09（已停止維護）/openEuler 22.09（已停止維護）/openEuler 22.03-LTS-SP1發布，可以通過配置以上發布版本的正式repo源來獲取rpm包；對於其他發布版本我們提供了以下方式來獲取rpm包：

    -   OBS 鏈接：網頁手動下載對應架構的rpm包

    ```basic
    openEuler-20.03-LTS : https://117.78.1.88/package/show/home:zpublic:branches:openEuler:20.03:LTS:SP1/gala-gopher-20.03lts
    openEuler-20.03-LTS-SP1 : https://117.78.1.88/package/show/home:zpublic:branches:openEuler:20.03:LTS:SP1/gala-gopher
    EulerOS-V2R9 : https://117.78.1.88/package/show/home:zpublic:branches:openEuler:20.03:LTS:SP1/gala-gopher-v2r9
    ```

    -   每日構建repo源：配置為yum源後安裝

    ```basic
    openEuler 22.03-LTS: http://121.36.84.172/dailybuild/openEuler-22.03-LTS/openEuler-22.03-LTS/EPOL/main/
    ```

-   rpm安裝

    ```bash
    yum install gala-gopher
    ```

-   運行

    通過 systemd 啟動後台服務：

    ```bash
    systemctl start gala-gopher.service
    ```

#### 容器方式部署

-   獲取容器鏡像

    用戶可以選擇直接[獲取官方容器鏡像](#docker1)或自行[構建容器鏡像](#docker2)

    <a id="docker1"></a>

    -   獲取官方容器鏡像

        在docker配置文件/etc/docker/daemon.json（文件不存在則需要新建）中追加如下內容來添加hub.oepkgs.net鏡像倉庫

            {
              "insecure-registries" : [ "hub.oepkgs.net" ]
            }

        完成後通過如下命令重啟docker服務使配置生效：

            systemctl daemon-reload
            systemctl restart docker


    根据系统架构从对应仓库拉取指定版本的gala-gopher官方容器镜像（以openEuler 20.03 LTS SP1为例）：

    ```
    # x86
    docker pull hub.oepkgs.net/a-ops/gala-gopher-x86_64:20.03-lts-sp1

    # aarch64
    docker pull hub.oepkgs.net/a-ops/gala-gopher-aarch64:20.03-lts-sp1
    ```

    目前支持的镜像版本tag有：euleros-v2r9（仅支持x86），20.03-lts，20.03-lts-sp1，22.03-lts，22.03-lts-sp1

<a id="docker2"></a>

-   構建容器鏡像

    獲取gala-gopher的rpm包，獲取方式詳見[RPM方式部署](#RPM方式部署)。

    用於生成容器鏡像的Dockerfile文件歸檔在[build目錄](./build)，生成方法詳見[如何生成gala-gopher容器鏡像](doc/how_to_build_docker_image.md)。

-   創建並運行容器

    gala-gopher涉及兩個配置文件：gala-gopher.conf和gala-gopher-app.conf。 gala-gopher.conf主要用於配置探針的數據上報開關、探針參數、探針是否開啟等；gala-gopher-app.conf是觀測白名單，可以把用戶感興趣的進程名加入白名單，gala-gopher就會觀測這個進程了。

    容器啟動前需要用戶自定義配置這兩個配置文件，請在宿主機創建配置文件目錄，並將[config目錄](./config)下兩個配置文件保存到該目錄，示例如下：

    ```shell
    [root@localhost ~]# mkdir gopher_user_conf
    [root@localhost gopher_user_conf]# ll
    total 8.0K
    -rw-r--r--. 1 root root 3.2K Jun 28 09:43 gala-gopher.conf
    -rw-r--r--. 1 root root  108 Jun 27 21:45 gala-gopher-app.conf
    ```

    請按照[配置文件介紹](./doc/conf_introduction.md)自定義修改配置文件。在執行docker run命令時，需要將宿主機上自定義的配置文件目錄和容器內/gala-gopher/user_conf目錄映射，從而將自定義的配置信息同步到容器內。

    最後按照如下示例命令啟動容器：

    ```shell
    docker run -d --name xxx -p 8888:8888 --privileged -v /etc/machine-id:/etc/machine-id -v /lib/modules:/lib/modules:ro -v /usr/src:/usr/src:ro -v /boot:/boot:ro -v /sys/kernel/debug:/sys/kernel/debug -v /sys/fs/bpf:/sys/fs/bpf -v /root/gopher_user_conf:/gala-gopher/user_conf/ -v /etc/localtime:/etc/localtime:ro -v /var/run/docker.sock:/var/run/docker.sock -v /var/lib/docker/overlay2:/var/lib/docker/overlay2 --pid=host gala-gopher:1.0.1
    ```

    成功啟動容器後，通過docker ps可以看到正在運行的容器：

    ```shell
    [root@localhost build]# docker ps
    CONTAINER ID   IMAGE               COMMAND                  CREATED              STATUS              PORTS                    NAMES
    eaxxxxxxxx02   gala-gopher:1.0.1   "/bin/sh -c 'cp -f /…"   About a minute ago   Up About a minute   0.0.0.0:8888->8888/tcp   xxx
    ```

-   獲取數據

    如上步驟docker run命令中所示，我們映射了宿主機8888端口和容器的8888端口，因而可以通過8888端口獲取數據來驗證gala-gopher是否運行成功：

    ```shell
    [root@localhost build]# curl http://localhost:8888
    ...
    gala_gopher_udp_que_rcv_drops{tgid="1234",s_addr="192.168.12.34",machine_id="xxxxx",hostname="eaxxxxxxxx02"} 0 1656383357000
    ...
    ```

    如上有指標數據輸出則證明gala-gopher運行成功。

#### K8S deployment方式部署

#### 

#### 自動化腳本方式部署

-   獲取部署工具

    1.  下載部署工具壓縮包：wget<https://gitee.com/Vchanger/a-ops-tools/repository/archive/master.zip>--no-check-certificate (內網用戶需要配置代理)
    2.  使用unzip解壓壓縮包後進入對應目錄即可使用

-   執行工具腳本進行部署

    -   rpm方式（僅支持openEuler 22.03 LTS/openEuler 22.03 LTS SP1)

            sh deploy.sh gopher -K <kafka服务器地址>

    -   容器鏡像方式：

            sh deploy.sh gopher -K <kafka服务器地址> --docker --tag <容器镜像tag>

        注:目前支持的鏡像版本tag有：euleros-v2r9（僅支持x86），20.03-lts，20.03-lts-sp1，22.03-lts，22.03-lts-sp1

    完成上述兩步後gala-gopher即可進入運行狀態。部署工具的使用約束說明與所有選項詳細說明可參照[A-Ops-Tools部署工具手冊](https://gitee.com/Vchanger/a-ops-tools#部署gala-gopher)

#### 系統集成API及方式

#### 配置方式及參數

[配置方式及參數](https://gitee.com/openeuler/gala-gopher/blob/master/doc/conf_introduction.md#配置文件介绍)

### 軟件架構

gala-gopher集成了常用的native探針以及知名中間件探針；gala-gopher有良好的擴展性，能方便的集成各種類型的探針程序，發揮社區的力量豐富探針框架的能力；gala-gopher中的幾個主要部件：

-   gala-gopher框架

    gala-gopher的基礎框架，負責配置文件解析、native探針/extend探針的管理、探針數據收集管理、探針數據上報對接、集成測試等；

-   native探針

    原生探針，主要是基於linux的proc文件系統收集的系統觀測指標；

-   extend探針

    支持shell/java/python/c等不同語言的第三方探針程序，僅需滿足輕量的數據上報格式即可集成到gala-gopher框架中；方便滿足各種應用場景下的觀測訴求；目前已實現知名中間件程序的探針觀測及指標上報，如：lvs、nginx、haproxy、dnsmasq、dnsbind、kafka、rabbitmq等；

-   部署配置文件

    gala-gopher啟動配置文件，可自定義具體使能的探針、指定數據上報的對接服務信息（kafka/prometheus等）

### 如何貢獻

#### 基於源碼構建

#### 構建rpm包

#### 探針開髮指南

[探針開髮指南](https://gitee.com/openeuler/gala-gopher/blob/master/doc/how_to_add_probe.md)

![devops](D:/GiteeCode/fork/gala-gopher/doc/pic/devops.JPG)

#### 如何新增探針

[如何新增native探針](https://gitee.com/openeuler/gala-gopher/blob/master/doc/how_to_add_probe.md#如何新增native探针)

[如何新增extends探針](https://gitee.com/openeuler/gala-gopher/blob/master/doc/how_to_add_probe.md#如何新增extends探针)

#### 如何裁剪探針

[如何實現探針裁剪](https://gitee.com/openeuler/gala-gopher/blob/master/doc/how_to_tail_probe.md)

### 路線圖

#### 巡檢能力

| 特性               | 發佈時間  | 發布版本                                |
| ---------------- | ----- | ----------------------------------- |
| TCP異常巡檢          | 22.12 | 開放歐拉 22.03 SP1                      |
| Socket異常巡檢       | 22.12 | 開放歐拉 22.03 SP1                      |
| 系統調用異常巡檢         | 22.12 | 開放歐拉 22.03 SP1                      |
| 進程I/O異常巡檢        | 22.12 | 開放歐拉 22.03 SP1                      |
| Block I/O異常巡檢    | 22.12 | 開放歐拉 22.03 SP1                      |
| 資源洩漏異常巡檢         | 22.12 | 開放歐拉 22.03 SP1                      |
| 硬件（磁盤/網卡/內存）故障巡檢 | 23.09 | openEuler 22.03 SP1、openEuler 23.09 |
| JVM異常巡檢          | 23.09 | openEuler 22.03 SP1、openEuler 23.09 |
| 主機網絡棧（包括虛擬化）丟包巡檢 | 23.09 | openEuler 22.03 SP1、openEuler 23.09 |

#### 可觀測性

| 特性                                                             | 發佈時間  | 發布版本                                |
| -------------------------------------------------------------- | ----- | ----------------------------------- |
| 進程級TCP觀測能力                                                     | 22.12 | 開放歐拉 22.03 SP1                      |
| 進程級Socket觀測能力                                                  | 22.12 | 開放歐拉 22.03 SP1                      |
| 分佈式存儲全棧I/O觀測能力                                                 | 22.12 | 開放歐拉 22.03 SP1                      |
| 虛擬化存儲I/O觀測能力                                                   | 22.12 | 開放歐拉 22.03 SP1                      |
| Block I/O觀測能力                                                  | 22.12 | 開放歐拉 22.03 SP1                      |
| 容器運行觀測能力                                                       | 22.12 | 開放歐拉 22.03 SP1                      |
| Redis性能觀測能力                                                    | 22.12 | 開放歐拉 22.03 SP1                      |
| PG性能觀測能力                                                       | 22.12 | 開放歐拉 22.03 SP1                      |
| Nginx會話觀測能力                                                    | 22.12 | 開放歐拉 22.03 SP1                      |
| Haproxy會話觀測能力                                                  | 22.12 | 開放歐拉 22.03 SP1                      |
| Kafka會話觀測能力                                                    | 22.12 | 開放歐拉 22.03 SP1                      |
| JVM性能觀測能力                                                      | 23.06 | openEuler 22.03 SP1、openEuler 23.09 |
| L7協議觀測能力（HTTP1.X/MySQL/PGSQL/Redis/Kafka）                      | 23.09 | openEuler 22.03 SP1、openEuler 23.09 |
| L7協議觀測能力（HTTP1.X/MySQL/PGSQL/Redis/Kafka/MongoDB/DNS/RocketMQ） | 24.03 | 深圳 22.03 開盤, 24.03 開盤               |
| 通用應用性能觀測能力                                                     | 24.03 | 開放歐拉24.03                           |
| 全鏈路協議跟踪能力                                                      | 24.09 | 開放歐拉24.09                           |

#### 性能profiling

| 特性                              | 發佈時間  | 發布版本                                |
| ------------------------------- | ----- | ----------------------------------- |
| 系統性能Profiling（OnCPU、Mem）        | 23.03 | 開放歐拉23.09                           |
| 系統性能Profiling（OnCPU、Mem、OffCPU） | 23.04 | openEuler 22.03 SP1、openEuler 23.09 |
| 線程級性能Profiling（java、C）          | 23.06 | openEuler 22.03 SP1、openEuler 23.09 |

#### 版本兼容性

| 特性                | 發佈時間  | 發布版本                  |
| ----------------- | ----- | --------------------- |
| 支持內核Release版本跨度兼容 | 23.12 | 深圳 22.03 開盤, 24.03 開盤 |
| 支持內核大版本跨度兼容       | 24.09 | 開放歐拉24.09             |
|                   |       |                       |

#### 可編程&擴展能力

| 特性                | 發佈時間  | 發布版本           |
| ----------------- | ----- | -------------- |
| 非侵入集成第三方探針        | 22.12 | 開放歐拉 22.03 SP1 |
| 非侵入集成第三方eBPF源碼    | 24.03 | 開放歐拉23.09      |
| 大語言驅動自動生成eBPF觀測探針 | 24.09 | 開放歐拉24.09      |

#### 部署&集成能力

| 特性                      | 發佈時間  | 發布版本                                |
| ----------------------- | ----- | ----------------------------------- |
| 支持Prometheus exporter對接 | 22.12 | 開放歐拉 22.03 SP1                      |
| 支持日誌文件形式對接              | 22.12 | 開放歐拉 22.03 SP1                      |
| 支持kafka client形式對接      | 22.12 | 開放歐拉 22.03 SP1                      |
| 支持REST接口動態變更探針監控能力      | 23.06 | openEuler 22.03 SP1、openEuler 23.09 |
