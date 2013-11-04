__author__ = 'xf3da'

import xmlrpclib
import rpc
import threading
import SimpleXMLRPCServer
import time
import rpc

class StoppableXMLRPCServer(SimpleXMLRPCServer.SimpleXMLRPCServer):
    """Override of TIME_WAIT"""
    allow_reuse_address = True

    def serve_forever(self):
        self.stop = False
        while not self.stop:
            self.handle_request()

    def force_stop(self):
        self.server_close()

class ClientData():
    def __init__(self, client_ip, client_port):
        self.ip = client_ip
        self.port = client_port
        self.available = False

class Server():
    def __init__(self, ip, port, clients):
        self.ip = ip
        self.port = port
        self.clients = clients
        self.authorized = []

    def start_server(self):
        """Start RPC Server on each node """
        server = StoppableXMLRPCServer(("192.168.146.13", self.port), allow_none =True)
        server.register_instance(self)
        server.register_introspection_functions()
        server_wait = threading.Thread(target=server.serve_forever)
        server_wait.start()
        #server.force_stop()
        #print server_wait.is_alive()

    def find_available_clients(self):
        for client in self.clients:
            client.available = rpc.find_available(self.ip, self.port)
            if client.server_available:
                print("Client " + client + "is available")
            else:
                print("Client " + client + "is not available")

    def mark_presence(self, client_ip, client_port):
        print "We are here in the server program"
        for ClientData in self.clients:
            if client_ip == ClientData.ip and client_port == ClientData.port:
                ClientData.available = True

    def authenticate_user(self, client_ip, client_port, username, user_password):
        if username == user_password: # code here should pass arguments to database to authenticate user; if condition here is temporary
            self.authorized.append(ClientData(client_ip, client_port))
            print "Loggin successful for user: " + username
        else:
            print "Username and password don't match our database"
            return False

    def activate(self):
        print "activating server"
        self.start_server()
        print "server activated"
        #self.find_available_clients()


def main():
    server = Server("192.168.146.13", 8003, get_clients())
    server.activate()

def get_clients():
    clients = []
    clients.append(ClientData("192.168.146.13",9000))
    return clients


if __name__ == "__main__":
    main()