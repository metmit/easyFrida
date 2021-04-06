/**
 * 在tt中注册了个回调
 * 在 com.bytedance.frameworks.baselib.network.http.e中调用了此回调
 * 回调中最终也是走到了 leviathan，为了保证可控性，实际可以直接拼参数调 leviathan
 * @param url
 * @param headMapJson
 * @returns {string}
 */
rpcClass.gorgontt= function (url, headMapJson) {
    var result = '';
    Java.perform(function () {
        var ss = Java.use('com.ss.sys.ces.gg.tt$1');
        var HashMap = Java.use("java.util.HashMap").$new();
        var headMap = JSON.parse(headMapJson)
        var ArrayList = Java.use("java.util.ArrayList");
        var JavaObject = Java.use("java.lang.Object");

        for (var key in headMap) {
            var m1 = ArrayList.$new();
            m1.add(headMap[key]);
            var mm1 = Java.cast(Java.cast(m1, ArrayList), JavaObject);
            HashMap.put(key, mm1)
        }

        var jsonObj = Java.use('org.json.JSONObject');
        var str = Java.use("java.lang.String");

        result = str.valueOf(jsonObj.$new(ss.$new().a(url, HashMap)));
    });
    return result;
}

/**
 * 调用native方法，获取签名
 * com.ss.a.b.a.a(com.ss.sys.ces.a.leviathan(v14, currenTime, com.ss.a.b.a.a(md5_params + x_ss_stub + md5_cookie + md5_sessionid)));
 * public static native byte[] leviathan(int i, int i2, byte[] bArr);
 * @returns {*}
 * @param i2 时间戳(秒)
 * @param bStr
 *  - v14：-1
 *  - currenTime：时间戳(秒)
 *  - md5_params： 对url参数进行MD5
 *  - x_ss_stub：只有post时才有效，否则是32个0，判断如果有X-SS-STUB这个值的话就获取，反之则填充32个0，POST数据的一个MD5签名值
 *  - md5_cookie：对cookie进行md5
 *  - md5_sessionid：对cookie里面对sessionid进行md5，否则也是32个0
 */
rpcClass.gorgonleviathan = function (i2, bStr) { // 注意 i2 的类型，传过来太大可能会隐式转换
    var result;
    Java.perform(function () {
        var com_ss_a_b_a = Java.use('com.ss.a.b.a');
        var com_ss_sys_ces_a = Java.use('com.ss.sys.ces.a');
        var bArr = com_ss_a_b_a.a(bStr) // 压缩为byte
        //.overload('int', 'int', '[B')
        var sArr = com_ss_sys_ces_a.leviathan(-1, i2, bArr) // 请求结果
        result = com_ss_a_b_a.a(sArr) // 转byte为string
    });
    return result;
}
