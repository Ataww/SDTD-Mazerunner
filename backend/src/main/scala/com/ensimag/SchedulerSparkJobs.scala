package com.ensimag

/**
  * Created by julien on 06/12/16.
  */
object SchedulerSparkJobs {

  // Temps d'attente entre le lancement de jobs sur spark en millisecondes
  val waitTime = 2000
  // Récupération de la configuration pour spark
  val sc = SparkInit.getSparkContext()
  // Création d'un graph
  val graph = GraphTest.build(sc)


  def launchScheduler(): Unit = {
    while(true) {
      Thread.sleep(500)
      println("New Job Launch")
      JobSparkGraph.calculateNumberOfAirports(graph)
      JobSparkGraph.calculateNumberOfRoutes(graph)
    }

  }

}
