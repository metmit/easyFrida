import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

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
        if task['action'] == 'video_list':
            return Posts(self.rpc, task)

        if task['action'] in ['channel_detail', 'channel_info', 'user_info']:
            return Profile(self.rpc, task)

        if task['action'] in ['topic_detail', 'topic_video_list']:
            return Challenge(self.rpc, task)

        return None

if __name__ == '__main__':
    test_debug = False

    if test_debug:
        test_task = {
            # "action": "video_list",
            "action": "user_info",
            "data": {
                # "timeout": 166666666,
                "uid": "84048748125",  # MS4wLjABAAAAhGsRpLXPKjiIXvGC9gutc796og0R0VUCAtgnyDgIxHk
                "count": 50,
            }
        }
        Task().debug(test_task)
    else:
        Task("74b00222", True).run()
