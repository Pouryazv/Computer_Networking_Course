import socket
import threading
import math
import datetime


def calculate(operator, op1, op2):
    result = None
    if operator == "Add":
        result = op1 + op2
    elif operator == "Subtract":
        result = op1 - op2
    elif operator == "Multiply":
        result = op1 * op2
    elif operator == "Divide":
        result = op1 / op2
    elif operator == "Sin":
        result = math.sin(op1)
    elif operator == "Cos":
        result = math.cos(op1)
    elif operator == "Tan":
        result = math.tan(op1)
    elif operator == "Cot":
        result = 1 / math.tan(op1)
    return result


def handle_client(client_socket):
    hello_msg = client_socket.recv(1024).decode().strip()
    if hello_msg != "Hello":
        client_socket.close()
        return

    server_hello = "Hello"
    client_socket.send(server_hello.encode())

    request = client_socket.recv(1024).decode().strip()
    request_parts = request.split("$")
    operator = request_parts[1].strip()
    op1 = float(request_parts[2].strip())
    op2 = float(request_parts[3].strip())

    result = calculate(operator, op1, op2)

    time = datetime.datetime.now().time()
    response = f"${operator}  ${time}  ${result}"

    client_socket.send(response.encode())
    client_socket.close()


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 8044))
    server_socket.listen(5)
    print("Server started. Listening on port 8044...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address[0]}:{client_address[1]}")

        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()


start_server()
