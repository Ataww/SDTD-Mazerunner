package com.ensimag

import com.typesafe.scalalogging.Logger
import org.apache.spark.graphx.Graph
// import classes required for using GraphX
import org.apache.spark.graphx._

/**
  * Created by julien on 06/12/16.
  */
object ApplicationMain {

  val logger = Logger("sparkjob-main")

  case class MusicTaste(idUtilisateur: Long, nomUtilisateur: String, relationAime: String, idTitre: String) extends java.io.Serializable

  def main(args: Array[String]) = {
    val sc = SparkInit.getSparkContext()
    val username = args(0)
    logger.info("Computing recommendations for user  " + username)


    def parseMusicTaste(str: String): MusicTaste = {
      val line = str.split(",")
      // Be careful : we drop the first character of idTitre because GraphX can't generate vertex with non-number ID
      // TODO : Add it at the end of the treatment
      MusicTaste(line(0).toLong, line(1), line(2), line(3).drop(1))
    }

    val textRDD = sc.textFile("hdfs:////jobs_to_do/" + username + ".txt")
    logger.info("Subgraph received")
    val musicTasteRDD = textRDD.map(parseMusicTaste).cache()

    val users = musicTasteRDD.map(music => (music.idUtilisateur, music.nomUtilisateur)).distinct

    val nowhere = "nowhere"

    val aime = musicTasteRDD.map(music => ((music.idUtilisateur, music.idTitre), music.relationAime))

    val vertices = users.map { case (idUtilisateur, name) => (idUtilisateur -> name) }.collect
    val edges = aime.map {
      case ((idUtilisateur, idTitre), aime) => Edge(idUtilisateur.toLong, idTitre.toLong, aime)
    }

    val vertexRDD = sc.parallelize(vertices)

    val graph = Graph(vertexRDD, edges, nowhere)

    logger.info(" Calculating music recommendations for user " + username)
    JobSparkGraph.calculateRecommendations(graph, username)
  }

}
