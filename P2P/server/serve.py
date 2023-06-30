import socket


PORT = 23456
DATA_CHUNK_SIZE = 127

def serve_files(filepaths):
    # Create a UDP socket
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Loading the files
    files = {}
    for filename in filepaths.filepaths:
        with open(f"server/{filename}", 'rb') as f:
            files[filename] = f.read()

    try:
        udp_socket.bind(('', PORT))
        print(f"Server listening on port {PORT}")

        while True:
            # Receive the request message and sender's address
            request_message, sender_address = udp_socket.recvfrom(1024)
            print(f"Received request from {sender_address}:")
            # Convention
            msg = request_message.decode().split(" ")
            method = msg[0].strip()
            if method != "GET":
                print("invalid method")
                continue
            filename = msg[1].strip()
            if filename not in files.keys():
                print("requested file does not exist")
                continue

            # Reading and chunking the file
            data = files[filename]
            chunks = [data[i:i+DATA_CHUNK_SIZE] for i in range(0, len(data), DATA_CHUNK_SIZE)]
            expect_message = f"EXPECT {len(chunks)} CHUNKS".encode()
            udp_socket.sendto(expect_message, sender_address)

            # Sending the chunks
            for i, chunk in enumerate(chunks):
                sequence_number = i.to_bytes(1, byteorder='big')
                chunk_with_sequence = sequence_number + chunk
                udp_socket.sendto(chunk_with_sequence, sender_address)

            print(f"Response sent to {sender_address}")

    finally:
        udp_socket.close()