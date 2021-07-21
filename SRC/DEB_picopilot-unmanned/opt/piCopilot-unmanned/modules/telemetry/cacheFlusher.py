#!/usr/bin/python3
"""
Keep the zmq cache empty
"""

import sys
import zmq

context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.bind('tcp://127.0.0.1:{0}'.format(sys.argv[1]))

while True:
    socket.recv_pyobj()
