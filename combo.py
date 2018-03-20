# file: rfcomm-server.py
# auth: Albert Huang <albert@csail.mit.edu>
# desc: simple demonstration of a server application that uses RFCOMM sockets
#
# $Id: rfcomm-server.py 518 2007-08-10 07:20:07Z albert $

# For the Screen
import sys
import time
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial)

# For the server
from bluetooth import *

server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

advertise_service( server_sock, "TextServer",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ], 
#                   protocols = [ OBEX_UUID ] 
                    )
                   
print "Waiting for connection on RFCOMM channel %d" % port

def main():
  try:
    client_sock, client_info = server_sock.accept()
    print "Accepted connection from ", client_info
    while True:
      data = client_sock.recv(1024)
      if len(data) == 0: break
      print "received [%s]" % data

      ### For the Screen
      dOut0, dOut1, dOut2, dOut3, dOut4, dOut5, dOut6 = data, "", "", "", "", "", ""
      dSize0 = len(dOut0)
      if (dSize0 > 20):
        dOut1 = dOut0[20:]
        dOut0 = dOut0[0:20]
      dSize1 = len(dOut1)
      if (dSize1 > 20):
        dOut2 = dOut1[20:]
        dOut1 = dOut1[0:20]
      dSize2 = len(dOut2)
      if (dSize2 > 20):
        dOut3 = dOut2[20:]
        dOut2 = dOut2[0:20]
      dSize3 = len(dOut3)
      if (dSize3 > 20):
        dOut4 = dOut3[20:]
        dOut3 = dOut3[0:20]
      dSize4 = len(dOut4)
      if (dSize4 > 20):
        dOut5 = dOut4[20:]
        dOut4 = dOut4[0:20]
      dSize5 = len(dOut5)
      if (dSize5 > 20):
        dOut6 = dOut5[20:]
        dOut5 = dOut5[0:20]

      with canvas(device) as draw:
        #draw.rectangle(device.bounding_box, outline="white")
        #for z in range(0,dSize):
        draw.text((3, 3), dOut0, fill="white")
        draw.text((3, 12), dOut1, fill="white")
        draw.text((3, 21), dOut2, fill="white")
        draw.text((3, 30), dOut3, fill="white")
        draw.text((3, 39), dOut4, fill="white")
        draw.text((3, 48), dOut5, fill="white")
        draw.text((3, 57), dOut6, fill="white")
  ###
  except IOError:
    print "all done"
    print "retrying"
    pass
  except KeyboardInterrupt:
    client_sock.close()
    server_sock.close()
    print "all done"
    print "exiting"
    exit()

while True:
  main()
