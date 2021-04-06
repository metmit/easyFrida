import json
import time

import frida
import requests

import utils

# 加载JS文件
js_code = open('./script.js', 'r', encoding='utf8').read()

#
session = frida.get_usb_device().attach('com.ss.android.ugc.aweme')

#
script = session.create_script(js_code)
script.on('message', utils.on_message)
script.load()

time = str(int(time.time()))

# url = 'https://aweme-lq.snssdk.com/aweme/v1/aweme/post/?max_cursor=0&user_id=1028768810424894&count=20&retry_type=no_retry&iid=184358846342967&device_id=2277828257122173&ac=wifi&channel=wandoujia_aweme1&aid=1128&app_name=aweme&version_code=670&version_name=6.7.0&device_platform=android&ssmix=a&device_type=Pixel&device_brand=google&language=zh&os_api=27&os_version=8.1.0&uuid=351615082104688&openudid=3d57b21540251c2e&manifest_version_code=670&resolution=1080*1794&dpi=420&update_version_code=6702&_rticket=1590890088312&app_type=normal&js_sdk_version=1.16.3.5&ts=1590890117&sec_user_id=MS4wLjABAAAA-7QwzV-uUTfGr3sbh6ZjhKMDNJDtH5AXBrX07t7QCkZdHY3xksemJ472P_IH6-lN'
# url = 'https://aweme.snssdk.com/aweme/v1/aweme/post/?source=0&max_cursor=0&user_id=104255897823&count=20&os_api=27&device_type=Redmi+6A&device_platform=android&ssmix=a&iid=2233800029897246&manifest_version_code=750&dpi=320&uuid=860621348536368&version_code=750&app_name=aweme&version_name=7.5.0&ts=1594987728&openudid=9657cd5f9b3b0f55&device_id=492173610192071&resolution=720*1344&os_version=8.1.0&language=zh&device_brand=xiaomi&app_type=normal&ac=wifi&update_version_code=7502&aid=1128&channel=wandoujia_aweme2&_rticket=1594987728001'
# url = 'https://aweme.snssdk.com/aweme/v1/aweme/post/?source=0&max_cursor=0&user_id=104255897823&count=20&os_api=27&device_type=Redmi+6A&device_platform=android&ssmix=a&iid=474581415759104&manifest_version_code=770&dpi=320&uuid=867530248398752&version_code=770&app_name=aweme&version_name=7.7.0&ts=1594985361&openudid=8da5badf7b3574de&device_id=2444906248278895&resolution=720*1344&os_version=8.1.0&language=zh&device_brand=xiaomi&app_type=normal&ac=wifi&update_version_code=7702&aid=1128&channel=wandoujia_aweme2&_rticket=1594985361295'
# url = 'https://aweme.snssdk.com/aweme/v1/aweme/post/?source=0&max_cursor=0&user_id=104255897823&count=20&os_api=23&device_type=MI%25205s&device_platform=android&ssmix=a&iid=1934732383506000&manifest_version_code=960&dpi=320&uuid=493873187626255&version_code=960&app_name=aweme&version_name=9.6.0&ts=1594991406&openudid=e37be4c3555be003&device_id=69106511310&resolution=800*1280&os_version=6.0.1&language=zh&device_brand=Xiaomi&app_type=normal&ac=wifi&update_version_code=9602&aid=1128&channel=aweGW&_rticket=1594991406296'
# url = 'https://aweme-eagle-lq.snssdk.com/aweme/v1/user/?user_id=58544496104&address_book_access=1&retry_type=no_retry&iid=4256901458042712&device_id=69106511310&ac=wifi&channel=xiaomi&aid=1128&app_name=aweme&version_code=750&version_name=7.5.0&device_platform=android&ssmix=a&device_type=MI+5s&device_brand=Xiaomi&language=zh&os_api=23&os_version=6.0.1&uuid=493873187626255&openudid=e37be4c3555be003&manifest_version_code=750&resolution=800*1280&dpi=320&update_version_code=7502&_rticket=1594996018659&ts=1594996017&app_type=normal&js_sdk_version=1.19.2.0'
url = 'https://aweme-eagle-lq.snssdk.com/aweme/v1/user/?sec_user_id=MS4wLjABAAAAvD7NPZEdQj9jDmgzas8JzC193zWef4mJfYIvVWnVS_M&address_book_access=1&retry_type=no_retry&iid=4256901458042712&device_id=69106511310&ac=wifi&channel=xiaomi&aid=1128&app_name=aweme&version_code=750&version_name=7.5.0&device_platform=android&ssmix=a&device_type=MI+5s&device_brand=Xiaomi&language=zh&os_api=23&os_version=6.0.1&uuid=493873187626255&openudid=e37be4c3555be003&manifest_version_code=750&resolution=800*1280&dpi=320&update_version_code=7502&_rticket=' + time + '032&ts=' + time + '&app_type=normal&js_sdk_version=1.19.2.0'

res = script.exports.callsecretfunctionedy(url)
print(res)

xg = json.loads(res)
headers = {
    'Accept-Encoding': 'gzip',
    'X-SS-REQ-TICKET': '1594991406296',
    'sdk-version': 1,
    'X-Gorgon': xg['X-Gorgon'],
    'X-Khronos': xg['X-Khronos'],
    'Connection': 'Keep-Alive',
    'User-Agent': 'okhttp/3.10.0.1',
}
print(headers)
data = requests.get(url, headers).text
print(data)
