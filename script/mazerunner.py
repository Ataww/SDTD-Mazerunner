#!/usr/bin/env python3

import configparser
import sys
import logging
from lib import getIpServerName, hostIsUp

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

# Permit to know if the server name is valide
def check_server():
    ip = getIpServerName(config, sys.argv[2])
    if hostIsUp(ip):
        return True
    return False

# Display help for launch commande
def show_commande():
    print("python3 mazerunner.py [OPTIONS] .... \n")
    print("Install all service on all server:")
    print("     python3 mazerunner.py -i")
    print("re-install all service on all server:")
    print("     python3 mazerunner.py -r")
    print("delete all service on all server:")
    print("     python3 mazerunner.py -d")
    print("Install service on specific server:")
    print("     python3 mazerunner.py -i <name_server>")
    print("re-install service on specific server:")
    print("     python3 mazerunner.py -r <name_server>")
    print("delete service on specific server:")
    print("     python3 mazerunner.py -d <name_server>")
    return


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(asctime)s :: %(levelname)s :: %(message)s")
    config = configparser.ConfigParser()
    config.read("conf.ini")
    launch_commande()
