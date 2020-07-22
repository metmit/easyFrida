import frida

manager = frida.get_device_manager()
# 获取指定设备
# device = manager.get_device("094fdb0a0b0df7f8")
# device = frida.get_device('094fdb0a0b0df7f8')

# 获取远程设备
# device = manager.add_remote_device("30.137.25.128:13355")
# device = frida.get_remote_device()

# 获取USB设备
# device = manager.get_usb_device()
device = frida.get_usb_device()
