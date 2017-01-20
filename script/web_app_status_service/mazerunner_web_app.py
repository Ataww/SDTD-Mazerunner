#!/usr/bin/env python3

from flask import Flask
from flask import render_template
from flask import make_response
import subprocess
import os
import sys

# Initialise Flask
app = Flask(__name__)
app.debug = True


@app.route("/")
def index():
    print("aaa")
    render_option = {}
    render_option["title"] = "SDTD-Mazerunner"

    return render_template('index.html', render_option=render_option)


@app.route("/status_<string:service_name>/<int:id>")
def status_service(service_name, id):
    key = 'Master'
    if 'spark' in service_name:
        if id == 1 or id == 2:
            key = 'Master'
        else:
            key = 'Slaves'
    elif 'hdfs' in service_name:
        key = 'DataNode'
    isOk = check_function(name_service=service_name, key_name=key, host=service_name + '-' + str(id))
    if isOk:
        return_code = 200
    else:
        return_code = 404
    resp = make_response()
    resp.status_code = return_code
    return resp


@app.route("/start_<string:service_name>/<int:id>")
def start_service(service_name, id):
    subprocess.run(['ssh', '-o', 'StrictHostKeyChecking=no', '-i', '~/.ssh/xnet',
                    'xnet@' + service_name + '-' + str(id),
                    'source ~/.profile; cd SDTD-Mazerunner/script/' + service_name + '; python3 launch_' + service_name + '.py'])
    resp = make_response()
    resp.status_code = 200
    return resp


@app.route("/stop_<string:service_name>/<int:id>")
def stop_service(service_name, id):
    subprocess.run(['ssh', '-o', 'StrictHostKeyChecking=no', '-i', '~/.ssh/xnet',
                    'xnet@' + service_name + '-' + str(id),
                    'source ~/.profile; cd SDTD-Mazerunner/script/' + service_name + '; python3 stop_' + service_name + '.py'])
    resp = make_response()
    resp.status_code = 200
    return resp


if __name__ == "__main__":
    os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from global_server.scheduler_server import check_function

    # Change diretory to script one
    try:
        os.chdir(os.path.dirname(sys.argv[0]))
    except FileNotFoundError:
        pass

    app.run(port=8079, host='0.0.0.0')
