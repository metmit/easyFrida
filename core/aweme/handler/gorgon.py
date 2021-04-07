

import hashlib
import json
import time

from core.aweme.handler.base import BaseTask

# 调用native方法，获取签名
# com.ss.a.b.a.a(com.ss.sys.ces.a.leviathan(v14, currenTime, com.ss.a.b.a.a(md5_params + x_ss_stub + md5_cookie + md5_sessionid)));
# public static native byte[] leviathan(int i, int i2, byte[] bArr);
# @returns {*}
# @param i2 时间戳(秒)
# @param bStr  com.ss.a.b.a.a(md5_params + x_ss_stub + md5_cookie + md5_sessionid)
#  - v14：-1
#  - currenTime：时间戳(秒)
#  - md5_params： 对url参数进行MD5
#  - x_ss_stub：只有post时才有效，否则是32个0，判断如果有X-SS-STUB这个值的话就获取，反之则填充32个0，POST数据的一个MD5签名值
#  - md5_cookie：对cookie进行md5
#  - md5_sessionid：对cookie里面对sessionid进行md5，否则也是32个0

class Gorgon(BaseTask):

    def run(self):
        # url, headerMap, signType='leviathan'
        self.ticks = int(self.data["time"]) if "time" in self.data else int(time.time() * 1000)

        url = self.data['url'] if 'url' in self.data else ""
        headerMap = self.data['header'] if 'header' in self.data else {}

        sign_type = self.data['sign_type'] if 'sign_type' in self.data else "tt"

        if not url:
            print("Params Error!")
            return False

        if sign_type == 'leviathan':
            result = self.__leviathan(url, headerMap)
        else:
            result = self.__tt(url, headerMap)
        return result

    def __tt(self, url, headerMap):
        return self.rpc.gorgontt(url, json.dumps(headerMap))

    def __leviathan(self, url, headerMap):
        # URL 参数的MD5
        md5_params = self.getMd5UrlParams(url)
        # 如果header中有 X-SS-STUB 就是用，否则为32个0
        # 只有post时才有，是POST数据的一个MD5签名值
        x_ss_stub = '00000000000000000000000000000000'
        # 如果header中有cookie，且不为空，md5(cookie_str)
        md5_cookie = '00000000000000000000000000000000'
        # 如果cookie中存在sessionid
        md5_sessionid = '00000000000000000000000000000000'

        for headKey in headerMap:
            tempKey = headKey.upper()
            if tempKey == 'X-SS-STUB':
                if headerMap[headKey] is not None and len(headerMap[headKey]) > 0:
                    x_ss_stub = headerMap[headKey]

            if tempKey == 'COOKIE':
                if headerMap[headKey] is not None and len(headerMap[headKey]) > 0:
                    md5_cookie = self.md5(headerMap[headKey])
                    cookieDict = self.cookieStrToDict(headerMap[headKey])
                    if 'sessionid' in cookieDict and cookieDict['sessionid'] is not None and len(
                            cookieDict['sessionid']) > 0:
                        md5_sessionid = self.md5(cookieDict['sessionid'])

        khronos = str(self.ticks)[:10]

        # gorgon = None
        # print("params: {} stub: {} cookie: {} session: {}".format(md5_params, x_ss_stub, md5_cookie, md5_sessionid))
        #  com.ss.a.b.a.a(md5_params + x_ss_stub + md5_cookie + md5_sessionid)
        gorgon = self.rpc.gorgonleviathan(int(khronos),
                                          md5_params.lower() + x_ss_stub.lower()
                                          + md5_cookie.lower() + md5_sessionid.lower())

        return {
            'X-Khronos': int(khronos),
            'X-Gorgon': gorgon
        }

    def getMd5UrlParams(self, url):
        urlParams = self.getUrlParams(url)
        # urlParams = urlParams.replace('%3A', ':')
        # urlParams = urlParams.replace('+', ' ')
        if urlParams is None or len(urlParams) <= 0:
            return "00000000000000000000000000000000"

        md5Params = self.md5(urlParams)
        if md5Params is None or len(md5Params) <= 0:
            return "00000000000000000000000000000000"
        return md5Params

    # com.ss.sys.ces.gg.tt.c(String str)
    def getUrlParams(self, url):
        indexOf = url.find("?")
        indexOf2 = url.find("#")

        if indexOf == -1:
            return None

        if indexOf2 == -1:
            return url[indexOf + 1:]

        if indexOf > indexOf2:
            return None
        return url[indexOf + 1:indexOf2]

    # com.ss.a.b.b.a
    def md5(self, data):
        m = hashlib.md5(data.encode())
        return m.hexdigest()

    # com.ss.sys.ces.gg.tt.d(String str)
    def cookieStrToDict(self, cookieStr):
        if cookieStr is None or len(cookieStr) <= 0:
            return None

        cookie = {}
        for charSequence in cookieStr.split(';'):
            if charSequence is None or len(charSequence) <= 0:
                continue
            split = charSequence.split('=')
            # if len(split) >= 2 and split[0].strip() == 'sessionid':
            #     return split[1]
            cookie[split[0].strip().lower()] = split[1].strip()
        return cookie
