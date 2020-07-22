import frida
import sys


def on_message(message, data):
    print(message)


device = frida.get_usb_device()
weixin = "com.tencent.mm"
# 枚举进程中加载指定模块中的导出函数
session = device.attach(weixin)  # 也可以使用attach(pid)的方式

jscode = """
    Process.enumerateModules({
      onMatch:function(exp){
        send(exp.name);
      },
      onComplete:function(){
        send("stop");
      }
})
"""
script = session.create_script(jscode)
script.on('message', on_message)
script.load()
sys.stdin.read()
