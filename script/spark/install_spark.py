#!/usr/bin/python

import os

url_master = '127.0.0.1'
port_master = '7070'
port_webui  = '8080'


# Function for install Spark and its environment
def install_spark():
	os.system(' echo "#############################"')
	os.system(' echo "####### Install Spark #######"')
	os.system(' echo "#############################"')
	os.system('rm spark-2.0.2-bin-hadoop2.7.tgz')
	os.system(' echo "[Info] Download Spark"')
	os.system('wget http://d3kbcqa49mib13.cloudfront.net/spark-2.0.2-bin-hadoop2.7.tgz')
	os.system('rm -rf spark')
	os.system('mkdir spark')
	os.system('tar xf spark-2.0.2-bin-hadoop2.7.tgz -C spark/')
	# TODO define the spark path
	os.system(' echo "#############################"')
	os.system(' echo "####### Launch Spark ########"')
	os.system(' echo "#############################"')
	#os.system('./spark/spark-2.0.2-bin-hadoop2.7/sbin/stop-master.sh')
	#os.system('./spark/spark-2.0.2-bin-hadoop2.7/sbin/start-master.sh -i '+url_master+' -p '+port_master+' --webui-port '+port_webui)
	#os.system('./spark/spark-2.0.2-bin-hadoop2.7/sbin/stop-slave.sh')
	#os.system('./spark/spark-2.0.2-bin-hadoop2.7/sbin/start-slave.sh spark://'+url_master+':'+port_master)
	return

install_spark()