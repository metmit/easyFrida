import frida

# 获取设备
device = frida.get_usb_device()

# 启动调试进程
pid = device.spawn('com.ss.android.ugc.aweme')
print(pid)

process = device.attach(pid)
# process = device.attach('com.ss.android.ugc.aweme')

device.resume(pid)
