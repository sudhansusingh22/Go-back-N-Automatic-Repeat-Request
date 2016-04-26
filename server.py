import socket
import os
import random
import sys
import helper
from helper import *

def create_soc(server_hostname, server_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((server_hostname, server_port))
    return sock

def init_variables():
    server_hostname = socket.getfqdn()
    
#     server_ip = socket.gethostbyname(server_hostname)
    server_ip = helper.get_ip_address('wlp1s0')
#     server_ip = '192.168.0.23'
#     print socket.getfqdn()
    print server_ip
    server_port = int(sys.argv[1])
    file_name = str(sys.argv[2])
    prob = float(sys.argv[3])
    prob_int = float(prob * 100)
    return server_ip, server_port, file_name, prob, prob_int

def write_data(message):
    fd = open(file_name, "a");
    data = helper.decode_message_received(message)
    fd.write(data)
    fd.close()


def main():
    if len(sys.argv)!=4:
        print "usage : python server.py 7735 \"test_file.txt \" 0.02"
        exit(0)
    print 'server started!!'  

    
if __name__ == '__main__':
    main()
    
def check_file_path(file_name):
    if(os.path.isfile(file_name)):
        os.remove(file_name)

server_hostname, server_port, file_name, prob, prob_int = init_variables()
check_file_path(file_name)
sock = create_soc(server_hostname, server_port)
data,address = sock.recvfrom(32768)
global seq_num
seq_num = 0

while True:
    data, address = sock.recvfrom(32768);
    if(data == "File_sent"):
        break;
#     print 
    if((int(data[0:32],2)) == seq_num):
        randum =  random.randint(0,99); 
        if(randum>=prob_int):
            if(helper.check_checksum_server(data)):
                recv_seq_num = int(data[0:32],2);
                if(recv_seq_num == seq_num):
                    seq_num += 1
                    new_data = data[64:]
                    write_data(new_data)
                    send_seq_num = '{0:032b}'.format(seq_num)
                    msg_to_be_sent = send_seq_num + '0'*16 + '10'*8
                    sock.sendto(msg_to_be_sent, address)          
            else:
                seq = int(data[0:32],2)
                print "Checksum failed, sequence number = %d" % seq
        else:
            seq = int(data[0:32],2)
            print "Packet loss, sequence number = %d" % seq
    else:
        if((int(data[0:32],2)) < seq_num):
            seq = int(data[0:32],2)
            print "Received duplicate packet with sequence number = %d" % seq
        else:
            seq = int(data[0:32],2)
            #print "Received future packet with sequence number = %d" % seq
print "File received successfully as: "+file_name +" ."

