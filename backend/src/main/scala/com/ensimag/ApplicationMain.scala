package com.ensimag

/**
  * Created by julien on 06/12/16.
  */
object ApplicationMain {

  def main(args: Array[String]): Unit = {
    SchedulerSparkJobs.launchScheduler()
  }
}
