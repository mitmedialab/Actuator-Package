
#https://wiki.python.org/moin/TcpCommunication
#!/usr/bin/env python

import socket
import time

class NetworkServerWrapper():
    def __init__(self, server_ip='', server_port = '8080'):
        self.ip = server_ip
        self.port = server_port
        # self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.status = 0 # 1 -->init socket , 2--> connect_socket
        self.open_socket()

    def open_socket(self, ip='', port=''):
        if ip != '':
            self.ip = ip
        if port != '':
            self.port = port

        if self.status ==2:
            self.close_socket(msg = 'Reset connection with ip:'+str(self.ip)+", port:"+str(self.port))

        if self.status ==0:
            self.init_socket()

        if self.status ==1:
            try:
                self.s.bind((self.ip,self.port))
                self.status = 2
                print("Opened server on ip:",self.ip,", port:",self.port)
                self.s.listen(1)
            except socket.error as msg:
                self.close_socket(msg = "Can't open to ip:"+str(self.ip)+", port:"+str(self.port))

        return

    def wait_socket(self):

        while self.status <2:
            print("Try to open the socket")
            self.open_socket()

        if self.status ==2:
            self.connection, self.client_address  = self.s.accept()
            self.status = 3

        else:
            print("Client is already connected")
        return

    def close_socket(self, msg=''):
        self.s.close()
        self.s = None

        time.sleep(0.01)

        if msg == '':
            print("Close socket server with ip:", self.ip, ",port:",self.port,  end="\r")
        else:
            print(msg, end='\r')

        self.status = 0
        return

    def init_socket(self):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.status =1
        except socket.error as msg:
            self.close_socket(msg = "Can't initialize socket")
        return


    def send_socket(self, buf):
        if self.status ==3:
            try:
                self.connection.send(buf)
                return 1
            except socket.error as msg:
                self.close_socket(msg = "Can't send. Client is down")
                return -1

        else:
            self.open_socket()
            return -1

        return

    def recv_socket(self, size=128):
        try:
            buf = self.connection.recv(size)

        except socket.error as msg:
            self.close_socket(msg = "Can't Receive. Client is down")
            return []

        if not buf:
            self.close_socket(msg = "Zero byte received from client. Close socket")

        return buf

    def fsm_open_socket(self):
        while self.status <2:
            self.open_socket()

        return

    def fsm_recv_socket(self, size=128):
        if self.status ==3:
            return self.recv_socket(size)

        else:
            return []

    def get_status(self):
        return self.status
