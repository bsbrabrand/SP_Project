import bluetooth #need to install? Bluez library for linux
import time

class monitor:
    def __init__(self):
        # the heart rate monitor bluetooth address
        self.address = "F3:7C:B0:DD:7C:D0"

        # Create a socket
        self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        
        try:
            # Connect to the heart rate monitor
            self.sock.connect((address, 1))
            print("Connected to heart rate monitor.")
        except Exception as e:
            print(f"An error occured: {e}")
            self.sock = None

   def get_heart_rate(self):
        if self.sock:
            try:
                data = self.sock.recv(1024)
                print(f"Raw Data: {data}")
                # Optional: Parse the data depending on your HRM's protocol
                return data
            except Exception as e:
                print(f"Error receiving data: {e}")
                return None
        else:
            print("Socket not connected.")
            return None

    def close(self):
        if self.sock:
            self.sock.close()
            print("Connection closed.")

if __name__ == "__main__":
    hr_monitor = Monitor()
    for i in range(100):
        hr_monitor.get_heart_rate()
        time.sleep(1)  # small delay between readings
    hr_monitor.close()
