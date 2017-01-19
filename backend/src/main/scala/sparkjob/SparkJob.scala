package sparkjob

import java.io.{File, FileWriter}

import org.apache.spark.{SparkConf, SparkContext}

import scala.util.Random

import org.apache.spark.graphx.Graph
import org.apache.spark.util.IntParam
// import classes required for using GraphX
import org.apache.spark.graphx._
import org.apache.spark.graphx.util.GraphGenerators
import sys.process._

import org.apache.spark.SparkConf
import org.apache.spark.SparkContext


/**
  * Created by Ataww on 14/01/2017.
  */
object SparkJob extends App {

  def calculateRecommendations(graph: Graph[String, String], username: String) {
    /////// Linking the music from other users to the actual user ///////

    // Récupération de la configuration pour spark
    val sc = SparkInit.getSparkContext()

    // Generate random seed
    val r = scala.util.Random
    val seed = r.nextLong()

    // We simply choose random music liked by other users
    val music_results = graph.collectNeighbors(EdgeDirection.In).takeSample(false, 30, seed)

    // Add to id_titre the character t and map the result into an RDD
    val lines = sc.parallelize(music_results.map {case (id, users) => "t" + id.toString})

    // Saving result to HDFS into one file (called part-00000)
    //TODO : HDFS Host has to be a variable
    lines.repartition(1).saveAsTextFile("hdfs:////jobs_done/" + username)

  }

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
    calculateRecommendations(graph, args(0))

}
