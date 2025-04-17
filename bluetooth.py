class monitor:
    def __init__():
        import bluetooth #need to install? Bluez library for linux
        import time
        # Replace with the actual address of your heart rate monitor
        address = "F3:7C:B0:DD:7C:D0"

        # Create a socket
        sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        try:
            # Connect to the heart rate monitor
            sock.connect((address, 1))

            

        except Exception as e:
            print(f"An error occurred: {e}")


    def get_heart_rate(self):
        # Read data from the socket
        data = self.sock.recv(1024)
        return data

    def close(self):
            # Close the socket
            self.sock.close()

if __name__ == "__main__":
    a = monitor()
    for i in range(100):
        a.get_heart_rate()
    a.close() #riley was here