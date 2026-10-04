import adbutils

# little app to download new pictures from my phone whenever available and save them

adb = adbutils.AdbClient(host="127.0.0.1", port=5037)
for info in adb.list(extended=True):
    print(info.serial, info.state)
    # <serial> <device|offline>
    print(info.transport_id)

# only list state=device
print(adb.device_list())

# Set socket timeout to 10 (default None)
adb = adbutils.AdbClient(host="127.0.0.1", port=5037, socket_timeout=10)
print(adb.device_list())


# to begin with i wanted to do my little app via adb but decided to leave that idee since
# i dont want to turn on root on that device, i want it to work as ordinary app
