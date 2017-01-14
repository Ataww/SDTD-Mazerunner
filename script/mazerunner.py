#!/usr/bin/env python3

import configparser
import logging
import os
import subprocess
import sys


# Display error
def error_command(msg):
    logging.error(msg)
    logging.error("Launch command : 'python3 mazerunner.py --help' for see details")
    return


def launch_command():
    if 1 >= len(sys.argv):
        error_command(msg="Not enough arguments")
    elif 2 == len(sys.argv) and "--help" == sys.argv[1]:
        show_command()
    elif 2 == len(sys.argv) or 3 == len(sys.argv):
        action = check_action()
        if action == "":
            error_command(msg="Not valid action to execute : " + sys.argv[1])
        elif 3 == len(sys.argv):
            if check_server():
                call_method(action=action, serverName=sys.argv[2])
            else:
                error_command(msg=sys.argv[2] + " It is not a valid server name")
        else:
            call_method(action=action, serverName=None)

    else:
        error_command(msg="Too much argument")
    return


# Valid action
def check_action():
    action = ""
    if "--install" == sys.argv[1]:
        action = "INSTALL"
    elif "--reinstall" == sys.argv[1]:
        action = "REINSTALL"
    elif "--remove" == sys.argv[1]:
        action = "REMOVE"
    elif "--start" == sys.argv[1]:
        action = "START"
    elif "--stop" == sys.argv[1]:
        action = "STOP"
    elif "--restart" == sys.argv[1]:
        action = "RESTART"
    elif "--update" == sys.argv[1]:
        action = "UPDATE"
    elif "--installenv" == sys.argv[1]:
        action = "ENVIRONMENT"
    return action


# Permit to know if the server name is valid
def check_server():
    ip = lib.getIpServerName(config, sys.argv[2])
    if lib.hostIsUp(ip):
        return True
    return False


# Display help for launch command
def show_command():
    print("\n")
    print(lib.color.BOLD + "DESCRIPTION" + lib.color.END)
    print("     " + lib.color.UNDERLINE + "Install service on server:\n" + lib.color.END)
    print("         python3 mazerunner.py --install                (for all server)")
    print("         python3 mazerunner.py --install <servername>   (for a specific server)")
    print("\n")
    print("     " + lib.color.UNDERLINE + "Reinstall service on server:\n" + lib.color.END)
    print("         python3 mazerunner.py --reinstall                (for all server)")
    print("         python3 mazerunner.py --reinstall <servername>   (for a specific server)")
    print("\n")
    print("     " + lib.color.UNDERLINE + "Delete service on server:\n" + lib.color.END)
    print("         python3 mazerunner.py --remove                (for all server)")
    print("         python3 mazerunner.py --remove <servername>   (for a specific server)")
    print("\n")
    print("     " + lib.color.UNDERLINE + "Launch service on server:\n" + lib.color.END)
    print("         python3 mazerunner.py --start                (for all server)")
    print("         python3 mazerunner.py --start <servername>   (for a specific server)")
    print("\n")
    print("     " + lib.color.UNDERLINE + "Restart service on server:\n" + lib.color.END)
    print("         python3 mazerunner.py --restart                (for all server)")
    print("         python3 mazerunner.py --restart <servername>   (for a specific server)")
    print("\n")
    print("     " + lib.color.UNDERLINE + "Stop service on server:\n" + lib.color.END)
    print("         python3 mazerunner.py --stop                (for all server)")
    print("         python3 mazerunner.py --stop <servername>   (for a specific server)")
    print("\n")
    print("     " + lib.color.UNDERLINE + "Update file on server:\n" + lib.color.END)
    print("         python3 mazerunner.py --update                (for all server)")
    print("         python3 mazerunner.py --update <servername>   (for a specific server)")
    print("\n")
    print("     " + lib.color.UNDERLINE + "Define environment on server:\n" + lib.color.END)
    print("         python3 mazerunner.py --installenv                (for all server)")
    print("         python3 mazerunner.py --installenv <servername>   (for a specific server)")
    print("\n")
    print(lib.color.BOLD + "SERVER NAME" + lib.color.END)
    print("     " + lib.color.UNDERLINE + "Spark server:\n" + lib.color.END)
    print("         spark-1")
    print("         spark-2")
    print("         spark-3")
    print("         spark-4")
    print("\n")
    print("     " + lib.color.UNDERLINE + "Hdfs server:\n" + lib.color.END)
    print("         hdfs-1")
    print("         hdfs-2")
    print("         hdfs-3")
    print("         hdfs-4")
    print("\n")
    print("     " + lib.color.UNDERLINE + "Neo4j server:\n" + lib.color.END)
    print("         Neo4j-1")
    print("         Neo4j-2")
    print("         Neo4j-3")
    print("\n")
    print("     " + lib.color.UNDERLINE + "Rabbitmq server:\n" + lib.color.END)
    print("         rabbitmq-1")
    print("         rabbitmq-2")
    print("\n")
    print("©ensimag ")
    return


# launch commande in ssh
def call_method(action, serverName):

    if serverName is not None:
        directory = serverName.split('-')[0]
        ip = lib.getIpServerName(config, serverName)
    else:
        if action == "START":
            global_service.launch_component()
        elif action == "STOP":
            global_service.stop_component()
        elif action == "RESTART":
            global_service.stop_component()
            global_service.launch_component()
        elif action == "UPDATE":
            global_service.update_all_server()
        elif action == "REMOVE":
            global_service.remove_all_server()
        elif action == "INSTALL":
            global_service.install_all_server()
        elif action == "REINSTALL":
            global_service.remove_all_server()
            global_service.install_all_server()
        elif action == "ENVIRONMENT":
            global_service.install_basic_config()
        else:
            error_command("NOT YET IMPLEMENTED")
        return

    if action == "INSTALL":
        subprocess.run(['ssh', '-o', 'StrictHostKeyChecking=no', '-i', '~/.ssh/xnet',
                        'xnet@' + ip,
                        'source ~/.profile; cd SDTD-Mazerunner/script/' + directory + '; python3 install_' + directory + '.py'])
    elif action == "REINSTALL":
        subprocess.run(['ssh', '-o', 'StrictHostKeyChecking=no', '-i', '~/.ssh/xnet',
                        'xnet@' + ip,
                        'source ~/.profile; cd SDTD-Mazerunner/script/' + directory + '; python3 remove_' + directory + '.py'])
        subprocess.run(['ssh', '-o', 'StrictHostKeyChecking=no', '-i', '~/.ssh/xnet',
                        'xnet@' + ip,
                        'source ~/.profile; cd SDTD-Mazerunner/script/' + directory + '; python3 install_' + directory + '.py'])
    elif action == "REMOVE":
        subprocess.run(['ssh', '-o', 'StrictHostKeyChecking=no', '-i', '~/.ssh/xnet',
                        'xnet@' + ip,
                        'source ~/.profile; cd SDTD-Mazerunner/script/' + directory + '; python3 remove_' + directory + '.py'])
    elif action == "START":
        subprocess.run(['ssh', '-o', 'StrictHostKeyChecking=no', '-i', '~/.ssh/xnet',
                        'xnet@' + ip,
                        'source ~/.profile; cd SDTD-Mazerunner/script/' + directory + '; python3 launch_' + directory + '.py'])
    elif action == "STOP":
        subprocess.run(['ssh', '-o', 'StrictHostKeyChecking=no', '-i', '~/.ssh/xnet',
                        'xnet@' + ip,
                        'source ~/.profile; cd SDTD-Mazerunner/script/' + directory + '; python3 stop_' + directory + '.py'])
    elif action == "RESTART":
        subprocess.run(['ssh', '-o', 'StrictHostKeyChecking=no', '-i', '~/.ssh/xnet',
                        'xnet@' + ip,
                        'source ~/.profile; cd SDTD-Mazerunner/script/' + directory + '; python3 stop_' + directory + '.py'])
        subprocess.run(['ssh', '-o', 'StrictHostKeyChecking=no', '-i', '~/.ssh/xnet',
                        'xnet@' + ip,
                        'source ~/.profile; cd SDTD-Mazerunner/script/' + directory + '; python3 launch_' + directory + '.py'])
    elif action == "UPDATE":
        lib.updateFileServer(config=config, serverName=serverName)
    elif action == "ENVIRONMENT":
        subprocess.run(['ssh', '-o', 'StrictHostKeyChecking=no', '-i', '~/.ssh/xnet', 'xnet@' + ip,
                        'source ~/.profile; cd SDTD-Mazerunner/script/; python3 install_config_machine.py'])
    else:
        error_command("NOT YET IMPLEMENTED")

    return


if __name__ == '__main__':
    os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from script.lib import lib, global_service

    config = configparser.ConfigParser()
    config.read("conf.ini")
    logging.basicConfig(level=logging.INFO, format="%(asctime)s :: %(levelname)s :: %(message)s")
    print(lib.color.BOLD + lib.color.GREEN + " /$$      /$$")
    print("| $$$    /$$$")
    print("| $$$$  /$$$$  /$$$$$$  /$$$$$$$$  /$$$$$$   /$$$$$$  /$$  /$$  /$$$$$$$  /$$$$$$$   /$$$$$$   /$$$$$$")
    print("| $$ $$/$$ $$ |____  $$|____ /$$/ /$$__  $$ /$$__  $$| $$ | $$ | $$__  $$| $$__  $$ /$$__  $$ /$$__  $$")
    print("| $$  $$$| $$  /$$$$$$$   /$$$$/ | $$$$$$$$| $$  \__/| $$ | $$ | $$  \ $$| $$  \ $$| $$$$$$$$| $$  \__/")
    print("| $$\  $ | $$ /$$__  $$  /$$__/  | $$_____/| $$      | $$ | $$ | $$  | $$| $$  | $$| $$_____/| $$")
    print("| $$ \/  | $$|  $$$$$$$ /$$$$$$$$| $$$$$$$ | $$      | $$$$$$ /| $$  | $$| $$  | $$|  $$$$$$$| $$")
    print(
        "|__/     |__/ \_______/|________/ \_______/|__/       \______/ |__/  |__/|__/  |__/ \_______/|__/"
        + lib.color.END)
    launch_command()
