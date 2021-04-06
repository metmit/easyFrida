import frida

device = frida.get_usb_device()

# 获取在前台运行的APP
front_app = device.get_frontmost_application()
print(front_app)
