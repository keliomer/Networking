#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  RFC_downloader.py
#  
#  Copyright 2016 Keliomer Castillo <keliomer@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import sys, socket

try:
    rfc_number = int(sys.argv[1])
except (IndexError, ValueError):
    print('Must supply an RFC number as the first argument!')
    sys.exit(2)

host = 'www.ietf.org'
port = 80
sock = socket.create_connection((host,port))

req = (
    'GET /rfc/rfc{rfcnum}.txt HTTP/1.1\r\n'
    'Host:{host}:{port}\r\n'
    'User-Agent: Python {version}\r\n'
    '\r\n'
    )
    
req = req.format(
    rfcnum=rfc_number,
    host=host,
    port=port,
    version=sys.version_info[0]
    )
sock.sendall(req.encode('ascii'))
rfc_raw = bytearray()
while True:
    buf = sock.recv(4096)
    if not len(buf):
        break
    rfc_raw += buf
rfc = rfc_raw.decode('utf-8')
print(rfc)
