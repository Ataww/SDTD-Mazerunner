package JobOrchestration

import java.util.concurrent.TimeUnit

import com.rabbitmq.client.AMQP.BasicProperties
import com.rabbitmq.client._
import org.apache.spark.launcher.{SparkAppHandle, SparkLauncher}
import com.typesafe.config._
import com.typesafe.scalalogging.Logger
import org.apache.spark.launcher.SparkAppHandle.{Listener, State}
import org.apache.spark.{SparkConf, SparkContext}

import scala.util.control.Breaks

object JobOrchestration {

  val logger = Logger("Orchestrator")

  val conf: Config = ConfigFactory.load("JobOrchestration")
  val QUEUE_NAME: String = conf.getString("subscribe_queue_name")
  val EXCHANGE_NAME_TODO: String = conf.getString("exchange_name_todo")
  val EXCHANGE_NAME_DONE: String = conf.getString("exchange_name_done")
  val LOADBALANCER_HOST: String = conf.getString("loadbalancer_host")
  val LOADBALANCER_PORT: Int = conf.getInt("loadbalancer_port")
  val RMQ_USER: String = conf.getString("rabbitmq_user")
  val RMQ_PWD: String = conf.getString("rabbitmq_pwd")
  val MAINCLASS_LAUNCHER: String = conf.getString("launcher_main_class")
  val LAUNCHER_JAR: String = conf.getString("launcher_jarpath")

  val cf = new ConnectionFactory
  cf.setHost(LOADBALANCER_HOST)
  cf.setPort(LOADBALANCER_PORT)
  cf.setUsername(RMQ_USER)
  cf.setPassword(RMQ_PWD)
  cf.setExceptionHandler(new CustomExceptionHandler)

  val sparkConf: SparkConf = new SparkConf().set("spark.cores.max", "2")

  val context: SparkContext = new SparkContext(sparkConf)


  def main(args: Array[String]): Unit = {
    createChannel()
  }

  def createChannel(): Unit = {

    logger.info("Initializing channel")

    val connection: Connection = cf.newConnection

    val channel: Channel = connection.createChannel

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
        val payload = new String(body, "UTF-8")
        logger.info(" [x] Job to do for user '" + payload + "'")
        try {
          //TODO VOIR AVEC RAKOTO
          // Launch spark job and wait for it
          logger.info("Initializing computation job")
          val spark_home = System.getenv("SPARK_HOME")
          val stateListener = new Listener {
            override def infoChanged(handle: SparkAppHandle): Unit = {
              logger.debug("info changed")
            }

            override def stateChanged(handle: SparkAppHandle): Unit = {
              logger.info("State changed to " + handle.getState)
              handle.getState match {
                case State.FINISHED => sendDoneJob(body)
                case State.FAILED => handle.kill()
                case State.LOST => handle.kill()
                case State.KILLED => sendDoneJob(body)
                case State.CONNECTED => logger.info("connected")
                case State.RUNNING => logger.info("running")
                case State.SUBMITTED => logger.info("submitted")
                case State.UNKNOWN => logger.info("unknown")
              }
            }
          }
          val spark = new SparkLauncher()
            .setAppResource(LAUNCHER_JAR)
            .setMainClass(MAINCLASS_LAUNCHER)
            .addAppArgs(payload)
            .setSparkHome(spark_home)
            .setAppName("Job-" + payload)
            .setConf("spark.cores.max", "2")
            .startApplication(stateListener)
          logger.info("Job-" + payload + " launched")
        } catch {
          case e: Exception => logger.error(e.getMessage)
        }
      }

    }
    logger.info("RabbitMQ channel initialized")
    channel.basicConsume(QUEUE_NAME, true, consumer)
  }

  def sendDoneJob(user: Array[Byte]): Unit = {
    logger.info("job finished")
    val loop = new Breaks
    loop.breakable(
      for (i <- 0 to 10)
        try {
          val connection: Connection = cf.newConnection

          val channel: Channel = connection.createChannel
          // Declare exchange
          channel.exchangeDeclare(EXCHANGE_NAME_DONE, BuiltinExchangeType.FANOUT)
          channel.basicPublish(EXCHANGE_NAME_DONE, "", null, user)
          logger.info("Completion message sent")
          loop.break
        } catch {
          case e: Exception => logger.error(e.getMessage)
        })
  }
}