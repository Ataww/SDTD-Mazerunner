
lazy val common = Seq(
  version := "1.0",
  scalaVersion := "2.12.1"
)

val deps = Seq(
  "com.rabbitmq" % "amqp-client" % "4.0.0",
  "org.apache.spark" % "spark-core_2.10" % "2.0.2" % "compile",
  "org.apache.spark" % "spark-graphx_2.10" % "2.0.2" % "compile",
  "com.typesafe" % "config" % "1.3.1"

)

lazy val root = (project in file(".")).settings(common: _*).settings(
  name := "SDTD-Mazerunner-Backend",
  libraryDependencies ++= deps

)