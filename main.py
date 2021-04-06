# -*- coding: UTF-8 -*-
import os

from core.aweme.main import Aweme


class Main(object):
    def __init__(self):
        os.environ["FRIDA_ROOT_PATH"] = os.path.dirname(os.path.abspath(__file__))

    def run(self):
        Aweme().run()


if __name__ == '__main__':
    Main().run()
