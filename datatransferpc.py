import socket

def receive_data_from_pi(pc_ip, pc_port):
    try:
        # initialize socket object
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # bind socket to ip and port
        server_socket.bind((pc_ip, pc_port))
        
        # wait for connection
        server_socket.listen(1)
        print("Waiting for connection...")
        
        # accept connection
        conn, addr = server_socket.accept()
        print(f"Connected by {addr}")
        return conn

    except Exception as e:
        print(f"error: {e}")

if __name__ == "__main__":
    pc_ip = "192.168.1.4" 
    pc_port = 65432
    receive_data_from_pi(pc_ip, pc_port)
