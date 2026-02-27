import time
import re
import socket
import struct
from pathlib import Path
import configparser

LOG = Path(r"c:\Pregenserver\logs\latest.log")
PROPS = Path(r"c:\Pregenserver\server.properties")

# Simple RCON client
class Rcon:
    def __init__(self, host, port, password, timeout=5):
        self.host = host
        self.port = int(port)
        self.password = password
        self.sock = None
        self.id = 0
        self.timeout = timeout

    def connect(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(self.timeout)
        s.connect((self.host, self.port))
        self.sock = s
        return self._auth()

    def _send(self, req_id, typ, payload):
        data = payload.encode('utf8') + b'\x00\x00'
        length = 4 + 4 + len(data)
        packet = struct.pack('<iii', length, req_id, typ) + data
        self.sock.sendall(packet)
        # read length
        raw = self._recvall(4)
        if not raw:
            return None
        (l,) = struct.unpack('<i', raw)
        body = self._recvall(l)
        if body is None:
            return None
        req_id, typ = struct.unpack('<ii', body[:8])
        payload = body[8:-2].decode('utf8', errors='ignore')
        return req_id, typ, payload

    def _recvall(self, n):
        data = b''
        while len(data) < n:
            part = self.sock.recv(n - len(data))
            if not part:
                return None
            data += part
        return data

    def _auth(self):
        self.id += 1
        res = self._send(self.id, 3, self.password)
        return res and res[0] == self.id

    def command(self, cmd):
        self.id += 1
        res = self._send(self.id, 2, cmd)
        if res:
            return res[2]
        return None

    def close(self):
        if self.sock:
            self.sock.close()
            self.sock = None

# read server.properties for rcon details
def read_props(path):
    props = {}
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if '=' in line and not line.strip().startswith('#'):
                k,v = line.strip().split('=',1)
                props[k]=v
    return props


def tail_log(path):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        # go to end
        f.seek(0,2)
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.2)
                continue
            yield line


def main():
    props = read_props(PROPS)
    if props.get('enable-rcon','false').lower() != 'true':
        print('RCON not enabled in server.properties')
        return
    pwd = props.get('rcon.password')
    port = int(props.get('rcon.port', '25575'))
    host = '127.0.0.1'

    rcon = Rcon(host, port, pwd)
    try:
        ok = rcon.connect()
    except Exception as e:
        print('RCON connect failed:', e)
        return
    if not ok:
        print('RCON auth failed')
        return
    print('RCON connected')

    current_world = None
    # match the STARTING_WORLD marker (we now tag the player in-game)
    start_re = re.compile(r'STARTING_WORLD:(?P<world>world_\d+)')
    chunky_re = re.compile(r'\[Chunky\] Task finished for (.+?)\.')

    for line in tail_log(LOG):
        # detect start marker and capture world
        m = start_re.search(line)
        if m:
            current_world = m.group('world')
            print('Detected start for', current_world)
            continue
        # check chunky completion
        m2 = chunky_re.search(line)
        if m2 and current_world:
            dim = m2.group(1)
            print('Chunky finished for', dim, ' — current tracked world:', current_world)
            # only trigger if the finished dimension contains the world id
            if current_world in dim:
                mnum = re.search(r'world_(\d+)', current_world)
                if mnum:
                    n = int(mnum.group(1))
                    nextn = n+1
                    # run the next function as the fixed player (always MrPlanckton)
                    cmd = f'execute as MrPlanckton run function pregen:worlds/world_{nextn}'
                    print('Sending RCON command:', cmd)
                    res = rcon.command(cmd)
                    print('RCON result:', res)
            current_world = None

if __name__ == '__main__':
    main()
