import socket

def receive_data_from_pi(pc_ip, pc_port):
    try:
        # Create a socket object
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Bind the socket to the IP and port
        server_socket.bind((pc_ip, pc_port))
        
        # Listen for incoming connections
        server_socket.listen(1)
        print("Waiting for connection...")
        
        # Accept a connection
        conn, addr = server_socket.accept()
        print(f"Connected by {addr}")
        return conn
        # Receive data
        #data = conn.recv(1024).decode('utf-8')
        #print(f"Received data: {data}")
        
        # Close the connection
        #conn.close()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    pc_ip = "192.168.1.4"  # Replace with your PC's IP address
    pc_port = 65432  # Replace with the port number you want to use
    receive_data_from_pi(pc_ip, pc_port)
