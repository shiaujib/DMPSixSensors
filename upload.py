from __future__ import print_function
import os

from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://drive.google.com/drive'
store = file.Storage('storage.json')
creds = store.get()

if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json')
    creds = tools.run_flow(flow, store, flags) \
            if flags else tools.run(flow, store)
DRIVE = build('drive', 'v2', http=creds.authorize(Http()))

flag=0
name=None
while not name:
    try:
        name=raw_input("Please enter subject name :")
        if not name:
            raise ValueError('empty String')

    except ValueError as e:
        print(e)
    
FILES = (
    (name+'_sensor1.txt', False),
    (name+'_sensor2.txt', False),
    (name+'_sensor3.txt', False),
    (name+'_sensor4.txt', False),
    (name+'_sensor5.txt', False),
    (name+'_sensor6.txt', False),
    (name+'_sensor7.txt', False),
    (name+'_sensor8.txt', False),
    (name+'_sensor9.txt', False),
    (name+'_sensor10.txt', False),
    (name+'_sensor11.txt', False),
    (name+'_sensor12.txt', False),
    (name+'_sensor13.txt', False),
)

for filename, convert in FILES:
    metadata = {'title': filename}
    res = DRIVE.files().insert(convert=convert, body=metadata,
            media_body=filename, fields='mimeType,exportLinks').execute()
    if res:
        print('Uploaded "%s" (%s)' % (filename, res['mimeType']))

'''if res:
    MIMETYPE = 'application/pdf'
    res, data = DRIVE._http.request(res['exportLinks'][MIMETYPE])
    if data:
        fn = '%s.pdf' % os.path.splitext(filename)[0]
        with open(fn, 'wb') as fh:
            fh.write(data)
        print('Downloaded "%s" (%s)' % (fn, MIMETYPE))
'''
