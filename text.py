import sys
import time
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306

serial = i2c(port=1, address=0x3C)
device = ssd1306(serial)

drawOut = sys.argv[1:]
dSize = len(drawOut)

if (dSize > 7):
  print "Error 7+ args"
  exit(1)

with canvas(device) as draw:
  #draw.rectangle(device.bounding_box, outline="white")
  for z in range(0,dSize):
    draw.text((3, z*9), drawOut[z], fill="white")

time.sleep(5)
