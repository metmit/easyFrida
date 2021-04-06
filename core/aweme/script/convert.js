/**
 * 数据映射转换
 * @type {{}}
 */
var awemeConvert = {}

/**
 * com.ss.android.ugc.aweme.profile.model.User
 * @param data
 * @returns {{}}
 */
awemeConvert.userModel = function (data) {
    var _maps = {
        "uid": "uid",
        "short_id": "shortId",
        "nickname": "nickname",
        "signature": "signature",
        "unique_id": "uniqueId",
        "sec_uid": "secUid",
        "birthday": "birthday",
        "gender": "gender",
        "create_time": "createTime",
        "province": "province",
        "city": "cityName",
        "follower_count": "followerCount",
        "following_count": "followingCount",
        "aweme_count": "awemeCount",
        "total_favorited": "totalFavorited",
        "avatar_larger": "avatarLarger",
        "avatar_thumb": "avatarThumb",
        "verify_info": "verifyInfo",
        "share_info": "shareInfo",
        "verification_type": "verificationType",
        "enterprise_verify_reason": "enterpriseVerifyReason",
        "custom_verify": "customVerify",
        "with_fusion_shop_entry": "withFusionShopEntry",
        "followers_detail": "followerDetailList",
        "is_star": "isStar"
    }

    var _result = helper.convert.handler(data, _maps, function (_jKey, _value) {
        if (_jKey === "avatarLarger" || _jKey === "avatarThumb") {
            return awemeConvert.urlModel(_value)
        }
        if (_jKey === "shareInfo") {
            return awemeConvert.shareInfoModel(_value)
        }
        if (_jKey === "followerDetailList") {
            return [] // TODO
        }
        return _value
    })

    if (_result["avatar_larger"] && !_result["avatar_thumb"]) {
        _result["avatar_thumb"] = _result["avatar_larger"]
    }
    return _result
}

/**
 * class com.ss.android.ugc.aweme.base.share.ShareInfo
 * @param data
 * @returns {{}}
 */
awemeConvert.shareInfoModel = function (data) {
    var _maps = {
        "share_url": "shareUrl",
        "share_weibo_desc": "shareWeiboDesc",
        "share_desc": "shareDesc",
        "share_title": "shareTitle",
        "share_link_desc": "shareLinkDesc"
    }
    return helper.convert.handler(data, _maps, function (_jKey, _value) {
        return _value
    })
}

/**
 * com.ss.android.ugc.aweme.base.model.UrlModel
 * @param data
 * @returns {{}}
 */
awemeConvert.urlModel = function (data) {
    var _maps = {
        // "file_hash": "fileHash",
        // "width": "width",
        // "height": "height",
        // "data_size": "size",
        // "uri": "uri",
        // "url_key": "urlKey",
        "url_list": "urlList"
    }
    return helper.convert.handler(data, _maps, function (_jKey, _value) {
        return _value
    })
}
