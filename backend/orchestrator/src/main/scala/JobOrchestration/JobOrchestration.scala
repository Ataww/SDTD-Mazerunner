package JobOrchestration

import com.rabbitmq.client.AMQP.BasicProperties
import com.rabbitmq.client._
import org.apache.spark.launcher.SparkLauncher
import com.typesafe.config._
import org.apache.spark.{SparkConf, SparkContext}

import scala.util.control.Breaks

object JobOrchestration {

  val conf : Config = ConfigFactory.load("JobOrchestration")
  val QUEUE_NAME : String = conf.getString("subscribe_queue_name")
  val EXCHANGE_NAME_TODO : String = conf.getString("exchange_name_todo")
  val EXCHANGE_NAME_DONE : String = conf.getString("exchange_name_done")
  val LOADBALANCER_HOST : String = conf.getString("loadbalancer_host")
  val LOADBALANCER_PORT : Int = conf.getInt("loadbalancer_port")
  val RMQ_USER : String = conf.getString("rabbitmq_user")
  val RMQ_PWD : String = conf.getString("rabbitmq_pwd")
  val MAINCLASS_LAUNCHER : String = conf.getString("launcher_main_class")
  val LAUNCHER_JAR : String = conf.getString("launcher_jarpath")

  val cf = new ConnectionFactory
  cf.setHost(LOADBALANCER_HOST)
  cf.setPort(LOADBALANCER_PORT)
  cf.setUsername(RMQ_USER)
  cf.setPassword(RMQ_PWD)
  cf.setExceptionHandler(new CustomExceptionHandler)

  val sparkLauncher : SparkLauncher = new SparkLauncher()
    .setAppResource(LAUNCHER_JAR)
    .setMainClass(MAINCLASS_LAUNCHER)

  val sparkConf : SparkConf= new SparkConf().set("spark.cores.max","2")

  val context : SparkContext = new SparkContext(sparkConf)

  val connection : Connection = cf.newConnection

  val channel : Channel = connection.createChannel

  def main(args: Array[String]): Unit = {
    createChannel()
  }

  def createChannel() : Unit = {

    println("Initializing channel")

    // Declare exchange
    channel.exchangeDeclare(EXCHANGE_NAME_TODO, BuiltinExchangeType.FANOUT)

    // Declare queue
    channel.queueDeclare(QUEUE_NAME, false, false, false, null)

    // Queue Bind
    channel.queueBind(EXCHANGE_NAME_TODO, QUEUE_NAME, "")

    // Create Consummer
    val consumer = new DefaultConsumer(channel) {
      // Define callback function when receiving message
      override def handleDelivery(consumerTag: String, envelope: Envelope, properties: BasicProperties, body: Array[Byte]):
      Unit = {
        println(" [x] Job to do for user'" + new String(body, "UTF-8") + "'")
        try {
          //TODO VOIR AVEC RAKOTO
          // Launch spark job and wait for it
          println("Before launching")
          val payload = new String(body, "UTF-8")
          val spark_home = System.getenv("SPARK_HOME")
          val spark = sparkLauncher
            .setSparkHome(spark_home)
            .addAppArgs(payload)
            .setAppName("Job-" + payload)
            .setConf("spark.cores.max","2")
            .launch()
          println("Launch OK")
          spark.waitFor()
          println("WAIT OK")
          // Post message do say that job is finish
          sendDoneJob(body)
          println("Message send")
        } catch {
          case e: Exception => println(e)
        }
      }

    }
    println("RabbitMQ channel initialized")
    channel.basicConsume(QUEUE_NAME, true, consumer)
  }

  def sendDoneJob(user: Array[Byte]) : Unit = {
    val loop = new Breaks
    loop.breakable(
      for(i <- 0 to 10)
        try {
          // Declare exchange
          channel.exchangeDeclare(EXCHANGE_NAME_DONE, BuiltinExchangeType.FANOUT)
          channel.basicPublish(EXCHANGE_NAME_DONE, "", null, user)
          loop.break
        } catch{
          case e : Exception => println(e)
        })
  }
}