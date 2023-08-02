# gala-gopher

### qu'est-ce que gala-gopher

Gala-gopher est une plate-forme d'observation qui combine eBPF, agent java et d'autres technologies observables non intrusives.Il peut facilement augmenter et diminuer les sondes grâce à l'architecture basée sur les sondes. Gala-gopher est le composant responsable de la collecte de données dans le projet gala. Il fournit des données telles que Metrics, Event et Perf pour le projet gala, ce qui est pratique pour le projet gala pour terminer le dessin de la topologie du système et l'emplacement de la cause première de la panne.

### Cas d'utilisation

#### Surveillance du réseau

#### Contrôle des E/S

#### Surveillance des performances des applications

#### Profilage des performances des applications

#### Collection de topologies de réseau

### guide d'installation

#### Déploiement RPM

-   Obtenir le package rpm

    Gala-gopher est actuellement publié dans openEuler 21.09 (maintenance arrêtée)/openEuler 22.09 (maintenance arrêtée)/openEuler 22.03-LTS-SP1, et le package rpm peut être obtenu en configurant la source officielle du référentiel de la version ci-dessus ; pour les autres versions versions we Les méthodes suivantes sont fournies pour obtenir des packages rpm :

    -   Lien OBS : Téléchargez manuellement le package rpm de l'architecture correspondante à partir de la page Web

    ```basic
    openEuler-20.03-LTS : https://117.78.1.88/package/show/home:zpublic:branches:openEuler:20.03:LTS:SP1/gala-gopher-20.03lts
    openEuler-20.03-LTS-SP1 : https://117.78.1.88/package/show/home:zpublic:branches:openEuler:20.03:LTS:SP1/gala-gopher
    EulerOS-V2R9 : https://117.78.1.88/package/show/home:zpublic:branches:openEuler:20.03:LTS:SP1/gala-gopher-v2r9
    ```

    -   Source du référentiel de construction quotidienne : installez-la après la configuration en tant que source yum

    ```basic
    openEuler 22.03-LTS: http://121.36.84.172/dailybuild/openEuler-22.03-LTS/openEuler-22.03-LTS/EPOL/main/
    ```

-   installation rpm

    ```bash
    yum install gala-gopher
    ```

-   courir

    Démarrez le service d'arrière-plan via systemd :

    ```bash
    systemctl start gala-gopher.service
    ```

#### Déploiement de conteneur

-   Obtenir l'image du conteneur

    Les utilisateurs peuvent choisir de directement[Obtenez des images de conteneurs officielles](#docker1)ou par vous-même[Construire une image de conteneur](#docker2)

    <a id="docker1"></a>

    -   Obtenez des images de conteneurs officielles

        Ajoutez le contenu suivant au fichier de configuration docker /etc/docker/daemon.json (si le fichier n'existe pas, il doit être créé) pour ajouter l'entrepôt miroir hub.oepkgs.net

            {
              "insecure-registries" : [ "hub.oepkgs.net" ]
            }

        Une fois terminé, redémarrez le service Docker avec la commande suivante pour que la configuration prenne effet :

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

-   Construire une image de conteneur

    Procurez-vous le package rpm de gala-gopher. Pour plus de détails, voir[Déploiement RPM](#RPM方式部署)。

    Le Dockerfile pour générer des images de conteneurs est archivé sur[répertoire de construction](./build), voir la méthode de génération pour plus de détails[Comment générer une image de conteneur gala-gopher](doc/how_to_build_docker_image.md)。

-   Créer et exécuter le conteneur

    Gala-gopher implique deux fichiers de configuration : gala-gopher.conf et gala-gopher-app.conf. gala-gopher.conf est principalement utilisé pour configurer le commutateur de rapport de données de la sonde, les paramètres de la sonde, si la sonde est activée, etc. ; gala-gopher-app.conf est la liste blanche d'observation, qui peut ajouter le nom du processus qui l'utilisateur est intéressé par la liste blanche, Gala-gopher observera ce processus.

    Avant le démarrage du conteneur, l'utilisateur doit configurer ces deux fichiers de configuration. Veuillez créer un répertoire de fichiers de configuration sur l'hôte et définir le[répertoire de configuration](./config)Les deux fichiers de configuration suivants sont enregistrés dans ce répertoire, les exemples sont les suivants :

    ```shell
    [root@localhost ~]# mkdir gopher_user_conf
    [root@localhost gopher_user_conf]# ll
    total 8.0K
    -rw-r--r--. 1 root root 3.2K Jun 28 09:43 gala-gopher.conf
    -rw-r--r--. 1 root root  108 Jun 27 21:45 gala-gopher-app.conf
    ```

    Veuillez suivre[Présentation du fichier de configuration](./doc/conf_introduction.md)Personnalisez les fichiers de configuration. Lors de l'exécution de la commande docker run, vous devez mapper le répertoire du fichier de configuration personnalisé sur l'hôte au répertoire /gala-gopher/user_conf dans le conteneur, afin de synchroniser les informations de configuration personnalisée dans le conteneur.

    Enfin, démarrez le conteneur selon l'exemple de commande suivant :

    ```shell
    docker run -d --name xxx -p 8888:8888 --privileged -v /etc/machine-id:/etc/machine-id -v /lib/modules:/lib/modules:ro -v /usr/src:/usr/src:ro -v /boot:/boot:ro -v /sys/kernel/debug:/sys/kernel/debug -v /sys/fs/bpf:/sys/fs/bpf -v /root/gopher_user_conf:/gala-gopher/user_conf/ -v /etc/localtime:/etc/localtime:ro -v /var/run/docker.sock:/var/run/docker.sock -v /var/lib/docker/overlay2:/var/lib/docker/overlay2 --pid=host gala-gopher:1.0.1
    ```

    Après avoir démarré le conteneur avec succès, vous pouvez voir le conteneur en cours d'exécution via docker ps :

    ```shell
    [root@localhost build]# docker ps
    CONTAINER ID   IMAGE               COMMAND                  CREATED              STATUS              PORTS                    NAMES
    eaxxxxxxxx02   gala-gopher:1.0.1   "/bin/sh -c 'cp -f /…"   About a minute ago   Up About a minute   0.0.0.0:8888->8888/tcp   xxx
    ```

-   récupérer des données

    Comme indiqué dans la commande docker run à l'étape ci-dessus, nous avons mappé le port 8888 de l'hôte et le port 8888 du conteneur, afin que nous puissions obtenir des données via le port 8888 pour vérifier si gala-gopher s'exécute avec succès :

    ```shell
    [root@localhost build]# curl http://localhost:8888
    ...
    gala_gopher_udp_que_rcv_drops{tgid="1234",s_addr="192.168.12.34",machine_id="xxxxx",hostname="eaxxxxxxxx02"} 0 1656383357000
    ...
    ```

    S'il y a une sortie de données d'indicateur, cela prouve que gala-gopher fonctionne avec succès.

#### Déploiement du mode de déploiement K8S

#### 

#### Déploiement automatisé des scripts

-   Obtenir des outils de déploiement

    1.  Téléchargez le package compressé de l'outil de déploiement : wget<https://gitee.com/Vchanger/a-ops-tools/repository/archive/master.zip>--no-check-certificate (les utilisateurs de l'intranet doivent configurer le proxy)
    2.  Utilisez unzip pour décompresser le package compressé et entrez le répertoire correspondant pour l'utiliser

-   Exécuter le script de l'outil à déployer

    -   mode rpm (seul openEuler 22.03 LTS/openEuler 22.03 LTS SP1 est pris en charge)

            sh deploy.sh gopher -K <kafka服务器地址>

    -   Méthode de mise en miroir du conteneur :

            sh deploy.sh gopher -K <kafka服务器地址> --docker --tag <容器镜像tag>

        Remarque : les balises de version d'image actuellement prises en charge sont : euleros-v2r9 (uniquement compatible x86), 20.03-lts, 20.03-lts-sp1, 22.03-lts, 22.03-lts-sp1

    Après avoir terminé les deux étapes ci-dessus, gala-gopher peut entrer dans l'état de fonctionnement. Pour connaître les contraintes d'utilisation et toutes les options de l'outil de déploiement, reportez-vous à[Manuel de l'outil de déploiement A-Ops-Tools](https://gitee.com/Vchanger/a-ops-tools#部署gala-gopher)

#### API et méthode d'intégration système

#### Méthode et paramètres de configuration

[Méthode et paramètres de configuration](https://gitee.com/openeuler/gala-gopher/blob/master/doc/conf_introduction.md#配置文件介绍)

### Architecture logicielle

gala-gopher intègre des sondes natives couramment utilisées et des sondes middleware bien connues ; gala-gopher a une bonne évolutivité, peut facilement intégrer divers types de programmes de sonde et exploite la puissance de la communauté pour enrichir les capacités du cadre de sonde ; gala -Plusieurs principaux composants de gopher :

-   cadre gala-gopher

    Le cadre de base de gala-gopher est responsable de l'analyse des fichiers de configuration, de la gestion des sondes natives/sondes d'extension, de la gestion de la collecte des données des sondes, de l'amarrage des rapports de données des sondes, des tests d'intégration, etc. ;

-   sonde native

    Les sondes natives sont principalement des indicateurs d'observation du système collectés sur la base du système de fichiers proc basé sur Linux ;

-   étendre la sonde

    Prend en charge les programmes de sonde tiers dans différents langages tels que shell/java/python/c, et peut être intégré dans le cadre gala-gopher uniquement en respectant le format de rapport de données léger ; il est pratique de répondre aux exigences d'observation dans divers scénarios d'application; actuellement Réaliser l'observation de sonde et le rapport d'index de programmes middleware bien connus, tels que: lvs, nginx, haproxy, dnsmasq, dnsbind, kafka, rabbitmq, etc.;

-   fichier de configuration de déploiement

    Le fichier de configuration de démarrage de gala-gopher peut personnaliser les sondes activées spécifiques et spécifier les informations de service d'amarrage pour le rapport de données (kafka/prometheus, etc.)

### comment contribuer

#### Construire à partir de la source

#### construire le paquet rpm

#### Guide de développement de la sonde

[Guide de développement de la sonde](https://gitee.com/openeuler/gala-gopher/blob/master/doc/how_to_add_probe.md)

![devops](D:/GiteeCode/fork/gala-gopher/doc/pic/devops.JPG)

#### Comment ajouter une sonde

[Comment ajouter une sonde native](https://gitee.com/openeuler/gala-gopher/blob/master/doc/how_to_add_probe.md#如何新增native探针)

[Comment ajouter une sonde d'extension](https://gitee.com/openeuler/gala-gopher/blob/master/doc/how_to_add_probe.md#如何新增extends探针)

#### Comment recadrer une sonde

[Comment obtenir un écrêtage de la sonde](https://gitee.com/openeuler/gala-gopher/blob/master/doc/how_to_tail_probe.md)

### le plan de route

#### Capacité d'inspection

| caractéristique                                                                           | temps de libération | version finale                       |
| ----------------------------------------------------------------------------------------- | ------------------- | ------------------------------------ |
| Inspection anormale du TCP                                                                | 22.12               | openEuler 22.03 SP1                  |
| Inspection anormale de la douille                                                         | 22.12               | openEuler 22.03 SP1                  |
| Inspection des exceptions d'appel système                                                 | 22.12               | openEuler 22.03 SP1                  |
| Inspection des exceptions d'E/S de processus                                              | 22.12               | openEuler 22.03 SP1                  |
| Inspection des exceptions d'E/S de bloc                                                   | 22.12               | openEuler 22.03 SP1                  |
| Inspection anormale de fuite de ressources                                                | 22.12               | openEuler 22.03 SP1                  |
| Inspection des pannes matérielles (disque/carte réseau/mémoire)                           | 23.09               | openEuler 22.03 SP1, openEuler 23.09 |
| Inspection des exceptions JVM                                                             | 23.09               | openEuler 22.03 SP1, openEuler 23.09 |
| Inspection de la perte de paquets de la pile du réseau hôte (y compris la virtualisation) | 23.09               | openEuler 22.03 SP1, openEuler 23.09 |

#### Observabilité

| caractéristique                                                                               | temps de libération | version finale                       |
| --------------------------------------------------------------------------------------------- | ------------------- | ------------------------------------ |
| Capacité d'observation TCP au niveau du processus                                             | 22.12               | openEuler 22.03 SP1                  |
| Capacité d'observation des sockets au niveau du processus                                     | 22.12               | openEuler 22.03 SP1                  |
| Capacité d'observation des E/S de la pile complète du stockage distribué                      | 22.12               | openEuler 22.03 SP1                  |
| Capacité d'observation des E/S de stockage virtualisé                                         | 22.12               | openEuler 22.03 SP1                  |
| Capacité d'observation des E/S de bloc                                                        | 22.12               | openEuler 22.03 SP1                  |
| Capacité d'observation du fonctionnement des conteneurs                                       | 22.12               | openEuler 22.03 SP1                  |
| Capacité d'observation des performances de Redis                                              | 22.12               | openEuler 22.03 SP1                  |
| Capacité d'observation des performances PG                                                    | 22.12               | openEuler 22.03 SP1                  |
| Capacité d'observation de session Nginx                                                       | 22.12               | openEuler 22.03 SP1                  |
| Capacité d'observation de session Haproxy                                                     | 22.12               | openEuler 22.03 SP1                  |
| Capacité d'observation des sessions Kafka                                                     | 22.12               | openEuler 22.03 SP1                  |
| Capacité d'observation des performances JVM                                                   | 23.06               | openEuler 22.03 SP1, openEuler 23.09 |
| Capacité d'observation du protocole L7 (HTTP1.X/MySQL/PGSQL/Redis/Kafka)                      | 23.09               | openEuler 22.03 SP1, openEuler 23.09 |
| Capacité d'observation du protocole L7 (HTTP1.X/MySQL/PGSQL/Redis/Kafka/MongoDB/DNS/RocketMQ) | 24.03               | ouvert le 22.03 SZZ, ouvert le 24.03 |
| Capacité générale d'observation des performances des applications                             | 24.03               | openEuler 24.03                      |
| Capacité de suivi du protocole de liaison complète                                            | 24.09               | openEuler 24.09                      |

#### profilage des performances

| caractéristique                                            | temps de libération | version finale                       |
| ---------------------------------------------------------- | ------------------- | ------------------------------------ |
| Profilage des performances du système (OnCPU, Mem)         | 23.03               | openEuler 23.09                      |
| Profilage des performances du système (OnCPU, Mem, OffCPU) | 23.04               | openEuler 22.03 SP1, openEuler 23.09 |
| Profilage des performances au niveau des threads (java, C) | 23.06               | openEuler 22.03 SP1, openEuler 23.09 |

#### compatibilité des versions

| caractéristique                                                                    | temps de libération | version finale                       |
| ---------------------------------------------------------------------------------- | ------------------- | ------------------------------------ |
| Prise en charge de la compatibilité de l'étendue de la version de version du noyau | 23.12               | ouvert le 22.03 SZZ, ouvert le 24.03 |
| Prise en charge de la compatibilité entre les principales versions du noyau        | 24.09               | openEuler 24.09                      |
|                                                                                    |                     |                                      |

#### Programmable et extensible

| caractéristique                                                             | temps de libération | version finale      |
| --------------------------------------------------------------------------- | ------------------- | ------------------- |
| Intégration non intrusive de sondes tierces                                 | 22.12               | openEuler 22.03 SP1 |
| Intégration non intrusive du code source eBPF tiers                         | 24.03               | openEuler 23.09     |
| Le pilote Big Language génère automatiquement des sondes d'observation eBPF | 24.09               | openEuler 24.09     |

#### Capacités de déploiement et d'intégration

| caractéristique                                                                                        | temps de libération | version finale                       |
| ------------------------------------------------------------------------------------------------------ | ------------------- | ------------------------------------ |
| Prend en charge l'amarrage de l'exportateur Prometheus                                                 | 22.12               | openEuler 22.03 SP1                  |
| Prend en charge l'amarrage sous la forme de fichiers journaux                                          | 22.12               | openEuler 22.03 SP1                  |
| Prise en charge de l'amarrage du client kafka                                                          | 22.12               | openEuler 22.03 SP1                  |
| Prise en charge de la capacité de surveillance de la sonde de changement dynamique de l'interface REST | 23.06               | openEuler 22.03 SP1, openEuler 23.09 |
