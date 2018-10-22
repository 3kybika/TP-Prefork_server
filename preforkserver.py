import os
import socket
import select
import struct


class PreforkServer:
    def __init__(self, cpu_count, host, port, listeners, buffer_size, handler):
        self.cpu_count = cpu_count
        self.host = host
        self.port = port
        self.listeners = listeners
        self.buffer_size = buffer_size
        self.handler = handler
        self.server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.workers = []

    class Worker:
        def __init__(self, pipe):
            self.pipe = pipe
            self.is_free = True
            self.client = None

    def create_child(self):
        child, parent = socket.socketpair()
        pid = os.fork()
        if pid == 0:
            # This perform in a child process
            print("|INFO | Created worker, PID: {}".format(os.getpid()))
            child.close()
            while True:
                # Read from socket parent-child
                request = parent.recv(self.buffer_size)
                if request:
                    responseBuilder = self.handler.handle(request)
                    PreforkServer.send_msg(parent, responseBuilder.build_response())

        # returning in parent...
        self.workers.append(PreforkServer.Worker(child))
        parent.close()

    def start(self):
        adress = (self.host, self.port)
        self.server.bind(adress)
        self.server.listen(self.listeners)

        for i in range(self.cpu_count):
            self.create_child()
        print('----------------------------------------')
        print("|INFO | Server is ready. Address: {}:{}".format(self.host, self.port))
        print('----------------------------------------')
        # Array of sockets for reading
        for_reading = [self.server] + [worker.pipe.fileno() for worker in self.workers]

        while True:
            readable, writable, exceptions = select.select(for_reading, [], [])
            if self.server in readable:
                for worker in self.workers:
                    # Looking for worker for this task
                    if worker.is_free:                        
                        client, client_addr = self.server.accept()
                        request = client.recv(self.buffer_size)
                        
                        if len(request.strip()) == 0:
                            client.close()
                            break
                        worker.is_free = False
                        worker.pipe.send(request)
                        worker.client = client
                        break

            for worker in self.workers:
                if worker.pipe.fileno() in readable:
                    # Recieved response from child
                    response = PreforkServer.recv_msg(worker.pipe)

                    worker.client.send(response)
                    worker.client.close()
                    worker.is_free = True

    def stop(self):
        self.server.close()

    @staticmethod
    def send_msg(sock, msg):
        msg = struct.pack('>Q', len(msg)) + msg
        sock.sendall(msg)

    @staticmethod
    def recv_msg(sock):
        msg_len = PreforkServer.recv_all(sock, 8)
        if not msg_len:
            return None
        msg_len = struct.unpack('>Q', msg_len)[0]
        return PreforkServer.recv_all(sock, msg_len)

    @staticmethod
    def recv_all(sock, size):
        data = b''
        while len(data) < size:
            packet = sock.recv(size - len(data))
            if not packet:
                return None
            data += packet
        return data

    def __del__(self):
        self.server.close()


