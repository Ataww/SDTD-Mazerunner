import Dependencies._


lazy val common = Seq(
  version := "1.0",
  scalaVersion := "2.11.8",
  organization := "fr.ensimag",
  test in assembly := {},
  libraryDependencies ++= dependencies,
  assemblyMergeStrategy in assembly := {
    case PathList(ps@_*) if ps.last endsWith ".conf" => MergeStrategy.concat
    case x =>
      val oldStrategy = (assemblyMergeStrategy in assembly).value
      oldStrategy(x)
  }
)

lazy val root = (project in file("."))
  .settings(common: _*)
  .aggregate(orchestrator, job)

lazy val orchestrator = (project in file("orchestrator"))
  .settings(common: _*)
  .settings(
    name := "SDTD-orchestrator",
    mainClass in assembly := Some("JobOrchestration.JobOrchestration"),
    assemblyJarName in assembly := "orchestrator.jar"
  )

lazy val job = (project in file("job"))
  .settings(common: _*)
  .settings(
    name := "SDTD-job",
    mainClass in assembly := Some("com.ensimag.ApplicationMain"),
    assemblyJarName in assembly := "sparkjob.jar"
  )

