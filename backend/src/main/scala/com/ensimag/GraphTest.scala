package com.ensimag

import org.apache.spark.SparkContext
import org.apache.spark.graphx.{Edge, Graph}

/**
  * Created by julien on 06/12/16.
  */
object GraphTest {

  val vertices=Array((1L, ("SFO")),(2L, ("ORD")),(3L,("DFW")))
  val edges = Array(Edge(1L,2L,1800),Edge(2L,3L,800),Edge(3L,1L,1400))

  def build(sc: SparkContext) = {
    val vRDD= sc.parallelize(vertices)
    val eRDD= sc.parallelize(edges)
    val graph = Graph(vRDD,eRDD)
    graph
  }

}
