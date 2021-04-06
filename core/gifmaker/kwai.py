import sys

import frida


def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)


# 加载Js脚本
"""
Java.perform(function() {
    //<instance: com.yxcorp.gifshow.retrofit.service.KwaiApiService, $className: $Proxy12>
    
    var KwaiAppManager = Java.use("com.yxcorp.gifshow.KwaiApp");
    KwaiAppManager.getApiService.overload().implementation = function () {
        console.log("[*]Called - getApiService");
        var temp = this.getApiService();
        console.log("real res: ");
        console.log(temp);
        console.log(JSON.stringify(temp));
        
        var aaa = temp.shareProfile("123", "copylink");
        console.log(aaa)
        return temp;
    };
})
"""

"""
Java.perform(function() {
    var KwaiAppManager = Java.use("com.yxcorp.gifshow.KwaiApp");
    var apiObj = KwaiAppManager.getApiService()
    console.log(apiObj);
    console.log(JSON.stringify(apiObj));

    var cp_text = apiObj.shareProfile("500375186", "copylink");
    console.log(cp_text)

    // var ss = Java.use('com.ss.sys.ces.gg.tt$1');
    //var HashMap = Java.use("java.util.HashMap").$new();
    //var jsonObj = Java.use('org.json.JSONObject');
    //var str = Java.use("java.lang.String");
    //var res = jsonObj.$new(ss.$new().a(url, HashMap));
    //result = str.valueOf(res);
})
"""

"""
public KwaiApp(Application application, int i, boolean z, long j, long j2, Intent intent) {
    super(application, i, z, j, j2, intent);
    sApp = getApplication();
}
"""

jsCode = """
var result;

function sin() {
    Java.perform(function () {
        var KwaiAppManager = Java.use("com.yxcorp.gifshow.KwaiApp");
        var appManager = Java.use("android.app.Application")
        var intentManager = Java.use("android.content.Intent")
        
        var app = appManager.$new()
        var intent = intentManager.$new()
        
        var apiObj = KwaiAppManager.$new(app, 1, true, 12, 12, intent).getApiService();
        console.log(apiObj.class)
        var cp_text = apiObj.shareProfile("500375186", "copylink");
        console.log(cp_text)
    
        result = "123"
        console.log("js："+result)
    })
    return result;
}

rpc.exports = {
    sina: sin,
};
"""

# 获取设备
device = frida.get_usb_device()
print(device)

# 启动调试进程
# pid = device.spawn('com.smile.gifmaker')  # 以挂起方式创建进程
# print("pid is " + str(pid))
# process = device.attach(pid)  # 附加到该进程
process = frida.get_usb_device().attach('com.smile.gifmaker')
script = process.create_script(jsCode)
script.on('message', on_message)
print('[*] Running CTF')
script.load()

res = script.exports.sina()
print(res)

# device.resume(pid)  # 创建完脚本, 恢复进程运行

sys.stdin.read()  # 读取脚本输出
