/**
 * 用户视频列表
 */
Java.perform(function () {

    send("Start hooking <aweme/post>...")

    var com_ss_android_ugc_aweme_profile_api_AwemeApi = Java.use('com.ss.android.ugc.aweme.profile.api.AwemeApi')
    com_ss_android_ugc_aweme_profile_api_AwemeApi.a
        .overload('boolean', 'java.lang.String', 'java.lang.String', 'int', 'long', 'int', 'java.lang.String', 'int', 'int', 'java.lang.Integer')
        .implementation = function (arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10) {
        var res = this.a.apply(this, arguments);
        helper.sendJson({
            "hook": "com_ss_android_ugc_aweme_profile_api_AwemeApi.a(10) ↓",
            "Arg1": arg1,
            "Arg2": arg2,
            "Arg3": arg3,
            "Arg4": arg4,
            "Arg5": arg5,
            "Arg6": arg6,
            "Arg7": arg7,
            "Arg8": arg8,
            "Arg9": arg9,
            "Arg10": arg10,
            "result": res // class com.ss.android.ugc.aweme.feed.model.FeedItemList
        })

        var it = res.items.value.iterator();
        while (it.hasNext()) {
            var aweme = it.next() // com.ss.android.ugc.aweme.feed.model.Aweme
            console.log(aweme)
        }
        return res
    }
})


