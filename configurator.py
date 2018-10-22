import argparse
import config

class Configurator:
    def __init__(self, path, args):
        self.path = path

        self.listeners = int(args['l']) if args['l'] else None
        self.port = int(args['p']) if args['p'] else None
        self.host = args['H']
        self.cpu_count = int(args['c']) if args['c'] else None
        self.root_dir = args['r']
        self.buffer_size = int(args['b']) if args['b'] else None

        self.parse()
        self.printConfigurationInfo()

    @staticmethod
    def extractLine(line):
        return line.split(b' ')[1].strip().decode()

    def parse(self):
        
        listeners = None     
        port = None 
        host = None 
        cpu_count = None
        root_dir = None
        buffer_size = None

        try:
            with open(self.path, 'rb') as f:
                line = f.readline()
                while line:
                    param = line.split(b' ')[0].decode()
                    if param == 'listeners':
                        self.listeners = int(self.extractLine(line))
                    elif param == 'port':
                        self.port = int(self.extractLine(line))
                    elif param == 'host':
                        self.host =  self.extractLine(line)
                    elif param == 'cpu_count':
                        self.cpu_count = int(self.extractLine(line))
                    elif param == 'root_dir':
                        self.root_dir = self.extractLine(line)
                    elif param == 'buffer_size':
                        self.buffer_size = int(self.extractLine(line))                 
                    else:
                        print('|ERROR| can not read param: ' + param)
                    line = f.readline()
        except IOError:
            print('|ERROR| can not read config file: ' + self.path)

        self.listeners =    self.listeners   or listeners   or config.LISTENERS
        self.port =         self.port        or port        or config.PORT
        self.host =         self.host        or host        or config.HOST
        self.cpu_count =    self.cpu_count   or cpu_count   or config.CPU_COUNT
        self.root_dir =     self.root_dir    or root_dir    or config.ROOT_DIR
        self.buffer_size =  self.buffer_size or buffer_size or config.BUFFER_SIZE 
        
    def printConfigurationInfo(self):
        print('----------------------------------------')
        print('|INFO | Current server configuration:')
        print('----------------------------------------')
        print('|INFO | PORT:', self.port)
        print('|INFO | HOST:', self.host)
        print('|INFO | CPUs:', self.cpu_count)
        print('|INFO | root:', self.root_dir)
        print('|INFO | listeners: ', self.listeners)
        print('|INFO | buffer size:', self.buffer_size)
        print('----------------------------------------')
            