import json
import os
import time


def get_root_path():

    if 'FRIDA_ROOT_PATH' not in os.environ or len(os.environ["FRIDA_ROOT_PATH"]) <= 0:
        os.environ["FRIDA_ROOT_PATH"] = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    return os.environ["FRIDA_ROOT_PATH"]


def on_frida_message(message, data):
    """
    接收打印frida脚本输出的消息
    :param message:
    :param data:
    :return:
    """
    _type = message['type'] if 'type' in message else "send"
    _payload = message['payload'] if "payload" in message else "No-Payload"

    if _type == 'send':
        try:
            if isinstance(_payload, str) or isinstance(_payload, bytes) or isinstance(_payload, bytearray):
                data = json.loads(_payload)
            else:
                data = _payload
        except Exception as e:
            data = _payload
            # print("[Send] {} && {}".format(e, message))
        # print(message)
        print("[Info] {}".format(data))

        # if "type" in data:
        #     save_message(data)
    elif _type == 'error':
        print("[Error] {0}".format(message['description']))
    else:
        print(message)


def save_message(data):
    print(data)


def get_second_time():
    return int(time.time())


def get_milli_time():
    return int(time.time() * 1000)


def get_date_time():
    return time.strftime("%Y-%m-%d %H:%M:%S")
