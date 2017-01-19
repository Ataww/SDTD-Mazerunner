import sbt._

object Dependencies {
  val sparkVersion : String = "2.0.2"
  val rabbitVersion : String = "4.0.0"
  val configVersion : String = "1.3.1"
  lazy val dependencies = Seq(
    "com.rabbitmq" % "amqp-client" % rabbitVersion % "compile",
    "org.apache.spark" % "spark-core_2.10" % sparkVersion % "provided",
    "org.apache.spark" % "spark-graphx_2.10" % sparkVersion % "provided",
    "com.typesafe" % "config" % configVersion % "compile"
  )
}