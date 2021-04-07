// 帮助类的集合
var helper = {}

// 要导出的 frida-rpc 方法集合
var rpcClass = {}

/**
 * 发送json消息到Python
 * @param JsonObj
 */
helper.sendJson = function (JsonObj) {
    send(helper.JsonToString(JsonObj))
}

/**
 * 发送结果到Python
 * @param action 操作
 * @param result 结果
 */
helper.sendResult = function (action, result) {
    send({
        "type": "hook_result",
        "action": action,
        "data": result,
    })
}

helper.JsonToString = function (Json) {
    var arr = []
    for (var key in Json) {
        arr.push('' + key + ': ' + Json[key])
    }
    return "\n" + arr.join('\n')
}

/**
 * 判断 str 中 是否包含 search
 * @param str {string}
 * @param search {string|array}
 * @returns {boolean|*}
 */
helper.includeString = function (str, search) {
    if (typeof search == 'string') {
        return str.includes(search)
    } else {
        for (var key in search) {
            if (str.includes(search[key])) return true
        }
        return false
    }
}

/**
 * 遍历Map，返回拼接 key + value 的字符串
 * @param maps
 * @returns {string}
 */
helper.mapToString2 = function (maps) {
    if (!maps) return '';
    var result = '\n'
    var keyset = maps.keySet();
    var it = keyset.iterator();
    while (it.hasNext()) {
        var keyStr = it.next().toString();
        var valueStr = maps.get(keyStr).toString();
        result += keyStr + ': ' + valueStr + '\n';
    }
    return result
}

helper.mapToString = function (maps) {
    if (!maps) return '';
    return Java.cast(maps, Java.use('java.util.HashMap')).toString();
}

helper.byteToString = function (bytes) {
    return Java.use('java.lang.String').$new(bytes)
}

helper.listToString = function (lists) {
    if (!lists) return '';
    return Java.cast(lists, Java.use('java.util.List')).toString();
}

helper.arrayToString = function (arr) {
    if (!arr) return '';
    return Java.cast(arr, Java.use('java.util.ArrayList')).toString();
}

helper.collectionsToString = function (arr) {
    return Java.cast(arr, Java.use('java.util.Collections')).toString();
}

/**
 * 打印安卓内的exception（起到断点作用、查找调用链）
 * @returns {*}
 */
helper.exception = function () {
    return Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Exception").$new())
}

/**
 * 遍历ArrayList对象，并通过callback处理数组元素，格式化item后返回Js的数组类型
 * @param instance
 * @param callback
 * @returns {[]}
 */
helper.iterateArray = function (instance, callback) {
    var arrayList = [];
    if (!instance) return arrayList;
    if (!callback) callback = function (item) {
        return item
    }
    var _iterator = Java.cast(instance, Java.use('java.util.ArrayList')).iterator();
    while (_iterator.hasNext()) {
        var _next = _iterator.next()
        arrayList.push(callback(_next))
    }
    return arrayList;
}

helper.convert = {
    /**
     * 遍历model的 _maps，从 _data 中取出对应数据，调用 _callback 对数据进行格式化
     * @param _data
     * @param _maps
     * @param _callback
     * @returns {[]}
     */
    handler: function (_data, _maps, _callback) {
        var _result = {}
        if (!_data) return _result
        if (!_maps) return _data
        if (!_callback) _callback = function (_jKey, _value) {
            return _value
        }
        for (var _key in _maps) {
            var _jKey = _maps[_key]

            if (!_data[_jKey]) continue;

            var _value = _data[_jKey]["value"] ? _data[_jKey]["value"] : null

            _result[_key] = _callback(_jKey, _value)
        }
        return _result
    }
}

/**
 * 反射Java对象
 */
helper.reflect = {

    /**
     * 获取反射对象
     * @param instance 待反射对象
     * @returns {*}
     */
    getInstance: function (instance) {
        return Java.cast(instance.getClass(), Java.use("java.lang.Class"))
    },

    /**
     * 反射获取对象指定属性的信息
     * @param instance 对象
     * @param fieldName 字段
     * @param reflect 反射类
     * @returns {{type: * 类型, value: * 值}}
     */
    getField: function (instance, fieldName, reflect) {
        if (!reflect)
            reflect = this.getInstance(instance)

        var field = reflect.getDeclaredField(fieldName)

        // 值为 true 则指示反射的对象在使用时应该取消 Java 语言访问检查。值为 false 则指示反射的对象应该实施 Java 语言访问检查
        // 由于JDK的安全检查耗时较多.所以通过setAccessible(true)的方式关闭安全检查就可以达到提升反射速度的目的
        field.setAccessible(true);

        return this.parseField(field.getType(), field.get(instance))
    },

    /**
     * 反射获取对象的所有属性信息
     * @param instance
     * @param needFields
     * @returns {{}}
     */
    getFields: function (instance, needFields) {
        var _this = this
        var result = {}
        if (!instance) return result;
        var reflect = _this.getInstance(instance)
        var fields = reflect.getDeclaredFields();
        if (!needFields) needFields = []
        fields.forEach(function (field) {
            // field.setAccessible(true); // 注释后速度反而提升了
            if (needFields.length <= 0 || needFields.indexOf(field.getName() + '') >= 0) {
                result[field.getName() + ''] = _this.parseField(field.getType(), field.get(instance))
            }
        })
        return result
    },

    /**
     * 快速获取反射的对象字段
     * @param instance
     * @param fields
     * @returns {{}}
     */
    getFastFields: function (instance, fields) {
        var _this = this
        var result = {};
        if (!instance) return result;
        if (!fields || fields.length <= 0) {
            return _this.getFields(instance, fields)
        }
        var reflect = _this.getInstance(instance)
        fields.forEach(function (field) {
            result[field] = _this.getField(instance, field, reflect)
        })
        return result;
    },

    /**
     * 格式化反射的字段
     * @param type
     * @param value
     * @returns {{type: string, value: (string|number|boolean)}}
     */
    parseField: function (type, value) {
        var typeString = type + ''
        if (typeString.includes("java.lang.String") || typeString === "long") {
            value = value + ''
        }
        if (typeString === "int") {
            value = Number(value + '')
        }
        if (typeString === "boolean") {
            value = Boolean(value + '' === 'true' || value + '' === '1')
        }
        return {
            "type": typeString,
            "value": value
        }
    },

    /**
     * 获取反射对象的所有方法
     * @param instance
     */
    getMethods: function (instance) {
        try {
            var clazz = Java.use("java.lang.Class");
            var methods = Java.cast(instance.getClass(), clazz).getDeclaredMethods();
            methods.forEach(function (method) {
                var methodName = method.getName();
                var val1Class = instance.getClass();
                var val1ClassName = Java.use(val1Class.getName());
                var overloads = val1ClassName[methodName].overloads;
                overloads.forEach(function (overload) {
                    var proto = "(";
                    overload.argumentTypes.forEach(function (type) {
                        proto += type.className + ", ";
                    });
                    if (proto.length > 1) {
                        proto = proto.substr(0, proto.length - 2);
                    }
                    proto += ")";
                    overload.implementation = function () {
                        var args = [];
                        for (var j = 0; j < arguments.length; j++) {
                            for (var i in arguments[j]) {
                                var value = String(arguments[j][i]);
                                send(val1ClassName + "." + methodName + " and arguments value is: " + value);
                            }
                            args[j] = arguments[j] + "";
                        }
                        //打印方法参数
                        send(val1ClassName + "." + methodName + " and args is: " + args);
                        //调用方法
                        var retval = this[methodName].apply(this, arguments);
                        //打印方法返回值
                        send(methodName + " return value is: " + retval);
                        return retval;//返回方法返回值
                    }
                })
            })
        } catch (e) {
            send("'" + instance + "' hook fail: " + e);
        }
    }
}

