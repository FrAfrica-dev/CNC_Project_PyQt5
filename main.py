# main.py
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QFileDialog, QLabel, QComboBox
import serial.tools.list_ports
from serial_communication import SerialCommunication
from file_handling import FileHandler

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("CNC Controller")
        self.setGeometry(200, 200, 400, 300)
        
        # Initialize communication and file handler
        self.serial_com = SerialCommunication()
        self.file_handler = FileHandler()
        
        # Main layout
        layout = QVBoxLayout()

        # Dropdown for selecting serial port
        self.port_label = QLabel("Select Serial Port:")
        self.port_combo = QComboBox()
        self.refresh_serial_ports()
        layout.addWidget(self.port_label)
        layout.addWidget(self.port_combo)

        # Dropdown for selecting baud rate
        self.baud_label = QLabel("Select Baud Rate:")
        self.baud_combo = QComboBox()
        self.baud_combo.addItems(["9600", "115200"])  # Common baud rates for CNC
        layout.addWidget(self.baud_label)
        layout.addWidget(self.baud_combo)
        
        # Button for loading G-code files
        self.load_file_button = QPushButton("Load G-code File")
        self.load_file_button.clicked.connect(self.load_file)
        layout.addWidget(self.load_file_button)
        
        # Button for starting the job
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_job)
        layout.addWidget(self.start_button)
        
        # Container for layout
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def refresh_serial_ports(self):
        """Fetches available serial ports and populates the combo box."""
        ports = serial.tools.list_ports.comports()
        self.port_combo.clear()
        for port in ports:
            self.port_combo.addItem(port.device)

    def load_file(self):
        """Loads a G-code file and adds it to the queue."""
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open G-code File", "", "G-code Files (*.gcode);;All Files (*)", options=options)
        if file_name:
            self.file_handler.add_file(file_name)

    def start_job(self):
        """Starts sending the G-code files to the CNC."""
        port = self.port_combo.currentText()
        baud_rate = self.baud_combo.currentText()
        if self.serial_com.open_connection(port, baud_rate):
            for file in self.file_handler.file_queue:
                self.serial_com.send_gcode(file)
            self.serial_com.close_connection()
        else:
            print("Failed to open serial connection")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
