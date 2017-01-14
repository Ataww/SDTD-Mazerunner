package sparkjob

import java.io.{File, FileWriter}

import org.apache.spark.{SparkConf, SparkContext}

import scala.util.Random

/**
  * Created by Ataww on 14/01/2017.
  */
object SparkJob {
  def main(args: Array[String]): Unit = {
    val conf = new SparkConf()
    val sc = new SparkContext(conf)
    val NUM_SAMPLES = Random.nextInt(100) + 1;

    val count = sc.parallelize(1 to NUM_SAMPLES).map{i =>
      val x = Math.random()
      val y = Math.random()
      if (x*x + y*y < 1) 1 else 0
    }.reduce(_ + _)
    val fw = new FileWriter(new File("/home/xnet/nath/out.txt"))
    val res = "Pi is roughly " + 4.0 * count / NUM_SAMPLES
    fw.write(res)
    fw.flush()
    fw.close()
  }
}
