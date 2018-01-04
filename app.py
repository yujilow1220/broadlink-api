import broadlink
import argparse
import os
import bottle
from bottle import request, route, run

def auto_int(x):
    return int(x, 0)

class BroadlinkClient():
    def __init__(self, host, mac):
        self.dev = broadlink.gendevice(0x2712, (host, 80), bytearray.fromhex(mac))
        self.dev.auth()

    def send(self, data_path):
        with open(data_path) as f:
            self.dev.send_data(bytearray.fromhex(f.read()))

cli = BroadlinkClient(os.environ.get('HOST'), os.environ.get('MAC'))


@route('/send/<file_path:path>', method="POST")
def send(file_path):
    if request.get_header(os.environ.get('ACCESS_HEADER')):
        print(file_path)
        print(request.get_header('Host'))
        cli.send(file_path)
        return {'host': request.get_header('Host')}
    else:
        return bottle.HTTPResponse(status=300, body="permission denied")

run(host='0.0.0.0', port=8080, debug=True)
