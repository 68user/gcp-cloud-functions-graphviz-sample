#!/usr/bin/python3

import sys
import os
import subprocess

from flask import escape, helpers

def run_dot(dotfile, imgfile):
    os.system("tar xfp ./graphviz.tar -C /tmp")

    cmd = "/tmp/graphviz/bin/dot -Kdot -Tpng {} -o {}".format(dotfile, imgfile)
    res = subprocess.run(cmd.split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("returncode["+str(res.returncode)+"]", file=sys.stderr)

    buflist = str(res.stdout).split("\\n")
    for buf in buflist:
        print("stdout["+buf+"]", file=sys.stderr)
    buflist = str(res.stderr).split("\\n")
    for buf in buflist:
        print("stderr["+buf+"]", file=sys.stderr)

    if res.returncode != 0:
        raise Exception("dot failed. cmd["+cmd+"]")


def do_graphviz(request):
    dotfile = "sample.dot"
    imgfile = "/tmp/out.png"
    run_dot(dotfile, imgfile)

    f = open(imgfile, "rb")
    response = helpers.make_response(f.read())
    response.headers["Content-type"] = "Image"
    return response

if __name__ == '__main__':
    run_dot("sample.dot", "dummy.png")
