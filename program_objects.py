from threading import *

global lock
lock = Lock()
global timerlock
timerlock = Lock()
global seq_num
global curr_seq_num
seq_num = 0
global rec_seq_number
global window
global mss
global total_packets
global gbntimer
global timeout
timeout = 0
global timerange
timerange = 0.1
global index
index = 0