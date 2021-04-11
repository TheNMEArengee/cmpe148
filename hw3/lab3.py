from socket import *
import ssl
import base64

subject = "Subject: A Message From A Fatui Skirmisher\r\n\r\n"
msg = "\r\n Sumetukk Sukk Sukk"
endmsg = "\r\n.\r\n"


# TODO: Choose a mail server (e.g. Google mail server) and call it mailserver
# mailserver = ("smtp.gmail.com", 587)
mailserver = ("smtp.gmail.com", 587)


# TODO: Create socket called clientSocket and establish a TCP connection with mail server
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(mailserver)
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '220':
    print('220 reply not received from server.')

# Send HELO command and print server response.
heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != '250':
    print('250 reply not received from server. 1st HELO.')

# Gmail Requires TLS
startTls = 'STARTTLS\r\n'
clientSocket.send(startTls.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != '220':
    print('220 reply not received from server. STARTTLS.')

# We could not read the HELO response after STARTTLS, so we wrapped
# our socket with SSL and continued the process with the wrapped socket.
# scs stands for SSL Client Socket.
scs = ssl.wrap_socket(clientSocket, ssl_version=ssl.PROTOCOL_SSLv23)

# Send HELO after TLS to check if it worked
scs.send('HELO Alice\r\n'.encode())
recv1 = scs.recv(1024).decode()
print(recv1)
if recv1[:3] != '250':
    print('250 reply not received from server. 2nd HELO.')

# Send AUTH LOGIN to log in by sending Gmail account credentials
scs.send('AUTH LOGIN\r\n'.encode())
recv1 = scs.recv(1024).decode()
print(recv1)
if recv1[:3] != '334':
    print('334 reply not received from server. AUTH LOGIN.')

# Account Credentials
email = base64.b64encode('insertemailhere@gmail.com'.encode()) + '\r\n'.encode()
password = base64.b64encode('insertpasswordhere'.encode()) + '\r\n'.encode()

scs.send(email)
recv1 = scs.recv(1024).decode()
print(recv1)
if recv1[:3] != '334':
    print('334 reply not received from server. Send email.')

scs.send(password)
print(recv1)
if recv1[:3] != '334':
    print('334 reply not received from server. Send password.')

# If no issues from here, we have logged in successfully
# Now, we can send the sender and recipient information
mailFrom = "MAIL FROM: <testing123kapp@gmail.com>\r\n"
scs.send(mailFrom.encode())
recv1 = scs.recv(1024).decode()
print(recv1)
if recv1[:3] != '235':
    print('235 reply not received from server. MAIL FROM.')

rcptTo = "RCPT TO: <jonsay157@gmail.com>\r\n"
# rcptTo = "RCPT TO: <testing123kapp@gmail.com>\r\n"
scs.send(rcptTo.encode())
recv1 = scs.recv(1024).decode()
print(recv1)
if recv1[:3] != '250':
    print('250 reply not received from server. RCPT TO.')

# Now, we send the data and email contents (previously defined)
data = "DATA\r\n"
scs.send(data.encode())
recv1 = scs.recv(1024).decode()
print(recv1)
if recv1[:3] != '250':
    print('250 reply not received from server. DATA.')

scs.send(subject.encode())
scs.send(msg.encode())
scs.send(endmsg.encode())

# The message is sent. Send QUIT command.
scs.send('QUIT\r\n'.encode())
recv1 = scs.recv(1024).decode()
print(recv1)
if recv1[:3] != '354':
    print('354 reply not received from server. QUIT.')

# Close socket connections
clientSocket.close()
scs.close()