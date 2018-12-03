#!/usr/bin/env python3
import pexpect
import os
import sys
import re


def execute_command(cmd, element=None, element_exists=False):
    child.sendline(cmd)
    child.expect("/>")
    if "error response" in child.before.decode():
        print("Error in cmd: %s" % cmd)
        exit(1)
    ls_tree = cmd.split(" ")[0]
    if ls_tree and element:
        child.sendline("ls %s" % ls_tree)
        child.expect("/>")
        print("child: %s" % child.before.decode())
        if element_exists:
            if element not in child.before.decode():
                print("Element %s not in list" % element)
                exit(1)
        else:
            if element in child.before.decode():
                print("Element %s is in list" % element)
                exit(1)


if __name__ == "__main__":
    socket = "/var/tmp/spdk.sock"
    if len(sys.argv) == 3:
        socket = sys.argv[2]
    testdir = os.path.dirname(os.path.realpath(sys.argv[0]))
    child = pexpect.spawn(os.path.join(testdir, "../../scripts/spdkcli.py") + " -s %s" % socket)
    child.expect(">")
    child.sendline("cd /")
    child.expect("/>")

    cmd_lines = sys.argv[1].strip().split("\n")
    for line in cmd_lines:
        data = line.strip()
        p = re.compile('\'(.*?)\'')
        cmd = p.findall(data)
        if data[-1] != "\'":
            cmd.append(data.rsplit(" ", 1)[1].strip())
            if cmd[-1] == "False":
                cmd[-1] = False
            else:
                cmd[-1] = True
        else:
            cmd.append(False)
        print("Executing command: %s" % cmd)
        execute_command(*cmd[0:3])
