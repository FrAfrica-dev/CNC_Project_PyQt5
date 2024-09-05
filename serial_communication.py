# serial_communication.py
import serial

class SerialCommunication:
    def __init__(self):
        self.serial_connection = None

    def open_connection(self, port, baud_rate):
        """Opens a serial connection to the CNC."""
        try:
            self.serial_connection = serial.Serial(port, baud_rate, timeout=1)
            print(f"Connected to {port} at {baud_rate} baud.")
            return True
        except serial.SerialException as e:
            print(f"Error opening serial port: {e}")
            return False

    def send_gcode(self, file_name):
        """Sends G-code commands from the file to the CNC."""
        if self.serial_connection:
            with open(file_name, 'r') as file:
                for line in file:
                    command = line.strip()
                    self.serial_connection.write(f"{command}\n".encode())
                    response = self.serial_connection.readline().decode().strip()
                    print(f"Sent: {command}, Response: {response}")
        else:
            print("No active serial connection")

    def close_connection(self):
        """Closes the serial connection."""
        if self.serial_connection:
            self.serial_connection.close()
            print("Serial connection closed")
