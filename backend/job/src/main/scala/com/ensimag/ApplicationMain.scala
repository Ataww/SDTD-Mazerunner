package com.ensimag

import org.apache.spark.graphx.Graph
import org.apache.spark.util.IntParam
// import classes required for using GraphX
import org.apache.spark.graphx._
import org.apache.spark.graphx.util.GraphGenerators

/**
  * Created by julien on 06/12/16.
  */
object ApplicationMain {

  def main(args: Array[String]): Unit = {

    // Récupération de la configuration pour spark
    val sc = SparkInit.getSparkContext()

    case class MusicTaste(idUtilisateur: Long, nomUtilisateur: String, relationAime: String, idTitre: String)

    def parseMusicTaste(str: String): MusicTaste = {
      val line = str.split(",")
      // Be careful : we drop the first character of idTitre because GraphX can't generate vertex with non-number ID
      // TODO : Add it at the end of the treatment
      MusicTaste( line(0).toLong, line(1), line(2), line(3).drop(1))
    }

    val textRDD = sc.textFile("hdfs:////jobs_to_do/" + args(0) + ".txt")

    val musicTasteRDD = textRDD.map(parseMusicTaste).cache()

    val users = musicTasteRDD.map(music => (music.idUtilisateur, music.nomUtilisateur)).distinct

    val nowhere = "nowhere"

    val aime = musicTasteRDD.map(music => ((music.idUtilisateur, music.idTitre), music.relationAime))

    val vertices = users.map { case (idUtilisateur, name) => (idUtilisateur -> name) }.collect
    val edges = aime.map {
      case ((idUtilisateur, idTitre), aime) =>Edge(idUtilisateur.toLong, idTitre.toLong, aime) }

    val vertexRDD = sc.parallelize(vertices)

    val graph = Graph(vertexRDD, edges, nowhere)

    println("New Job Launch : Calculate music recommendations for the actual user")
    JobSparkGraph.calculateRecommendations(graph, args(0))

  }
}
