#!/usr/bin/env python
import random
import socket
import time

s = socket.socket()         # Create a socket object
host = socket.getfqdn() # Get local machine name
port = random.randint(8000, 9999)
s.bind((host, port))        # Bind to the port

print 'Starting server on', host, port
print 'The Web server URL for this would be http://%s:%d/' % (host, port)

s.listen(5)                 # Now wait for client connection.

print 'Entering infinite loop; hit CTRL-C to exit'
while True:
    # Establish connection with client.    
    c, (client_host, client_port) = s.accept()
    print 'Got connection from', client_host, client_port
    line_1 = "HTTP/1.0 200 OK\r\n"
    line_2 = "Content-Type:  text/html\r\n\r\n"
    page_content = "<h1>Hello, world</h1> this is hoffm386's web server."
    message = line_1 + line_2 + page_content
    c.send(message)
    c.close()
