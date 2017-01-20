#!/usr/bin/env python3


import subprocess
import os


def launch_deployement():
    subprocess.run(['python3', 'mazerunner.py', '--update'], cwd=os.getcwd())
    subprocess.run(['python3', 'mazerunner.py', '--update-api-mazerunner'], cwd=os.getcwd())
    subprocess.run(['python3', 'deploy_website.py'], cwd=os.getcwd().replace('/script', '/application/script'))
    subprocess.run(['python3', 'deploy_application.py'], cwd=os.getcwd().replace('/script', '/backend/script'))
    subprocess.run(['python3', 'mazerunner.py', '--installenv'], cwd=os.getcwd())
    subprocess.run(['python3', 'mazerunner.py', '--install'], cwd=os.getcwd())
    subprocess.run(['python3', 'deploy_website.py', 'env'],
                   cwd=os.getcwd().replace('/script', '/application/script'))
    subprocess.run(['python3', 'mazerunner.py', '--start', 'zookeeper-1'], cwd=os.getcwd())
    subprocess.run(['python3', 'mazerunner.py', '--start', 'zookeeper-2'], cwd=os.getcwd())
    subprocess.run(['python3', 'mazerunner.py', '--start', 'zookeeper-3'], cwd=os.getcwd())
    subprocess.run(['python3', 'mazerunner.py', '--start', 'spark-1'], cwd=os.getcwd())
    subprocess.run(['python3', 'mazerunner.py', '--start', 'spark-2'], cwd=os.getcwd())
    subprocess.run(['python3', 'mazerunner.py', '--start', 'spark-3'], cwd=os.getcwd())
    subprocess.run(['python3', 'mazerunner.py', '--start', 'spark-4'], cwd=os.getcwd())
    subprocess.run(['python3', 'mazerunner.py', '--start', 'hdfs-1'], cwd=os.getcwd())
    subprocess.run(['python3', 'mazerunner.py', '--start', 'rabbitmq-1'], cwd=os.getcwd())
    subprocess.run(['python3', 'mazerunner.py', '--start', 'rabbitmq-2'], cwd=os.getcwd())
    subprocess.run(['python3', 'mazerunner.py', '--start', 'neo4j-1'], cwd=os.getcwd())
    subprocess.run(['python3', 'mazerunner.py', '--start', 'neo4j-2'], cwd=os.getcwd())
    subprocess.run(['python3', 'mazerunner.py', '--start', 'neo4j-3'], cwd=os.getcwd())
    subprocess.run(['python3', 'mazerunner.py', '--globalstatus_start', 'webapp-1'], cwd=os.getcwd())
    subprocess.run(['python3', 'mazerunner.py', '--globalserver_start', 'webapp-1'], cwd=os.getcwd())

    # Not Use because block the script
    # subprocess.run(['python3', 'deploy_website.py', 'run'],
    #               cwd=os.getcwd().replace('/script', '/application/script'))
    # subprocess.run(['python3', 'start_application.py'], cwd=os.getcwd().replace('/script', '/backend/script'))
    return


if __name__ == '__main__':
    launch_deployement()
