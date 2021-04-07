import json
import os
import random
import sys
import time

import frida

from utils import utils


class Aweme(object):
    """
    可以执行任务的能力
    """
    _abilities = [
    ]

    _script_files = []

    def __init__(self, deviceId=None, forceReboot=None):
        self.rpc = None
        self.deviceId = deviceId
        self.forceReboot = forceReboot

    def debug(self, task):
        print("debug...")
        self._bootDevice()

        clz = None if len(task) <= 0 else (None if 'action' not in task else self._dispatch(task))
        if clz is None:
            self._test(task)
        else:
            clz.run()

        sys.stdin.read()

    def run(self):
        print("execute...")
        self._bootDevice()

        self._execute()

        sys.stdin.read()  # 读取脚本输出

    def _bootDevice(self):
        # 加载脚本
        js_code = self._load_js_code(self._script_files)

        # 获取设备
        if self.deviceId is None:
            device = frida.get_usb_device(timeout=10,)
        else:
            device = frida.get_device(timeout=10, id=self.deviceId)

        pid = None
        session = None
        for i in range(5):
            try:
                process = device.get_process('com.ss.android.ugc.aweme')
                session = device.attach(process.pid)
            except Exception as e:
                # unable to find process with name 'com.ss.android.ugc.aweme'
                try:
                    session = device.attach('com.ss.android.ugc.aweme')
                except Exception as e:
                    # unable to find process with name 'com.ss.android.ugc.aweme'
                    time.sleep(random.random())
                    continue
            break

        if not session:
            # 启动调试进程
            pid = device.spawn('com.ss.android.ugc.aweme')
            session = device.attach(pid)
            # raise

        script = session.create_script(js_code)
        script.on('message', utils.on_frida_message)
        script.load()

        time.sleep(2)

        if pid:  # 新启动的APP在加载后要恢复到正常运行
            device.resume(pid)

        time.sleep(2)  # 如果没有sleep，好像会走到Python打印、再走rpc内的

        # frida.core.ScriptExports
        self.rpc = script.exports

    def _execute(self):
        while True:
            time.sleep(1)
            task = self._getTask()
            if 'action' not in task:
                continue

            if task['action'] not in self._abilities:
                print("超出能力范围：{}".format(task))
                self._insertTask(task)
                time.sleep(15)
                continue

            clz = self._dispatch(task)

            if clz is None:
                print("超出能力范围：{}".format(task))
                self._insertTask(task)
                time.sleep(15)
                continue

            print("任务：{}".format(json.dumps(task)))
            data = clz.run()
            # return data

    def _dispatch(self, task: dict):
        return None

    def _test(self, task):
        pass

    @staticmethod
    def _getTask() -> dict:
        return {}

    @staticmethod
    def _putTask(task: dict):
        pass

    @staticmethod
    def _insertTask(task: dict):
        pass

    @staticmethod
    def _load_js_code(filenames):

        root_path = utils.get_root_path()

        common_code = ''

        # 加载帮助文件
        common_code += open(os.path.join(root_path, 'core/common/script', 'helper.js'), 'r', encoding='utf8').read()
        common_code += '\n\n\n'

        script_path = 'core/aweme/script'

        # 加载自定义文件
        for filename in filenames:
            common_code += open(os.path.join(root_path, script_path, filename), 'r', encoding='utf8').read()
            common_code += '\n\n\n'

        # 加载rpc文件
        common_code += open(os.path.join(root_path, 'core/common/script', 'rpc.js'), 'r', encoding='utf8').read()

        return common_code


if __name__ == '__main__':
    test_debut = True

    if test_debut:
        test_task = {
            # "action": "video_list",
            # "data": {
            #     # "timeout": 166666666,
            #     "uid": "84048748125",  # MS4wLjABAAAAhGsRpLXPKjiIXvGC9gutc796og0R0VUCAtgnyDgIxHk
            #     "count": 50,
            # }
        }
        Aweme().debug(test_task)
    else:
        Aweme().run()
