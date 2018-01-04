import broadlink
import argparse
from bottle import request, route, run

def auto_int(x):
    return int(x, 0)

class BroadlinkClient():
    def __init__(self, type, host, mac):
        self.dev = broadlink.gendevice(type, (host, 80), bytearray.fromhex(mac))
        self.dev.auth()

    def send(self, data_path):
        with open(data_path) as f:
            self.dev.send_data(bytearray.fromhex(f.read()))



parser = argparse.ArgumentParser()
parser.add_argument("--type", type=auto_int, default=0x2712, help="type of device")
parser.add_argument("--host", help="host address")
parser.add_argument("--mac", help="mac address (hex reverse), as used by python-broadlink library")
args = parser.parse_args()
cli = BroadlinkClient(args.type, args.host, args.mac)


@route('/send/<file_path:path>', method="POST")
def send(file_path):
    request_token = request.forms.get('token')
    print(file_path)
    print(request.get_header('Host'))
    cli.send(file_path)

run(host='0.0.0.0', port=8080, debug=True)
