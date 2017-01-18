package com.ensimag

import org.apache.spark.SparkConf
import org.apache.spark.SparkContext

/**
  * Created by julien on 06/12/16.
  */
object SparkInit {

  val conf = new SparkConf().setAppName("Mazerunner")
  val sc = new SparkContext(conf)

  def getSparkContext() ={
    sc
  }
}
