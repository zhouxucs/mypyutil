#!/usr/bin/python
import kazoo
from kazoo.client import KazooClient, KazooState
import sys
import argparse
import os

zkip = "127.0.0.1"
zkport = 3000

current_path = "/"
def set_current_path(path):
    global current_path
    current_path = path

def get_full_path(path):
    if not path.startswith("/"):
        path = os.path.join(current_path, path)
    return path

def exec_ls(path = None):
    if path != None:
        ls = zkclient.get_children(path)
    else:
        ls = zkclient.get_children(current_path)
    for node in ls:
        print node

def exec_pwd(*args):
    print current_path

def exec_help(*args):
    for key, value in cmd_map.items():
        print key

def del_star(full_path, recursive=False):
    child_list = zkclient.get_children(full_path)
    for child in child_list:
        child_node = os.path.join(full_path, child)
        if child_node.startswith("/zookeeper"):
            continue
        zkclient.delete(child_node, recursive=recursive)

def exec_del(*args):
    recursive = False
    for arg in args:
        if arg == "-r":
            recursive = True
    for arg in args:
        if arg.startswith("-"):
            continue
        try:
            if arg == "*":
                del_star(current_path, recursive=recursive)
                continue
            node_path = get_full_path(arg)
            if node_path == "/" or node_path.startswith("/zookeeper"):
                print "System node(%s) cannot be deleted" % arg
                continue
            zkclient.delete(node_path, recursive=recursive)
        except kazoo.exceptions.NotEmptyError:
            print "Node %s is not empty, delete it with '-r'" % arg
        except kazoo.exceptions.BadArgumentsError:
            print "System node(%s) cannot be deleted" % arg

def exec_add(path, val = "", *args):
    path = get_full_path(path)
    zkclient.create(path, val, makepath=True)

def exec_set(path, val, *args):
    path = get_full_path(path)
    zkclient.set(path, val)

def exec_cat(path):
    full_path = get_full_path(path)
    try:
        val = zkclient.get(full_path)
        print val[0]
    except kazoo.exceptions.NoNodeError:
        print "No such node: ", path

def exec_cd(path):
    if path == "..":
        full_path = os.path.dirname(current_path)
    else:
        full_path = get_full_path(path)
    set_current_path(full_path)

def exec_clear_all(*args):
    choice = raw_input("Are you sure to clear the zookeeper data? Y/n? ")
    choice = choice.strip()
    if choice == "n" or choice == "N" or choice == "No" or choice == "no":
        return
    del_star("/", recursive=True)

cmd_map = {"ls": exec_ls,
            "pwd": exec_pwd,
            "help": exec_help,
            "del": exec_del,
            "add": exec_add,
            "set": exec_set,
            "cat": exec_cat,
            "cd": exec_cd,
            "clear-all": exec_clear_all}

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
    parser.add_argument("-c", "--command", dest="cmd", required=False)
    args = parser.parse_args()
    if args.zkip != None:
        zkip = args.zkip
    if args.port != None:
        zkport = args.port

    endpoint = zkip + ":" + str(zkport)

    zkclient = KazooClient(hosts=endpoint)
    zkclient.start()

    if args.cmd != None:
        exec_command(args.cmd)
    else:
        command_loop(endpoint)
    #result = zkclient.get_children("/")
    #print result

    zkclient.stop()
