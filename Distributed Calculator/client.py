import socket


def send_request(request):
    server_address = ("localhost", 8044)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect(server_address)
    except ConnectionRefusedError:
        print("Connection refused. Server may not be running.")
        return

    hello_msg = "Hello"
    client_socket.send(hello_msg.encode())

    server_hello = client_socket.recv(1024).decode().strip()
    if server_hello != "Hello":
        client_socket.close()
        return "Handshake failed"

    # Send the calculation request
    client_socket.send(request.encode())

    response = client_socket.recv(1024).decode().strip()
    client_socket.close()
    return response


while True:
    user_input = input("Enter calculation request (or 'FINISH' to exit): ")

    if user_input == "FINISH":
        break

    request_parts = user_input.split("$")
    if len(request_parts) != 4:
        print("Invalid request format.")
        continue

    operator = request_parts[1].strip()
    op1 = request_parts[2].strip()
    op2 = request_parts[3].strip()

    if operator not in ["Add", "Subtract", "Multiply", "Divide", "Sin", "Cos", "Tan", "Cot"]:
        print("Invalid operator.")
        continue

    try:
        op1 = float(op1)
        op2 = float(op2)
    except ValueError:
        print("Invalid operands. Both operands must be numbers.")
        continue

    response = send_request(user_input)
    print("Response:", response)

print("Client disconnected.")
