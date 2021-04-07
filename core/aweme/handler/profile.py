from core.aweme.handler.base import BaseTask


class Profile(BaseTask):

    def run(self):
        uid = self.data['uid'] if 'uid' in self.data else ""
        sec_uid = self.data['sec_uid'] if 'sec_uid' in self.data else ""
        if not uid and not sec_uid:
            print("Params Error!")
            return False

        needData = True
        response = self.rpc.profile(uid, sec_uid, needData)
        return response
