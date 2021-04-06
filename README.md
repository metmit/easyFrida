# Easy-Frida

快速上手开发使用frida。

## 安装
**！！！server与client版本必须保持一致！！！**

### 安装组件
```
$ pip3 install frida-tools==8.0.1
$ pip3 install frida==12.10.4
```

###安装 server

打开 [下载页](https://github.com/frida/frida/releases) ，找到对应手机架构、对应Client版本的包。

比如模拟器使用x86架构（frida-server-xx.xx.xx-android-x86.xz）、手机使用arm架构（frida-server-xx.xx.xx-android-arm.xz），注意是否为64位。

```
$ wget https://github.com/frida/frida/releases/download/12.10.4/frida-server-12.10.4-android-arm64.xz
$ tar -xf frida-server-12.10.4-android-arm64.xz
$ adb push ./frida-server-12.10.4-android-arm64 /data/local/tmp/fs
$ adb shell

begonia:/ $ su 
begonia:/ # chmod +x /data/local/tmp/fs
```

### 启动服务
```
begonia:/ # /data/local/tmp/fs
或者
begonia:/ # /data/local/tmp/fs -l 0.0.0.0:13764
```

### 快速启动
```
$ adb shell < ./start.txt
```

## 问题
有时会有SELinux问题：
```
begonia:/ # setenforce 0
setenforce: SELinux is disabled
```

如果server和client版本不一致，保持两段版本一致：
```
$ frida-ps -U
Failed to enumerate processes: unable to communicate with remote frida-server; please ensure that major versions match and that the remote Frida has the feature you are trying to use
```

如果在64位架构上运行了32的服务，替换对应架构版本的服务：
```
frida.NotSupportedError: unable to handle 64-bit processes due to build configuration
```

如果已存在进程占用端口，杀死遗留进程：
```
Unable to start: Error binding to address 127.0.0.1:27042: Address already in use

begonia:/ # ps -A | grep fs
begonia:/ # kill 111
begonia:/ # /data/local/tmp/fs

```

## 文档
- [官网](https://frida.re/docs/home/)
