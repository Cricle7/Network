import socket

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to an address and port
server_address = ('localhost', 10000)
sock.bind(server_address)

print('Waiting to receive message')
data, addr = sock.recvfrom(1500)

# Check if the received data is at least 12 bytes
if len(data) >= 12:
    # Strip off the first 12 bytes (RTP header)
    payload = data[12:]

    # Write the remaining data to a file
    with open('data.txt', 'wb') as file:
        file.write(payload)
    print('Payload written to data.txt')
else:
    print('Received data is less than 12 bytes, cannot strip RTP header')
