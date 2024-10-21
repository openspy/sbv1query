
import socket
import struct
from gsseckey import gsseckey

SERVER_HOST = 'master.openspy.net'
SERVER_PORT = 28900
QUERY_GAMENAME = "ut"
GAMENAME = "ut"
SECRETKEY = "Z5Nfb0"

def get_kv_value(input, lookup_key):
    last_key = None
    s = input.split("\\")[1:]
    for key in s:
        if last_key == None:
            last_key = key
        else:
            if last_key == lookup_key:
                return key
            last_key = None


def send_comp_list_req(tcpSock):
    #send list req
    list_req = "\\list\\cmp\\gamename\\" + QUERY_GAMENAME + "\\final\\"
    tcpSock.sendall(list_req.encode('ascii'))

    while True:
        data = tcpSock.recv(6)
        if data == None or len(data) != 6 or data[0:6] == "\\final".encode('ascii'):
            break
        port = struct.unpack(">H", data[4:6])[0]
        ipaddr = socket.inet_ntoa(data[0:4])
        print("{}:{}".format(ipaddr, port))


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((SERVER_HOST, SERVER_PORT))

data = s.recv(128)
input = data.decode('ascii')
challenge = get_kv_value(input, "secure")
validation = gsseckey(challenge, SECRETKEY)

#send validation response
validation = "\\gamename\\"+GAMENAME+"\\validate\\"+validation+"\\final\\"
s.sendall(validation.encode('ascii'))

send_comp_list_req(s)

s.close()