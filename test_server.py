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

# Test a basic GET call.

def test_handle_connection_slash():
    conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")
    header = 'HTTP/1.0 200 OK\r\n' + \
             'Content-type: text/html\r\n' + \
             '\r\n'
    body = """
        <h1>Hello, world.</h1>This is hoffm386's Web server.
        <ul>
          <li><a href='/content'>Content</a></li>
          <li><a href='/file'>File</a></li>
          <li><a href='/image'>Image</a></li>
        </ul>
        """
    expected_return = header + body

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_content():
    conn = FakeConnection("GET /content HTTP/1.0\r\n\r\n")
    header = 'HTTP/1.0 200 OK\r\n' + \
             'Content-type: text/html\r\n' + \
             '\r\n'
    body = """
        <h1>Content</h1>
        This page will contain "content"
        """
    expected_return = header + body

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_file():
    conn = FakeConnection("GET /file HTTP/1.0\r\n\r\n")
    header = 'HTTP/1.0 200 OK\r\n' + \
             'Content-type: text/html\r\n' + \
             '\r\n'
    body = """
        <h1>File</h1>
        This page will contain "file"
        """
    expected_return = header + body

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_image():
    conn = FakeConnection("GET /image HTTP/1.0\r\n\r\n")
    header = 'HTTP/1.0 200 OK\r\n' + \
             'Content-type: text/html\r\n' + \
             '\r\n'
    body = """
        <h1>Image</h1>
        This page will contain an "image"
        """
    expected_return = header + body

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_post():
    conn = FakeConnection("POST / HTTP/1.1\r\n\r\n")
    header = 'HTTP/1.0 200 OK\r\n' + \
             'Content-type: text/html\r\n' + \
             '\r\n'
    body = """
    <h1>Post Request</h1>
    This is not actually what a post request will do, but I have received
    a post request
    """
    expected_return = header + body
    server.handle_connection(conn)
    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)
