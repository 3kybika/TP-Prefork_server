# coding=utf-8
import os

HOST = '127.0.0.1'
PORT = 80

CPU_COUNT = os.cpu_count() + 1

BUFFER_SIZE = 1024
LISTENERS = 1000

ROOT_DIR = "/var/www/html"

config_path = '/etc/httpd.conf'
