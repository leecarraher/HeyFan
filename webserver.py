#!/usr/bin/env python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import urlparse
import sys
from fan_433 import *




class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_POST(self):
        self._set_headers()
        parsed_path = urlparse.urlparse(self.path)
        cmd = self.path[1:]


        print cmd,control_map[cmd]
        tx1.send(int(control_map[cmd]))
        #tx1.cancel()

        self._set_headers()
        self.wfile.write("<html><body><h1>POST!</h1></body></html>")


def run(server_class=HTTPServer, handler_class=S, port=8000):
    server_address = ('localhost', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()

if __name__ == "__main__":
    '''
        preamble
        +400us
        11000us

        * according to spec it is 1:30 so if full preamble is 11400us
        * the base symbol is 11400/31  = 367.7us

        then signal
        [
        bit is 1400us
        1 = High_1000us + Low_400us
        0 = High_400us  + Low_1000us
        ]
        * according to spec it is 1:3 ratio
        preamble+
            example lights on:
            0011 1101 1101 0000 1001 0101 0
            low
            0011 1101 1101 0000 1001 1000 0
            med
            0011 1101 1101 0000 1001 0010 0
            hi
            0011 1101 1101 0000 1001 0110 0
            stop fan
            0011 1101 1101 0000 1001 1100 0

            1hour delay
            0011 1101 1101 0000 1001 0100 0
            2hour delay
            0011 1101 1101 0000 1001 0001 0
            4hour delay
            0011 1101 1101 0000 1001 0011 0
            8hour delay
            0011 1101 1101 0000 1001 1010 0
    '''
    TX=21

    global control_map
    global tx1
    control_map =   {
            'light':0b001111011101000010010101,
            'low'  :0b001111011101000010011000,
            'med'  :0b001111011101000010010010,
            'hi'   :0b001111011101000010010110,
            'stop' :0b001111011101000010011100,
            '1hour':0b001111011101000010010100,
            '2hour':0b001111011101000010010001,
            '4hour':0b001111011101000010010011,
            '8hour':0b001111011101000010011010,
    }

    # define optional callback for received codes.
    pi = pigpio.pi() # Connect to local Pi.
    tx1 = tx(pi, gpio=TX)

    run()

    pi.stop() # Disconnect from local Pi.

