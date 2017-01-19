package com.ensimag

import org.apache.spark.graphx.Graph
import org.apache.spark.util.IntParam
// import classes required for using GraphX
import org.apache.spark.graphx._
import org.apache.spark.graphx.util.GraphGenerators
import sys.process._

/**
  * Created by julien on 06/12/16.
  */
object JobSparkGraph {

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

}
