# SDTD-Mazerunner

## Description

Stack comprenant les outils :
- GraphX
- Spark
- RabbitMQ
- Neo4J
- HDFS

## Deploiment

#### Start the deployment

```bash
    $ ./launch_deployment
```

## Fonctionnement

#### Start all services

```bash
    $ ./start_services
```

#### Stop all services

```bash
    $ ./stop_services
```

## Configuration

La répartition des adresses ip pour les services se fait dans le fichier conf.ini

```
    [hdfs]
    hosts: 149.202.161.176, 149.202.170.223, 149.202.170.208
    
    [spark]
    hosts: 149.202.161.176, 149.202.170.223, 149.202.170.208
    
    [neo4j]
    hosts: 149.202.170.185, 149.202.170.194, 149.202.161.163
    
    [rabbitmq]
    hosts: 149.202.161.167, 149.202.161.163
```