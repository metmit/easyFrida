// 检查是否root
Java.perform(function () {
    send("Start hooking <root>...")

    var com_ss_android_common_applog_RootUtils = Java.use('com.ss.android.common.applog.RootUtils')
    com_ss_android_common_applog_RootUtils.isDeviceRooted.implementation = function () {
        console.log('com_ss_android_common_applog_RootUtils.isDeviceRooted():')
        var res = this.isDeviceRooted()
        console.log(res)
        return res
    }
    var com_umeng_commonsdk_internal_utils_h = Java.use('com.umeng.commonsdk.internal.utils.h')
    com_umeng_commonsdk_internal_utils_h.a.implementation = function () {
        console.log('com_umeng_commonsdk_internal_utils_h.a(): ') // 被调用了
        var res = this.a()
        console.log(res)
        return res
    }

    var com_ss_android_ugc_aweme_utils_bq = Java.use('com.ss.android.ugc.aweme.utils.bq')
    com_ss_android_ugc_aweme_utils_bq.f.overload().implementation = function () {
        console.log('com_ss_android_ugc_aweme_utils_bq.f(): ')
        var res = this.f()
        console.log(res)
        return res
    }

    var com_alipay_sdk_g_b = Java.use('com.alipay.sdk.g.b')
    com_alipay_sdk_g_b.c.implementation = function () {
        console.log('com_alipay_sdk_g_b.c(): ')
        var res = this.c()
        console.log(res)
        return res
    }

    var com_bytedance_crash_nativecrash_c = Java.use('com.bytedance.crash.nativecrash.c')
    com_bytedance_crash_nativecrash_c.g.implementation = function () {
        console.log('com_bytedance_crash_nativecrash_c.g(): ')
        var res = this.g()
        console.log(res)
        return res
    }
})
