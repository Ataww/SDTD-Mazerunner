package JobOrchestration

import java.io._

import com.rabbitmq.client.AMQP.BasicProperties
import com.rabbitmq.client.{BuiltinExchangeType, ConnectionFactory, DefaultConsumer, Envelope}
import org.apache.spark.launcher.SparkLauncher
import com.typesafe.config._
import org.apache.spark.SparkContext

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
  val LAUNCHER_MASTER : String = conf.getString("launcher_masters")

  val cf = new ConnectionFactory
  cf.setHost(LOADBALANCER_HOST)
  cf.setPort(LOADBALANCER_PORT)
  cf.setUsername(RMQ_USER)
  cf.setPassword(RMQ_PWD)

  val sparkLauncher = new SparkLauncher()
    .setAppResource(LAUNCHER_JAR)
    .setMainClass(MAINCLASS_LAUNCHER)
    .setMaster(LAUNCHER_MASTER)

  val context = new SparkContext()

  def main(args: Array[String]): Unit = {


    // Create connection
    val conn = cf.newConnection

    // Get channel
    val channel = conn.createChannel

    // Declare exchange
    val exchange = channel.exchangeDeclare(EXCHANGE_NAME_TODO, BuiltinExchangeType.FANOUT)

    // Declare queue
    val queue = channel.queueDeclare(QUEUE_NAME, false, false, false, null)

    // Queue Bind
    channel.queueBind(EXCHANGE_NAME_TODO, QUEUE_NAME, "")

    // Create Consummer
    val consumer = new DefaultConsumer(channel) {
      // Define callback function when recivied message
      override def handleDelivery(consumerTag: String, envelope: Envelope, properties: BasicProperties, body: Array[Byte]):
      Unit = {
        println(" [x] Job to do for user'" + new String(body, "UTF-8") + "'")
        try {
          //TODO VOIR AVEC RAKOTO
          // Launch spark job and wait for it
          val payload = new String(body, "UTF-8")
          val spark_home = System.getenv("SPARK_HOME")
          val spark = sparkLauncher
              .setSparkHome(spark_home)
            .addAppArgs(payload)
            .setAppName("Job-"+payload)
            .launch()
          spark.waitFor()

          // Post message do say that job is finish
          sendDoneJob(body)

          /*val err = spark.getErrorStream
          val fos = new FileOutputStream("/home/xnet/nath/err.txt")
          println("Spark job fired up")
          spark.waitFor()
          var byte = new Array[Byte](1024)
          var read = 0
          while (read != -1) {
            read = err.read(byte);
            fos.write(byte,0,read)
          }
          println("status: "+ spark.exitValue())
          println("Spark job finished")
        } catch {
          case e: Exception => println(e)
        }*/

        } catch { case  e: Exception => println(e) }
      }
    }
    channel.basicConsume(QUEUE_NAME, true, consumer)
  }

  def sendDoneJob(user: Array[Byte]) : Unit = {

    // Create connection
    val conn = cf.newConnection

    // Get channel
    val channel = conn.createChannel

    // Declare exchange
    val exchange = channel.exchangeDeclare(EXCHANGE_NAME_DONE, BuiltinExchangeType.FANOUT)

    channel.basicPublish(EXCHANGE_NAME_DONE, "", null, user)
  }
}