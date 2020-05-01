#!/usr/bin/evn ptyhon
# -*- coding: utf-8 -*-

import time
import paramiko

class Obj_SSHClient(object):
    def __init__(self, ip, port, user, password):
        self.ip = ip
        self.port = port
        self.user = user
        self.password = password

        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(self.ip, self.port, self.user, self.password, timeout=5)
        self.chan = self.ssh.invoke_shell()

    def invoke_shell(self, cmd, end_str):
        result = ''
        self.chan.send(cmd)
        time.sleep(0.1)
        result = self.chan.recv(10240)
        num = 0
        while result.find(end_str) == -1 and num < 50:
            time.sleep(0.1)
            num+=1
            if self.chan.recv_ready():
                result = ''.join([result, self.chan.recv(10240)])
        return result


    def close(self):
        self.chan.close()
        self.ssh.close()

