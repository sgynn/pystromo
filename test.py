import os
import fcntl
import time
import struct

from lib import events
from lib import constants as consts


fd = os.open("/dev/uinput", os.O_WRONLY | os.O_NONBLOCK);

# register virtual  device
USER_DEVICE_FORMAT = "80sHHHHi" + 'I'*64*4
USER_DEVICE_DATA = [ b"uinput test device", consts.BUS_USB, 1, 1, 4, 0, ]
USER_DEVICE_DATA += [0] * 64*4
os.write(fd, struct.pack(USER_DEVICE_FORMAT, *USER_DEVICE_DATA))


UI_SET_EVBIT = 0x40045564
fcntl.ioctl(fd, UI_SET_EVBIT, consts.EV_KEY);
for code in range(0,256):
    fcntl.ioctl(fd, UI_SET_EVBIT+1, code);


UI_DEV_CREATE  = 0x5501
fcntl.ioctl(fd, UI_DEV_CREATE)



time.sleep(0.1)


E = events.Event
syn     = bytes(E(type=consts.EV_SYN, code=0, value=0));
keydown = bytes(E(type=consts.EV_KEY, code=30, value=1))
keyup   = bytes(E(type=consts.EV_KEY, code=30, value=1))



print("raw:",  ' '.join("{:02x}".format(c) for c in keydown))
print("raw:",  ' '.join("{:02x}".format(c) for c in keyup))
print("raw:",  ' '.join("{:02x}".format(c) for c in syn))

os.write(fd, keydown);
os.write(fd, syn);


os.write(fd, keyup);
os.write(fd, syn);



UI_DEV_DESTROY = 0x5502
fcntl.ioctl(fd, UI_DEV_DESTROY)

