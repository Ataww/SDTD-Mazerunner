# SDTD-Mazerunner

## Description
Application en charge de générer les jobs spark au seins du cluster utilisant les librairies Spark et l'API Graphx de Spark

## Configuration
1. Scala installé sur la machine: http://www.scala-lang.org/
2. Sbt installé sur la machine: http://www.scala-sbt.org/

## Build

A réaliser à la racine de l'application
 
1. Compilation

    ```bash
    $ sbt compile
    ```  
2. Mise à jour des dépendances

    ```
    $ sbt update
    ```
    
3. Package (alias pour assembly)

    ```bash
    $ sbt package
    ```  
4. Déplacer les jars dans le dossier artifact pour déploiement
   ```
   $ cd ..
   $ ./move_artifacts
   ```
## Run application in cluster spark

1. Run 

    ```bash
    # Pour envoyer les sources sur le serveurs
    $ python3 deploy_application.py
     
    # Pour lancer le spark-submit (Vérifier que spark est lancer sur les serveurs)
    $ python3 start_application.py
    ``` 
    
## Problèmes courant
* Erreur de résolution des dépendances

 1. Supprimer le dossier ~/.ivy2/cache
 2. Relancer l'assembly
