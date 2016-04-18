#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  untitled.py
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

import sys
import csv
import requests
import requests_aws4auth
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import mimetypes

with open('./credentials.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        access_id = row['Access Key Id']
        access_key = row['Secret Access Key']
region = 'us-east-1'
if region and region != 'us-east-1':
    endpoint = 's3-{}.amazonaws.com'.format(region)
else:
    endpoint = 's3.amazonaws.com'
auth = requests_aws4auth.AWS4Auth(access_id, access_key, region, 's3')
ns = 'http://s3.amazonaws.com/doc/2006-03-01/'

def xml_pprint(xml_string):
    print(minidom.parseString(xml_string).toprettyxml())
    
def create_bucket(bucket):
    XML = ET.Element('CreateBucketConfiguration')
    XML.attrib['xmlns'] = ns
    location = ET.SubElement(XML, 'LocationConstraint')
    location.text = auth.region
    
    data = ET.tostring(XML, encoding='utf-8')
    url = 'http://{}.{}'.format(bucket, endpoint)
    if region == 'us-east-1':
        r = requests.put(url, auth=auth)
    else:
        r = requests.put(url, data=data, auth=auth)
    if r.ok:
        print('Created bucket {} OK'.format(bucket))
    else:
        xml_pprint(r.text)
        
def upload_file(bucket,s3_name,local_path, acl='private'):
    data = open(local_path, 'rb').read()
    url = 'http://{}.{}/{}'.format(bucket, endpoint, s3_name)
    headers = {'x-amz-acl': acl}
    mimetype = mimetypes.guess_type(local_path)[0]
    if mimetype:
            headers['Content-Type'] = mimetype
    r = requests.put(url,data=data, headers=headers, auth=auth)
    if r.ok:
        print('Uploaded {} OK'.format(local_path))
    else:
            xml_pprint(r.text)
            
def download_file(bucket, s3_name, local_path):
    url = 'http://{}.{}/{}'.format(bucket,endpoint,s3_name)
    r = requests.get(url, auth=auth)
    if r.ok:
        open(local_path,'wb').write(r.content)
        print('Downloaded {} OK'.format(s3_name))
    else:
        xml_pprint(r.text)
        
        
if __name__ == '__main__':
    cmd, *args = sys.argv[1:]
    globals()[cmd](*args)
