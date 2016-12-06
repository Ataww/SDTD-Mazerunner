package com.ensimag

import org.apache.spark._

/**
  * Created by julien on 06/12/16.
  */
object SparkInit {

  val conf = new SparkConf().setAppName("Mazerunner").setMaster("local[*]")
  val sc = new SparkContext(conf)

  def getSparkContext() ={
    sc
  }
}
