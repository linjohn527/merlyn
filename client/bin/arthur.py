# _*_ coding:utf-8 _*_
# __auth__: LJ

import os, sys, platform

if platform.system() == 'Windows':
    BASE_DIR = "\\".join(os.path.abspath(os.path.dirname(__file__)).split('\\')[:-1])
elif platform.system() == 'Linux':
    BASE_DIR = "/".join(os.path.abspath(os.path.dirname(__file__)).split('/')[:-1])

print BASE_DIR
sys.path.append(BASE_DIR)

from core import arrow

if __name__ == '__main__':
    client = arrow.Arrow(sys.argv)