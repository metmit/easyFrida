/**
 * 反射Java实例，转换为JS可读实例
 * @type {{}}
 */
var awemeReflect = {}

/**
 * com.ss.android.ugc.aweme.profile.model.User
 * @param instance
 * @param fields
 * @returns {{}}
 */
awemeReflect.userModel = function (instance, fields) {
    if (!fields) {
        fields = [
            "uid", "shortId", "nickname", "signature", "uniqueId", "secUid",
            "birthday", "gender", "createTime",
            "province", "cityName", "city",
            "isStar", "avatarLarger",
            "shareInfo",
            "followerDetailList", // followers_detail: apple_id, name, fan_count
            "followerCount", "followingCount", "awemeCount", "totalFavorited",
            "verifyInfo", "verificationType", "customVerify", "enterpriseVerifyReason", "withFusionShopEntry"
        ]
    }
    var result = helper.reflect.getFastFields(instance, fields)
    if (result["avatarLarger"]) {
        var authorAvatar = awemeReflect.urlModel(result["avatarLarger"]["value"])
        result["avatarLarger"]["instance"] = result["avatarLarger"]["value"]
        result["avatarLarger"]["value"] = authorAvatar
        result["avatarThumb"] = result["avatarLarger"]
    }

    if (result["shareInfo"]) {
        var shareInfo = awemeReflect.shareInfoModel(result["shareInfo"]["value"])
        result["shareInfo"]["instance"] = result["shareInfo"]["value"]
        result["shareInfo"]["value"] = shareInfo
    }

    return result
}

/**
 * class com.ss.android.ugc.aweme.base.share.ShareInfo
 * @param instance
 * @param fields
 * @returns {{}}
 */
awemeReflect.shareInfoModel = function (instance, fields) {
    return helper.reflect.getFastFields(instance, [
        "shareUrl", "shareWeiboDesc", "shareDesc", "shareTitle"
    ])
}

/**
 * com.ss.android.ugc.aweme.base.model.UrlModel
 * @param instance
 * @param fields
 * @returns {{}}
 */
awemeReflect.urlModel = function (instance, fields) {
    var result = helper.reflect.getFastFields(instance, [
        // "uri",
        "urlList"
    ])
    if (result["urlList"]) {
        var urlList = Java.cast(result["urlList"]["value"], Java.use('java.util.ArrayList'))
        result["urlList"]["instance"] = result["urlList"]["value"]
        result["urlList"]["value"] = [
            urlList.iterator().next() + ""
        ]
    }

    return result
}
