package JobOrchestration

import com.rabbitmq.client._

/**
  * Created by Ataww on 17/01/2017.
  */
class CustomExceptionHandler extends ExceptionHandler {
  override def handleUnexpectedConnectionDriverException(conn: Connection, exception: Throwable): Unit = {
    conn.close()
    JobOrchestration.createChannel()
  }

  override def handleConsumerException(channel: Channel, exception: Throwable, consumer: Consumer, consumerTag: String, methodName: String): Unit = {
    channel.close()
    JobOrchestration.createChannel()
  }

  override def handleBlockedListenerException(connection: Connection, exception: Throwable): Unit = {
    connection.close()
    JobOrchestration.createChannel()
  }

  override def handleChannelRecoveryException(ch: Channel, exception: Throwable): Unit = {
    ch.close()
    JobOrchestration.createChannel()
  }

  override def handleFlowListenerException(channel: Channel, exception: Throwable): Unit = {
    channel.close()
    JobOrchestration.createChannel()
  }

  override def handleReturnListenerException(channel: Channel, exception: Throwable): Unit = {
    channel.close()
    JobOrchestration.createChannel()
  }

  override def handleTopologyRecoveryException(conn: Connection, ch: Channel, exception: TopologyRecoveryException): Unit = {
    conn.close()
    JobOrchestration.createChannel()
  }

  override def handleConfirmListenerException(channel: Channel, exception: Throwable): Unit = {
    channel.close()
    JobOrchestration.createChannel()
  }

  override def handleConnectionRecoveryException(conn: Connection, exception: Throwable): Unit = {
    conn.close()
    JobOrchestration.createChannel()
  }
}
