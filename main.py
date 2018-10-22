import argparse
import config
import traceback

from preforkserver import PreforkServer
from handler import ResponseHandler
from configurator import Configurator


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='server')
    parser.add_argument('-r', type=str, help='Root directory with static files')
    parser.add_argument('-c', type=int, help='CPU count')
    parser.add_argument('-H', type=int, help='Server\'s host')
    parser.add_argument('-p', type=str, help='Server\'s port')
    parser.add_argument('-l', type=str, help='Number of socket connections before refusing')
    parser.add_argument('-b', type=str, help='Size of buffer being used for reading data from socket')

    args = vars(parser.parse_args())
    configurator = Configurator(config.config_path, args)

    server = PreforkServer(
        cpu_count = configurator.cpu_count,
        host = configurator.host, 
        port = configurator.port,
        listeners = configurator.listeners,
        buffer_size = configurator.buffer_size,
        handler = ResponseHandler(configurator.root_dir)
    )
    try:
        server.start()
    except Exception as err:
        print('|ERROR|', err)
        traceback.print_exc()
    finally:
        server.stop()

