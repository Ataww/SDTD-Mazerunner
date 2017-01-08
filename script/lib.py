#!/usr/bin/env python3

import os


class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


# Recover all ip for one component. Return format ip
def getHostsByKey(config, key):
    hosts = config.get(key, "hosts").split(',')
    index = 0
    for host in hosts:
        hosts[index] = host.strip(' \n')
        index += 1
    return hosts


# Function who return the ip of the current machine
def getIp():
    ip = os.popen('ifconfig ens3 | grep "inet ad" | cut -f2 -d: | awk \'{print $1}\'', "r").read()
    ip = ip.replace('\n', '')
    return ip


# Check if String il already present in the file
def isAlreadyAdd(pathFile, string):
    file = open(pathFile)
    for line in file:
        if string in line:
            return True
    return False


def deleteLineWithString(pathFile, stringResearch):
    contenu = ""
    fichier = open(pathFile, "r")
    for ligne in fichier:
        if not (stringResearch in ligne):
            contenu += ligne
    fichier.close()

    fichier = open('tmp.txt', 'w')
    fichier.write(contenu)
    fichier.close()
    os.system('sudo mv tmp.txt /etc/hosts >> /dev/null 2>&1')
    return


# Function for check host
def hostIsUp(host):
    if os.system('ping -c 1 ' + host + ' >> /dev/null 2>&1'):
        return False
    return True


# Function for recover ip by using server name
def getIpServerName(config, serverName):
    ip = ""
    value = serverName.split('-')
    if len(value) == 2:
        try:
            hosts = config.get(value[0], "hosts").split(',')
            ip = hosts[int(value[1]) - 1].strip(' \n')
        except:
            return ip
    return ip
