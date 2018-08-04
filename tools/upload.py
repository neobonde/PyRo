#This file is based on webrepl_cli.py


import struct, sys, os, socket, time

from PyRo_websocket import websocket, WEBREPL_REQ_S, WEBREPL_PUT_FILE, WEBREPL_GET_FILE, WEBREPL_GET_VER

import websocket_helper


DEBUG = 0
SANDBOX= ""

def debugmsg(msg):
    if DEBUG:
        print(msg)

def read_resp(ws):
    data = ws.read(4)
    sig, code = struct.unpack("<2sH", data)
    assert sig == b"WB"
    return code

def send_req(ws, op, sz=0, fname=b""):
    rec = struct.pack(WEBREPL_REQ_S, b"WA", op, 0, 0, sz, len(fname), fname)
    debugmsg("%r %d" % (rec, len(rec)))
    ws.write(rec)

def put_file(ws, local_file, remote_file):
    sz = os.stat(local_file)[6]
    dest_fname = (SANDBOX + remote_file).encode("utf-8")
    rec = struct.pack(WEBREPL_REQ_S, b"WA", WEBREPL_PUT_FILE, 0, 0, sz, len(dest_fname), dest_fname)
    debugmsg("%r %d" % (rec, len(rec)))
    ws.write(rec[:10])
    ws.write(rec[10:])
    assert read_resp(ws) == 0
    cnt = 0
    with open(local_file, "rb") as f:
        while True:
            sys.stdout.write("Sent %d of %d bytes\r" % (cnt, sz))
            sys.stdout.flush()
            buf = f.read(1024)
            if not buf:
                break
            ws.write(buf)
            cnt += len(buf)
    print()
    assert read_resp(ws) == 0

def get_ver(ws):
    send_req(ws, WEBREPL_GET_VER)
    d = ws.read(3)
    d = struct.unpack("<BBB", d)
    return d

def login(ws, passwd):
    while True:
        c = ws.read(1, text_ok=True)
        if c == b":":
            assert ws.read(1, text_ok=True) == b" "
            break
    ws.write(passwd.encode("utf-8") + b"\r")


def send_cmd(ws, cmd):
    print("Doint REPL command: " + cmd)
    bcmd = str.encode(cmd+'\r')
    ws.write(bcmd, text=True)
    time.sleep(1) # Just to slow down comm

TARGET_IP = "192.168.87.109"
TARGET_PORT = "8266"
TARGET_PASS = "1234"

def main():

    print("Uploading src")
    s = socket.socket()

    ai = socket.getaddrinfo(TARGET_IP, TARGET_PORT)
    addr = ai[0][4]

    print (addr)
    s.connect(addr)
    #s = s.makefile("rwb")
    websocket_helper.client_handshake(s)

    ws = websocket(s)

    login(ws, TARGET_PASS)
    print("Remote WebREPL version:", get_ver(ws))

    # Now commands can be sent and files can be uploaded

    send_cmd(ws,"\x03") # Break currently running program if any
    
    send_cmd(ws,"import os")
    send_cmd(ws,"import machine")

    thisFileDir = os.path.dirname(os.path.abspath(__file__))
    srcDir = os.path.join(thisFileDir,'..', 'src')

    rootDir = os.listdir(srcDir)

    # Go through source and look for folders
    # For each folder in src
        # Send create folder command
        # Send go to folder command
        # Put all files from folder in target folder
        # Return to previous folder
    # For the rest of the files just upload in root

    for item in rootDir:
        fullPath = os.path.join(srcDir,item)
        print(fullPath)
        if os.path.isdir(fullPath):
            cmd = "os.mkdir('%s')"%item
            send_cmd(ws,cmd)

            cmd = "os.chdir('%s')"%item
            send_cmd(ws,cmd)
            
            subDir = os.listdir(fullPath)
            
            for subItem in subDir:
                subFullPath = os.path.join(fullPath,subItem)
                print(subFullPath)
                put_file(ws, subFullPath, subItem)
            
            cmd = "os.chdir('..')"
            send_cmd(ws,cmd)
            

        else:
            put_file(ws, fullPath, item)


    cmd = "machine.reset()"
    send_cmd(ws,cmd)

    # Nothing can be done after this
    s.close()

main()