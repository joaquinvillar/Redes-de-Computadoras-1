#!/usr/bin/python

#parm: 1:Host 2:CantBytes 3:FlagNombres 4::HostIntermedio 

import socket
import struct
import sys

# We want unbuffered stdout so we can provide live feedback for
# each TTL. You could also use the "-u" flag to Python.
class flushfile(file):
    def __init__(self, f):
        self.f = f
    def write(self, x):
        self.f.write(x)
        self.f.flush()

sys.stdout = flushfile(sys.stdout)

def main(dest_name):
    dest_addr = socket.gethostbyname(dest_name)
    port = 33434
    max_hops = 30
    icmp = socket.getprotobyname('icmp')
    udp = socket.getprotobyname('udp')
    ttl = 1
    host2 = False
    while True:
        recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
        send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, udp)
        send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
        
        # Build the GNU timeval struct (seconds, microseconds)
        timeout = struct.pack("ll", 5, 0)
        
        # Set the receive timeout so we behave more like regular traceroute
        recv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, timeout)
        
        recv_socket.bind(("", port))
        sys.stdout.write(" %d  " % ttl)
        payload = "a" * int(sys.argv[2]) #tamano pasado por parametro en bytes
        send_socket.sendto(payload, (dest_name, port))
        curr_addr = None
        curr_name = None
        finished = False
        tries = 3
        while not finished and tries > 0:
            try:
                _, curr_addr = recv_socket.recvfrom(512)
                finished = True
                curr_addr = curr_addr[0]
                try:
                    curr_name = socket.gethostbyaddr(curr_addr)[0]
                except socket.error:
                    curr_name = curr_addr
            except socket.error as (errno, errmsg):
                tries = tries - 1
                sys.stdout.write("* ")
        
        send_socket.close()
        recv_socket.close()
        
        if not finished:
            pass
        
        if curr_addr is not None:
            curr_host = "%s (%s)" % (curr_name, curr_addr)
            if curr_addr == sys.argv[4] or curr_name == sys.argv[4]:
				host2 = True
        else:
            curr_host = ""

        if sys.argv[3] == "V":   #CASE FLAG = "V" OUTPUT SHOW ONLY IPADRESS
        	sys.stdout.write("%s\n" % (curr_addr))
        else:	
        	sys.stdout.write("%s\n" % (curr_host))
        
        ttl += 1
        if curr_addr == dest_addr or ttl > max_hops:		
			if host2 == True:
				sys.stdout.write("Uno de los hops coincide con la direccion pasada por parametro\n ")
			break

	            

if __name__ == "__main__":
    main(sys.argv[1])

    #if curr_addr == sys.argv[4] or curr_name == sys.argv[4]:
    		#host2 = True