import socket

def send_data_to_pc(pc_ip, pc_port):
    try:
        # Create a socket object
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Connect to the PC
        client_socket.connect((pc_ip, pc_port))
        
        # Send data
        #client_socket.sendall(data.encode('utf-8'))
        
        # Close the connection
        #client_socket.close()
        #print("Data sent successfully!")
        return client_socket
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    data = "Hello from Raspberry Pi!"
    pc_ip = "192.168.1.4"  # Replace with your PC's IP address
    pc_port = 65432  # Replace with the port number you want to use
    send_data_to_pc(data, pc_ip, pc_port)
