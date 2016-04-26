import os
import sys
import socket
# import thread
from threading import *
# from time import *
from program_objects import *
import helper
from helper import *
import time
import datetime

def init_variables():
    server_hostname = str(sys.argv[1])
#     server_ip = socket.gethostbyname(server_hostname)
    server_port = int(sys.argv[2])
    file_name = str(sys.argv[3])
    window = int(sys.argv[4])
    mss = int(sys.argv[5])
    return server_hostname, server_port, file_name, window, mss


def create_soc(server_hostname, server_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto("This is first message",(server_hostname, server_port))
    return sock

"""
main function
"""
def main():
    if len(sys.argv)!=6:
        print " usage : python client.py 192.168.101.138 7735 \"test_f.txt\"  64 500"
        exit(0)
    print 'server connected!!'  

    
if __name__ == '__main__':
    main()
 

def recv_data():
    global seq_num
    global timer_object
    global index
    while True:
        (data, server) = sock.recvfrom(8240)
        lock.acquire()
        ackstr = "10"*8
        #print "data received"
        if(data[48:64] == ackstr):
            pass
        else:
            print "Discarding packet as this is not ACK."
        rec_seq_number = int(data[0:32],2)
        if(rec_seq_number == (total_packets+1)):
            seq_num = rec_seq_number
            sock.sendto("File_sent", server);
            print "File "+ file_name + " successfully sent."
            lock.release()
            break
        if(rec_seq_number > seq_num):
            diff = rec_seq_number - seq_num
            index = index - diff
            seq_num = rec_seq_number
            timer_object.cancel()
            timer_object = Timer(timerange, handle_timeout)
            timer_object.start()
            lock.release()
        else:
            lock.release()

    
def handle_timeout():
    global total_packets
    global timeout
    if(seq_num<=total_packets):
        print "Timeout, sequence number is %d" % seq_num
    timeout = 1


def create_thread():
    thread_instance = Thread(target=recv_data, args=())
    return thread_instance
    
 
def check_file_path():
    if not os.path.isfile(file_name):
        print "File not present in the given path."
        exit
 
def create_timer():      
    timer_object = Timer(timerange, handle_timeout)
    file_to_read = open(file_name, "r")
    total_file = file_to_read.read()
    total_packets = len(total_file)/mss
    curr_seq_num = seq_num
    return timer_object,file_to_read,total_file,total_packets,curr_seq_num


"""
Calling methods
"""

server_hostname, server_port, file_name, window, mss = init_variables()
check_file_path()
start_time = datetime.datetime.now()
print "Start time: " +  time.strftime('%l:%M:%S%p %Z on %b %d, %Y') 
sock = create_soc(server_hostname, server_port) 
thread_instance = create_thread()    
thread_instance.start()
timer_object,file_to_read,total_file,total_packets,curr_seq_num = create_timer()
timer_object.start()


while(thread_instance.isAlive()):
    while(index<window):
        file_to_read = open(file_name, "r")
        lock.acquire()
        if(curr_seq_num == seq_num):
            curr_seq_num = seq_num
            temp_index = index
            lock.release();
            file_to_read.seek((curr_seq_num+temp_index)*mss, 0)
            msgs = file_to_read.read(mss)
            counter = msgs.count('\n')
            msg = msgs #[0:(mss-counter)]
            file_to_read.close()
            if(len(msg) != 0):
                msg_final = helper.formingMessage((temp_index+curr_seq_num), msg)
                index = index + 1
                sock.sendto(msg_final,(server_hostname, server_port))
            else:
                break
        else:
            curr_seq_num = seq_num
            temp_index = index
            lock.release();
            file_to_read.seek((curr_seq_num+temp_index)*mss, 0)
            msgs = file_to_read.read(mss)
            counter = msgs.count('\n')
            msg = msgs
            file_to_read.close()
            if(len(msg) != 0):
                msg_final = helper.formingMessage((temp_index+curr_seq_num), msg)
                index = index + 1
                sock.sendto(msg_final,(server_hostname, server_port))
            else:
                break
                
    if(timeout == 1):
        index = 0
        timer_object = Timer(timerange, handle_timeout)
        timer_object.start()
        timeout = 0

# run_thread()

sock.close()
stop_time = datetime.datetime.now()
print "End time: " + time.strftime('%l:%M:%S%p %Z on %b %d, %Y')
print "Time to send: " + str((stop_time - start_time).seconds) + " seconds."


