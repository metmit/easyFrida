import os

import frida


class BaseTask(object):

    def __init__(self, rpc, task: dict):
        self.rpc = rpc
        self.task = task
        if 'data' in self.task:
            self.data = self.task['data']
        else:
            self.data = {}

    def run(self):
        pass

    def callRpc(self, attr, *args):
        if not isinstance(self.rpc, frida.core.ScriptExports):
            return False

        # def method(*args, **kwargs):
        #     return script._rpc_request('call', js_name, args, **kwargs)
        # return method

        return getattr(self.rpc, attr)(*args)

    def log(self, message):
        # file_id = self.getDeviceId()
        file_id = 'test'
        filename = os.environ["FRIDA_ROOT_PATH"] + '/aweme/runtime/log_' + file_id + '.log'
        file = open(filename, 'a', encoding='utf8')
        print('[' + str(file_id) + '] ' + str(message))
        file.write(message + '\n')
        file.close()
