
lazy val common = Seq(
  version := "1.0",
  scalaVersion := "2.12.1",
  test in assembly := {}
)

val deps = Seq(
  "com.rabbitmq" % "amqp-client" % "4.0.0" % "compile",
  "org.apache.spark" % "spark-core_2.10" % "2.0.2" % "provided",
  "org.apache.spark" % "spark-graphx_2.10" % "2.0.2" % "provided",
  "com.typesafe" % "config" % "1.3.1" % "compile"

)

lazy val root = (project in file(".")).settings(common: _*).settings(
  name := "SDTD-Mazerunner-Backend",
  libraryDependencies ++= deps
).settings(
  mainClass in assembly := Some("JobOrchestration.JobOrchestration"),
  assemblyJarName in assembly := "orchestrator-sbt.jar",
  assemblyMergeStrategy in assembly := {
    case PathList("javax", "servlet", xs @ _*)         => MergeStrategy.first
    case PathList("javax", "transaction", xs @ _*)     => MergeStrategy.first
    case PathList("javax", "mail", xs @ _*)     => MergeStrategy.first
    case PathList("javax", "activation", xs @ _*)     => MergeStrategy.first
    case "application.conf" => MergeStrategy.concat
    case x =>
      val oldStrategy = (assemblyMergeStrategy in assembly).value
      oldStrategy(x)
  }
)