package com.ensimag

import org.apache.spark.graphx.Graph

/**
  * Created by julien on 06/12/16.
  */
object JobSparkGraph {

  def calculateNumberOfAirports(graph: Graph[String, Int]) {
    // How many airports?
    val numairports = graph.numVertices
    println(numairports)
  }

  def calculateNumberOfRoutes(graph: Graph[String, Int]) {
    // How many routes?
    val numroutes = graph.numEdges
    println(numroutes)
  }

  // Other possibilitie of JOB :

  //graph.vertices.collect.foreach(println)
  //graph.edges.collect.foreach(println)
  //graph.edges.filter { case Edge(src, dst, prop) => prop > 1000 }.collect.foreach(println)
  //graph.triplets.take(3).foreach(println)
  //graph.triplets.sortBy(_.attr, ascending=false).map(triplet =>
  //"Distance " + triplet.attr.toString + " from " + triplet.srcAttr + " to " + triplet.dstAttr + ".").collect.foreach(println)

}
