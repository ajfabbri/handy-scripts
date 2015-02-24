#!/usr/bin/python
#
# tcp_break.py: A script to cause TCP connections to fail or disconnect.
# Currently linux-specific.
# Aaron Fabbri, 2015
#

import argparse
import signal
import subprocess
import sys
import time

verbose = False
old_sigint_handler = None
undo_commands = []

def dprint(s) :
    if (verbose) :
        print s

def parse_args() :
    global verbose
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("dest_host", help="Destination hostname.")
    arg_parser.add_argument("-p", "--dest_port", help="Destination TCP port.",
            type=int)
    arg_parser.add_argument("-v", "--verbose", help="Verbose (debug) output.",
        action="store_true", default=False)
    arg_parser.add_argument("-l", "--list",
        help="List active connections matching options", action="store_true")
    arg_parser.add_argument("-r", "--reset",
            help="Reset connection, forcefully, if possible",
            action="store_true")
    arg_parser.add_argument("-d", "--drop", type=int, 
            help="Drop packets for this connection for X milliseconds.")

    opts = arg_parser.parse_args()
    if (opts.verbose) :
        verbose = True
    return opts

def die(msg) :
    print msg
    sys.exit()

def verify_opts(opts) :
    if not (opts.dest_host and 
            (opts.list or opts.reset or opts.drop)) :
        die("Must supply destination host and one of list, reset, drop.")

def exit_cleanup(signo=None, stackframe=None) :
    global undo_commands
    dprint("-> exit_cleanup()")
    while undo_commands :
        try :
            do_cmd(undo_commands.pop())
        except subprocess.CalledProcessError:
            dprint("exit_cleanup(): Non-zero exit status,")

def warn_if_not_root() :
    if do_cmd("whoami") != "root" :
        print "\n*** You may need to run as root for this command to work. ***\n"

def do_cmd(cmd_list) :
    dprint("do_cmd(%s)" % str(cmd_list))
    return subprocess.check_output(cmd_list, stderr=subprocess.STDOUT)

def do_list(opts) :
    port_str = (":%d" % opts.dest_port) if opts.dest_port else "" 
    try :
        print do_cmd(["lsof", "-i", "TCP@%s%s" % (opts.dest_host, port_str)])
    except subprocess.CalledProcessError:
        dprint("No matching sockets found")

def do_reset(opts) :
    warn_if_not_root()
    die("This would be cool to do via forged RST packets.  Don't need\n" +
            "this yet so it is a TODO in the future.")
    # should be able to use python struct and raw socket to do this

def do_drop(opts) :
    global undo_commands

    warn_if_not_root()
    ipt_cmd = ["iptables", "-A", "OUTPUT", "-p", "tcp", "--destination",
            opts.dest_host, "-j", "DROP"]
    if opts.dest_port :
        ipt_cmd.extend(["--dport", str(opts.dest_port)])

    undo_commands.append(["iptables", "-D"] + ipt_cmd[2:])

    if verbose :
        dprint(do_cmd(["iptables", "-L"]))

    try :
        do_cmd(ipt_cmd)
    except subprocess.CalledProcessError :
        print "Command indicated failure: " + " ".join(ipt_cmd)
        return

    # Packets are being blocked.  Sleep then cleanup on exit.
    if verbose :
        dprint(do_cmd(["iptables", "-L"]))
    dprint("Sleeping for %d msec" % opts.drop)
    time.sleep(opts.drop/1000.0)


def main() :
    global old_sigint_handler
    opts = parse_args()

    dprint(str(opts))

    verify_opts(opts)
    old_sigint_handler = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, exit_cleanup)
    try :
        if opts.list :
            do_list(opts)
        elif opts.reset :
            do_reset(opts)
        elif opts.drop :
            do_drop(opts)
    finally :
        exit_cleanup()
        signal.signal(signal.SIGINT, old_sigint_handler)


if __name__ == "__main__":
	main()

# vim: ai ts=4 sts=4 et sw=4 ft=python
