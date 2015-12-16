#!/usr/bin/python
from kazoo.client import KazooClient, KazooState
import sys
import argparse

zkip = "127.0.0.1"
zkport = 3000

current_path = "/"

def exec_ls(path = None):
    if path != None:
        ls = zkclient.get_children(path)
    else:
        ls = zkclient.get_children(current_path)
    print ls

def exec_pwd(*args):
    print current_path

def exec_help(*args):
    for key, value in cmd_map.items():
        print key

def exec_del(*args):
    recursive = False
    for arg in args:
        if arg == "-r":
            recursive = True
    for arg in args:
        if arg.starts_with("-"):
            continue
        if arg.starts_with("/"):
            node_path = arg
        else:
            node_path = os.path.join(current_path, arg)
        zkclient.delete(arg, recursive = recursive)

cmd_map = {"ls": exec_ls,
            "pwd": exec_pwd,
            "help": exec_help}

def exec_command(cmd_line):
    words = cmd_line.split()
    cmd = words[0]
    args = [words[i] for i in range(1, len(words))]
    if not cmd_map.has_key(cmd):
        print "Command not found!"
        return False
    cmd_func = cmd_map[cmd]
    cmd_func(*args)
    #print "cmd: %s, args %s" % (cmd, args)

def command_loop(endpoint):
    while True:
        cmd_line = raw_input("zookeeper:" + endpoint + "\>")
        cmd_line = cmd_line.strip()
        if cmd_line == "":
            continue
        elif cmd_line == "quit" or cmd_line == "exit":
            break
        exec_command(cmd_line)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-z", "--zkip", dest="zkip", required=False)
    parser.add_argument("-p", "--port", dest="port", type=int, required=False)
    args = parser.parse_args()
    if args.zkip != None:
        zkip = args.zkip
    if args.port != None:
        zkport = args.port

    endpoint = zkip + ":" + str(zkport)

    zkclient = KazooClient(hosts=endpoint)
    zkclient.start()

    command_loop(endpoint)
    #result = zkclient.get_children("/")
    #print result

    zkclient.stop()
