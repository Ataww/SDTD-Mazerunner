# SDTD-Mazerunner

## Description
Application en charge de générer les jobs spark au seins du cluster utilisant les librairies Spark et l'API Graphx de Spark

## Configuration
1. Scala installer sur la machine
2. Sbt installer sur la machine

## Build

A réaliser à la racine de l'application
 
1. Compile

    ```bash
    $ sbt compile
    ```  
2. Package

    ```bash
    $ sbt package
    ```  
## Run application in cluster spark

1. Run 

    ```bash
    # Pour envoyer les sources sur le serveurs
    $ python3 deploy_application.py
     
    # Pour lancer le spark-submit (Vérifier que spark est lancer sur les serveurs)
    $ python3 start_application.py
    ``` 