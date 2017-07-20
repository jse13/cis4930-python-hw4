from __future__ import print_function
from browser import HTTPConnection


def test_course_website():
    conn = HTTPConnection("www.cs.fsu.edu")
    conn.request("GET", "/~carnahan/cis4930/")
    resp = conn.getresponse()
    print("Version: ", resp.version)
    print("Status: ", resp.status)
    print("Reason: ", resp.reason)
    print("Headers: ", resp.getheaders())
    print("Value of Date header: ", resp.getheader("Date"))
    print("First 10 bytes of body: ", resp.read(10))
    print("Rest of body: ", resp.read())
    print("Trying to read more: ", resp.read(20))

def test_wrong_page():
    conn = HTTPConnection("www.cs.fsu.edu")
    # Requesting non-existent page
    conn.request("GET", "/~carnahan/cis430/")
    resp = conn.getresponse()
    print("Version: ", resp.version)
    print("Status: ", resp.status)
    print("Reason: ", resp.reason)
    print("Headers: ", resp.getheaders())
    print("Value of Date header: ", resp.getheader("Date"))
    print("First 10 bytes of body: ", resp.read(10))
    print("Rest of body: ", resp.read())


def test_head_request():
    conn = HTTPConnection("www.cs.fsu.edu")
    # Requesting non-existent page                                                                             
    conn.request("HEAD", "/~carnahan/cis4930/", )
    resp = conn.getresponse()
    print("Version: ", resp.version)
    print("Status: ", resp.status)
    print("Reason: ", resp.reason)
    print("Headers: ", resp.getheaders())
    print("Value of Date header: ", resp.getheader("Date"))
    print("First 10 bytes of body: ", resp.read(10))
    print("Rest of body: ", resp.read())

def test_get_request_2():
    conn = HTTPConnection("www.cs.fsu.edu")                                 
    conn.request("GET", "/~carnahan/cda3101/", {"User-agent": "browser/1.0", "Accept-Language": "en-US,en;q=0.5"})
    resp = conn.getresponse()
    print("Version: ", resp.version)
    print("Status: ", resp.status)
    print("Reason: ", resp.reason)
    print("Headers: ", resp.getheaders())
    print("Value of Date header: ", resp.getheader("Date"))
    print("First 100 bytes of body: ", resp.read(100))



if __name__ == "__main__":
    test_course_website()
    print("********************")
    test_wrong_page()
    print("********************")
    test_head_request()
    print("********************")
    test_get_request_2()
