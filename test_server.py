#! /usr/bin/env python
# Taken from github.com/leflerja.

import server

def test_error():
    conn = FakeConnection("GET /dingus HTTP/1.0\r\n\r\n")
    server.handle_connection(conn, server.get_server_environ())
    result = conn.sent

    if 'HTTP/1.0 404 Not Found' not in result:
        assert False
    else:
        pass

def test_index():
    conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")
    server.handle_connection(conn, server.get_server_environ())
    result = conn.sent

    if ('HTTP/1.0 200 OK' and \
        'Content-type: text/html' and \
        'Hello world!') not in result:
        assert False
    else:
        pass

def test_content():
    conn = FakeConnection("GET /content HTTP/1.0\r\n\r\n")
    server.handle_connection(conn, server.get_server_environ())
    result = conn.sent

    if ('HTTP/1.0 200 OK' and \
        'Content-type: text/html' and \
        'Content') not in result:
        assert False
    else:
        pass

def test_files():
    conn = FakeConnection("GET /file HTTP/1.0\r\n\r\n")
    server.handle_connection(conn, server.get_server_environ())
    result = conn.sent

    if ('HTTP/1.0 200 OK' and \
        'Content-type: text/plain') not in result:
        assert False
    else:
        pass

def test_images():
    conn = FakeConnection("GET /image HTTP/1.0\r\n\r\n")
    server.handle_connection(conn, server.get_server_environ())
    result = conn.sent

    if ('HTTP/1.0 200 OK' and \
        'Content-type: image/jpeg') not in result:
        assert False
    else:
        pass

def test_form():
    conn = FakeConnection("GET /form HTTP/1.0\r\n\r\n")
    server.handle_connection(conn, server.get_server_environ())
    result = conn.sent

    if ('HTTP/1.0 200 OK' and \
        'Content-type: text/html' and \
        'Credit Card Number' and \
		'Social Security Number' and \
		'<input type=\'submit\' value=\'Enter\'/>') not in result:
        assert False
    else:
        pass

def test_submit():
    conn = FakeConnection("GET /submit?ccn=999&ssn=000 HTTP/1.0\r\n\r\n")
    server.handle_connection(conn, server.get_server_environ())
    result = conn.sent

    if ('HTTP/1.0 200 OK' and \
        'CCN' and \
		'999' and \
		'000' and \
		'SSN' ) not in result:
        assert False
    else:
        pass

def test_post_app():
	payload = "ccn=999&ssn=000\r\n"
	conn = FakeConnection("POST /submit HTTP/1.0\r\n" + \
						  "Content-Length: " + str(len(payload)) + "\r\n" + \
						  "Content-Type: application/x-www-form-urlencoded\r\n\r\n" + \
						  payload)
	server.handle_connection(conn, server.get_server_environ())
	result = conn.sent

	if ('HTTP/1.0 200 OK' and \
		'CCN' and \
		'SSN') not in result:
		assert False
	else:
		pass

def test_post_multi():

	payload = "--AaB03x\r\n" + \
			  "Content-Disposition: form-data; name=\"ccn\";\r\n\r\n" + \
			  "999\r\n" + \
			  "--AaB03x\r\n" + \
			  "Content-Disposition: form-data; name=\"ssn\";\r\n\r\n" + \
			  "000\r\n" + \
			  "--AaB03x--\r\n"
			  
	conn = FakeConnection("POST /submit HTTP/1.0\r\n" + \
						  "Content-Length: " + (str(len(payload))) + "\r\n"  + \
						  "Content-Type: multipart/form-data; boundary=AaB03x\r\n\r\n" + payload)
	server.handle_connection(conn, server.get_server_environ())
	result = conn.sent

	if 'HTTP/1.0 200 OK' not in result:
		assert False
	else:
		pass

def test_main():

    fakemodule = FakeSocketModule()

    success = False
    try:
		server.main(fakemodule)
    except AcceptCalledMultipleTimes:
        success = True
        pass

    assert success, "Something went wrong"

class AcceptCalledMultipleTimes(Exception):
    pass

class FakeSocketModule(object):
	def getfqdn(self):
		return "fakehost"

	def socket(self):
		return FakeConnection("")

class FakeConnection(object):
	def __init__(self, to_recv):
		self.to_recv = to_recv
		self.sent = ""
		self.is_closed = False
		self.n_times_accept_called = 0

	def bind(self, param):
		(host, port) = param

	def listen(self, n):
		assert n == 5
		if n != 5:
			raise Exception("n should be five you dumby")

	def accept(self):
		print "socket accept"
		self.n_times_accept_called += 1
		if self.n_times_accept_called >= 1:
			raise AcceptCalledMultipleTimes("stop calling accept, please")
		
		
		c = FakeConnection("")
		return c, ("noclient", 32351)

	def recv(self, n):
		if n > len(self.to_recv):
			r = self.to_recv
			self.to_recv = ""
			return r
			
		r, self.to_recv = self.to_recv[:n], self.to_recv[n:]
		return r

	def send(self, s):
		self.sent += s

	def close(self):
		self.is_closed = True