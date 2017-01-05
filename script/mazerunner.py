#!/usr/bin/env python3

import configparser
import sys
import os, logging, coloredlogs
from lib import getIpServerName, hostIsUp, color

# Display error
def error_commande(msg):
    logging.error(msg)
    logging.error("Launch command : 'python3 mazerunner.py --help' for see details")
    return


def launch_commande():
    if 1 >= len(sys.argv):
        error_commande("Not enough arguments")
    elif 2 == len(sys.argv) and "--help" == sys.argv[1]:
        show_commande()
    elif 2 == len(sys.argv) or 3 == len(sys.argv):
        action = check_action()
        if action == "":
            error_commande("Not valid action to execute : " + sys.argv[1])
        elif 3 == len(sys.argv):
            if check_server():
                logging.info("Launch " + action + " on server : " + sys.argv[2])
            else:
                error_commande(sys.argv[2] + " It is not a valid server name")
        else:
            logging.info("Launch " + action + " on all server")

    else:
        error_commande("Too much argument")
    return

# Valid action
def check_action():
    action = ""
    if "-i" == sys.argv[1]:
        action = "INSTALL"
    elif "-r" == sys.argv[1]:
        action = "REINSTALL"
    elif "-d" == sys.argv[1]:
        action = "DELETE"
    return action

# Permit to know if the server name is valid
def check_server():
    ip = getIpServerName(config, sys.argv[2])
    if hostIsUp(ip):
        return True
    return False

# Display help for launch commande
def show_commande():
    print("\n")
    print(color.BOLD+"DESCRIPTION"+color.END)
    print("     "+color.UNDERLINE+"Install service server:\n"+color.END)
    print("         python3 mazerunner.py -i                (for all server)")
    print("         python3 mazerunner.py -i <servername>   (for a specific server)")
    print("\n")
    print("     "+color.UNDERLINE+"Reinstall service server:\n"+color.END)
    print("         python3 mazerunner.py -r                (for all server)")
    print("         python3 mazerunner.py -r <servername>   (for a specific server)")
    print("\n")
    print("     "+color.UNDERLINE+"Delete service server:\n"+color.END)
    print("         python3 mazerunner.py -d                (for all server)")
    print("         python3 mazerunner.py -d <servername>   (for a specific server)")
    print("\n")
    print(color.BOLD+"SERVER NAME"+color.END)
    print("     "+color.UNDERLINE+"Spark server:\n"+color.END)
    print("         spark-1")
    print("         spark-2")
    print("         spark-3")
    print("         spark-4")
    print("\n")
    print("     "+color.UNDERLINE+"Hdfs server:\n"+color.END)
    print("         hdfs-1")
    print("         hdfs-2")
    print("         hdfs-3")
    print("         hdfs-4")
    print("\n")
    print("     "+color.UNDERLINE+"Neo4j server:\n"+color.END)
    print("         Neo4j-1")
    print("         Neo4j-2")
    print("         Neo4j-3")
    print("\n")
    print("     "+color.UNDERLINE+"Rabbitmq server:\n"+color.END)
    print("         rabbitmq-1")
    print("         rabbitmq-2")
    print("\n")
    print("©ensimag ")
    return


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read("conf.ini")
    os.environ["COLOREDLOGS_LOG_FORMAT"] = "[%(hostname)s] %(asctime)s - %(levelname)s - %(message)s"
    coloredlogs.install(level='DEBUG')
    print(color.BOLD+color.GREEN+" /$$      /$$")
    print("| $$$    /$$$")
    print("| $$$$  /$$$$  /$$$$$$  /$$$$$$$$  /$$$$$$   /$$$$$$  /$$  /$$  /$$$$$$$  /$$$$$$$   /$$$$$$   /$$$$$$")
    print("| $$ $$/$$ $$ |____  $$|____ /$$/ /$$__  $$ /$$__  $$| $$ | $$ | $$__  $$| $$__  $$ /$$__  $$ /$$__  $$")
    print("| $$  $$$| $$  /$$$$$$$   /$$$$/ | $$$$$$$$| $$  \__/| $$ | $$ | $$  \ $$| $$  \ $$| $$$$$$$$| $$  \__/")
    print("| $$\  $ | $$ /$$__  $$  /$$__/  | $$_____/| $$      | $$ | $$ | $$  | $$| $$  | $$| $$_____/| $$")
    print("| $$ \/  | $$|  $$$$$$$ /$$$$$$$$| $$$$$$$ | $$      | $$$$$$ /| $$  | $$| $$  | $$|  $$$$$$$| $$")
    print("|__/     |__/ \_______/|________/ \_______/|__/       \______/ |__/  |__/|__/  |__/ \_______/|__/"+color.END)
    launch_commande()
