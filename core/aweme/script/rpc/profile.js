/**
 * 请求用户信息
 *   1、j.a 获取url
 *   2、j.b发起网络请求
 * @param uid
 * @param sec_uid
 * @param needData 是否需要反射获取数据
 * @returns {{}}
 */
rpcClass.profile = function (uid, sec_uid, needData) {
    var result = {}
    Java.perform(function () {
        var profileApiJ = Java.use('com.ss.android.ugc.aweme.profile.api.j')
        uid = Java.use("java.lang.String").$new(uid);
        sec_uid = Java.use("java.lang.String").$new(sec_uid);
        var from = 0; // from
        var tab_type = -1; // prefer_profile_tab_type

        // https://aweme.snssdk.com/aweme/v1/user/profile/other/?sec_user_id=MS4wLjABAAAAhGsRpLXPKjiIXvGC9gutc796og0R0VUCAtgnyDgIxHk&address_book_access=1&from=0&publish_video_strategy_type=2&user_avatar_shrink=188_188&user_cover_shrink=750_422
        var url = profileApiJ.a(sec_uid, uid, from, tab_type)

        //<instance: com.ss.android.ugc.aweme.profile.presenter.UserResponse>
        var UserResponse = profileApiJ.b(url, true, null)

        if (!needData) return result

        // <instance: com.ss.android.ugc.aweme.profile.model.User>
        // var UserModel = UserResponse.user.value
        var UserModel = UserResponse["user"]["value"]

        var user = awemeReflect.userModel(UserModel, [])
        result = awemeConvert.userModel(user)
    });

    return result;
}



