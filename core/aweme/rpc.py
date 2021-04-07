import os
import sys

from core.aweme.handler.gorgon import Gorgon

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from core.aweme.handler.base import BaseTask
from core.aweme.base import Aweme

from core.aweme.handler.profile import Profile


class Task(Aweme):
    # 可以执行任务的能力
    _abilities = [
        "user_info",
        "gorgon",
    ]

    # 要加载的脚本文件
    _script_files = [
        "reflect.js",
        "convert.js",
        "rpc/profile.js",
        "rpc/gorgon.js",
    ]

    def __init__(self, deviceId=None, forceReboot=None):
        super().__init__(deviceId, forceReboot)

    def debug(self, task):
        super().debug(task)

    def run(self):
        super().run()

    def _test(self, task):
        # response = self.rpc.challengeaweme("人性", "", "0", "")
        response = self.rpc.liveroominfo()
        print(response)

    def _dispatch(self, task: dict) -> BaseTask or None:
        if task['action'] in ['user_info']:
            return Profile(self.rpc, task)

        if task['action'] == 'gorgon':
            return Gorgon(self.rpc, task)

        return None


if __name__ == '__main__':

    test_debug = True

    if test_debug:
        test_task = {
            # "action": "user_info",
            # "data": {
            #     "uid": "84048748125",
            #     "sec_uid": "MS4wLjABAAAAhGsRpLXPKjiIXvGC9gutc796og0R0VUCAtgnyDgIxHk"
            # },

            "action": "gorgon",
            "data": {
                "url": "https://www.iesdouyin.com/share/user/104255897823?u_code=1g8ff6aflc0c&sec_uid=MS4wLjABAAAA8U_l6rBzmy7bcy6xOJel4v0RzoR_wfAubGPeJimN__4&timestamp=1592923020&utm_source=copy&utm_campaign=client_share&utm_medium=android&share_app_name=douyin"
            }
        }
        Task().debug(test_task)
    else:
        Task("74b00222", True).run()
