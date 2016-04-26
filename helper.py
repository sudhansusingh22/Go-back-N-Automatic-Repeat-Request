# from client import *
from program_objects import *
import os
import binascii
from __builtin__ import classmethod
import socket
import fcntl
import struct
class helper(object):
    
    @classmethod
    
    def handle_timeout():
        global total_packets
        global timeout
        if(seq_num<=total_packets):
            print "Timeout, sequence number is %d" % seq_num
        timeout = 1
    
    @classmethod
    def check_file_path(file_name):
        if not os.path.isfile(file_name):
            print "File not present in the given path."
            exit
            
    
    @classmethod
    def create_timer(file_name, mss):      
        timer_object = Timer(timerange, helper.handle_timeout)
        fo = open(file_name, "r")
        total_file = fo.read()
        total_packets = len(total_file)/mss
        curr_seq_num = seq_num
        return timer_object,fo,total_file,total_packets,curr_seq_num
    
    @classmethod
    def encode_message_to_send(self, message, encoding = 'utf-8', errors = 'surrogatepass'):
        bits = bin(int(binascii.hexlify(message.encode(encoding, errors)), 16))[2:]
        return bits.zfill(8 * ((len(bits) + 7) // 8))
    
    def convert_int_to_byte(self,i):
        hex_string = '%x' % i
        n = len(hex_string)
        return binascii.unhexlify(hex_string.zfill(n + (n & 1)))

    @classmethod
    def decode_message_received(self, bits, encoding='utf-8', errors='surrogatepass'):
        n = int(bits, 2)
        return helper.convert_int_to_byte(helper(),n).decode(encoding, errors)
    
    """
    calculate check sum 
    """
    @staticmethod
    def calculate_checksum_client(message):
        total = 0
        for i in range(0,len(message),16):
            data = message[i:i+16]
            int_num = int(data,2)
            total = total + int_num;
            if (total >= 65535):
                total -= 65535
        total = 65535 - total
        checksum_bits = '{0:016b}'.format(total)
        msg_header= message[0:32]+checksum_bits+message[48:]
        return msg_header
    
    @staticmethod
    def check_checksum_server(msg):
        total = 0
        for i in range(0,len(msg),16):
            int_num = int(msg[i:i+16],2)
            total = total + int_num;
            if (total >= 65535):
                total -= 65535
        if(total == 0):
            return 1
        else:
            return 0
    
    
    @classmethod
    def formingMessage(self,sequence, msg):
        sequence_bits = '{0:032b}'.format(sequence)
        data = helper.encode_message_to_send(msg)
        message = sequence_bits + "0"*16 + "01"*8 + data
        msg_checksum = helper.calculate_checksum_client(message)
        return msg_checksum
    
    @staticmethod

    def get_ip_address(ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
                                            s.fileno(),
                                            0x8915,  # SIOCGIFADDR
                                            struct.pack('256s', ifname[:15])
                                            )[20:24])
    
    
