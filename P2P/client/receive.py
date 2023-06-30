import socket
from unittest import result


LISTENING_PORT = 12345
SERVER_PORT = 23456
BROADCAST_IP = "255.255.255.255"
TIMEOUT = 20
CHUNK_SIZE = 128

def receive_file(filename):
    # Create a UDP socket
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    udp_socket.settimeout(TIMEOUT)

    try:
        # Send the request to the broadcast IP
        udp_socket.bind(('', LISTENING_PORT))
        request_message = f"GET {filename.filename}".encode()
        udp_socket.sendto(request_message, (BROADCAST_IP, SERVER_PORT))
        print(f"Requesting file {filename.filename} via UDP broadcast to {BROADCAST_IP}:{SERVER_PORT}")

        # Wait for the response
        try:
            while True:
                response, sender_address = udp_socket.recvfrom(1024)
                print(f"Received response from {sender_address}:")
                msg = response.decode().split(" ")
                method = msg[0].strip()
                if method != "EXPECT":
                    print("invalid method")
                    continue

                chunks = {}
                chunk_len = int(msg[1].strip())
                i = 0
                while i < chunk_len:
                    response, sender_address = udp_socket.recvfrom(CHUNK_SIZE)
                    # Simple validation
                    msg = request_message.decode().split(" ")
                    if msg[0].strip() == "EXPECT":
                        print(f"invalid method, received EXPECTED from {sender_address}, expect chunk...")
                        continue
                    if chunks.get(int(response[0]), None) is not None:
                        print(f"duplicate chunk {int(response[0])} from {sender_address}")
                        continue

                    print(f"received chunk {int(response[0])} from {sender_address}")
                    chunks[int(response[0])] = response[1:]
                    i += 1
                
                print("Received all chunks, combining...")
                result = chunks[0]
                for i in range(1, chunk_len):
                    result += chunks[i]
                
                print("---------------------")
                print(str(result))   # for testing purpose
                with open(f"client/{filename.filename}", 'wb') as f:
                    f.write(result)
                break
        except socket.timeout:
            print("Timeout occurred. No data received.")

    finally:
        udp_socket.close()
