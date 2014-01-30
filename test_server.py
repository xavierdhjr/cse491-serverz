import server

class FakeConnection(object):
    """
    A fake connection class that mimics a real TCP socket for the purpose
    of testing socket I/O.
    """
    def __init__(self, to_recv):
        self.to_recv = to_recv
        self.sent = ""
        self.is_closed = False

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

def test_handle_connection_form_get():
	conn = FakeConnection("GET /submit?ccn=999&ssn=111 HTTP/1.0\r\n\r\n")
	expected_return = 'HTTP/1.0 200 OK\r\n' + \
			'Content-type: text/html\r\n' + \
			'\r\n' +\
			"<html><body>Thanks. You have won. Your information: " + \
			"<br/>CC:999 <br/>SSN:111 " +  \
			"<br/><img src='http://bhpmss.org/yahoo_site_admin/assets/images/money.135143522.jpg'/>" + \
			"</body></html>"
			
	server.handle_connection(conn)

	assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_form_post():
	conn = FakeConnection(
		"POST /submit HTTP/1.0\r\n\r\n" + \
		"ccn=999&ssn=333")
	expected_return = 'HTTP/1.0 200 OK\r\n' + \
			'Content-type: text/html\r\n' + \
			'\r\n' +\
			"<html><body>Thanks. You have won. Your information: " + \
			"<br/>CC:999 <br/>SSN:333 " +  \
			"<br/><img src='http://bhpmss.org/yahoo_site_admin/assets/images/money.135143522.jpg'/>" + \
			"</body></html>"
			
	server.handle_connection(conn)

	assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)
# Test a basic GET call.

def test_handle_connection_root():
	conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")
	expected_return = 'HTTP/1.0 200 OK\r\n' + \
					'Content-type: text/html\r\n' + \
					'\r\n' + \
					'<html><body>\n' + \
					'<h1>Hello world!</h1>This is xavierdhjr\'s web server.\n' + \
					'<br/><a href="/form.html">Form</a>\n' + \
					'<br/><a href="/form_post.html">Form (POST)</a>\n' + \
					'<br/><a href="/content.html">Content</a>\n' + \
					'<br/><a href="/file.html">File</a>\n' + \
					'<br/><a href="/image.html">Image</a>\n' + \
					'</body></html>'

	server.handle_connection(conn)

	assert conn.sent == expected_return, 'Expected\n %s \n\n Got\n%s' % (repr(expected_return),repr(conn.sent))
	
def test_handle_connection_content():
	conn = FakeConnection("GET /content.html HTTP/1.0\r\n\r\n")
	expected_return = 'HTTP/1.0 200 OK\r\n' + \
					'Content-type: text/html\r\n' + \
					'\r\n' + \
					'<html><body><h1>Content</h1>This is xavierdhjr\'s Web server.</body></html>'

	server.handle_connection(conn)

	assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)
	
def test_handle_connection_file():
	conn = FakeConnection("GET /file.html HTTP/1.0\r\n\r\n")
	expected_return = 'HTTP/1.0 200 OK\r\n' + \
					'Content-type: text/html\r\n' + \
					'\r\n' + \
					'<html><body><h1>File</h1>This is xavierdhjr\'s Web server.</body></html>'

	server.handle_connection(conn)

	assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)
	
def test_handle_connection_image():
	conn = FakeConnection("GET /image.html HTTP/1.0\r\n\r\n")
	expected_return = 'HTTP/1.0 200 OK\r\n' + \
					'Content-type: text/html\r\n' + \
					'\r\n' + \
					'<html><body><h1>Image</h1>This is xavierdhjr\'s Web server.</body></html>'

	server.handle_connection(conn)

	assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)
	