#!/usr/bin/python
import zbarlight
import os
import sys
import PIL
import requests

API_ENDPOINT = "http://localhost:3000/api/qrReader"

import time

while True:
    print 'Taking picture..'
    try:
        f = 1
        qr_count = len(os.listdir('qr_codes'))
        os.system('sudo fswebcam -d /dev/video' +
                  sys.argv[1]+' -q qr_codes/qr_'+str(qr_count)+'.jpg')
        print 'Picture taken..'
    except:
        f = 0
        print 'Picture couldn\'t be taken..'

    print

    if(f):
        print 'Scanning image..'
        f = open('qr_codes/qr_'+str(qr_count)+'.jpg', 'rb')
        qr = PIL.Image.open(f)
        qr.load()
        codes = zbarlight.scan_codes('qrcode',qr)
        
    if(codes==None):
        os.remove('qr_codes/qr_'+str(qr_count)+'.jpg')
        print 'No QR code found'
        data = {
         "devID": "QR_Scanner",
         "QRMessage": "no QR code found"
        }
    else:
        print 'QR code(s):'
        print codes
        data = {
         "devID": "QR_Scanner",
         "QRMessage": codes
        }
    try:
        r = requests.post(url=API_ENDPOINT, data=data)
        # extracting response text
        pastebin_url = r.text
        print("The pastebin URLis: %s" % pastebin_url)
    except:
        print("An exception occurred")
    print
    time.sleep(5)
