import sbt._

object Dependencies {
  val sparkVersion : String = "2.0.2"
  val sparkScalaVersion : String = "2.11"
  val rabbitVersion : String = "4.0.0"
  val configVersion : String = "1.3.1"
  lazy val dependencies = Seq(
    "com.rabbitmq" % "amqp-client" % rabbitVersion % "compile",
    "org.apache.spark" % ("spark-core_"+sparkScalaVersion) % sparkVersion % "provided",
    "org.apache.spark" % ("spark-graphx_"+sparkScalaVersion) % sparkVersion % "provided",
    "com.typesafe" % "config" % configVersion % "compile",
    "com.typesafe.scala-logging" %% "scala-logging" % "3.5.0" % "compile"
  )
}