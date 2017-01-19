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
    subprocess.run(['python3', 'mazerunner.py', '--start'], cwd=os.getcwd())

    # Not Use because block the script
    # subprocess.run(['python3', 'deploy_website.py', 'run'],
    #               cwd=os.getcwd().replace('/script', '/application/script'))
    # subprocess.run(['python3', 'start_application.py'], cwd=os.getcwd().replace('/script', '/backend/script'))
    return


if __name__ == '__main__':
    launch_deployement()
