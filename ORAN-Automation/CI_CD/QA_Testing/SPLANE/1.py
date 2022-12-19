import sys, getpass, telnetlib

def telnet_connect(hostname, username, password):
    t = telnetlib.Telnet(hostname,port=8888)            # actively connects to a telnet server
    # t.set_debuglevel(1)                     # uncomment to get debug messages
    t.read_until(b'login:', 10)               # waits until it recieves a string 'login:'
    t.write(username.encode('utf-8'))         # sends username to the server
    t.write(b'\r')                            # sends return character to the server
    t.read_until(b'Password:', 10)            # waits until it recieves a string 'Password:'
    t.write(password.encode('utf-8'))         # sends password to the server
    t.write(b'\r')                            # sends return character to the server
    n, match, previous_text = t.expect([br'Login incorrect', br'\$'], 10)
    if n == 0:
        print('Username and password failed - giving up')
    else:
        t.write(b'get-SwInv\r')             # sends a command to the server
        # t.write(b'exec exit\r')
        print(t.read_all().decode('utf-8'))  # read until socket closes
    t.close()

if __name__ == '__main__':
    if len(sys.argv) < 2: 
        print ("Usage: python telnet_login.py hostname username")
    hostname = "192.168.59.37"
    username = "oranuser"
    password = getpass.getpass('Password: ')
    telnet_connect(hostname, username, password)

    