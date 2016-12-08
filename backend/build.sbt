lazy val common = Seq(
  version := "1.0",
  scalaVersion := "2.10.4"
)

lazy val deps = Seq(
  "org.apache.spark" % "spark-core_2.10" % "2.0.2",
  "org.apache.spark" % "spark-graphx_2.10" % "2.0.2",
  "com.rabbitmq" % "amqp-client" % "4.0.0"
)

lazy val root = (project in file(".")).settings(common: _*).settings(
  name := "SDTD-Mazerunner-Backend",
  libraryDependencies ++= deps
)