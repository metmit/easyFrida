import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from core.aweme.base import Aweme


class Hook(Aweme):
    _script_files = [
        "hooks/posts.js"
    ]

    def __init__(self):
        super().__init__()

    def debug(self, task):
        super().debug(task)

    def run(self):
        super().run()


if __name__ == '__main__':
    test_debut = True
    if test_debut:
        Hook().debug({})
    else:
        Hook().run()
