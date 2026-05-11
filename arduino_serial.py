import serial
import time

class ArduinoReader:
    def __init__(self, port, baudrate):
        self.port = port
        self.baudrate = baudrate

        self.latest_data = {"temp": 22.0, "moisture": 50.0, "uv": 40}  # default values
        self.ser = None

        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
            time.sleep(2)  # wait for the connection to initialize
            print(f"Connected to Arduino on {self.port} at {self.baudrate} baud.")
        except serial.SerialException:
            print(f"Warning: Could not connect to Arduino on {self.port}. Using default sensor values.")
            self.ser = None

    def get_data(self): 
        """Reads a line from Arduino and updates the latest_data dictionary."""
        if not self.ser:
            return self.latest_data  # return default values if not connected
        
        try: 
            if self.ser.in_waiting > 0:
                line = ""
                while self.ser.in_waiting > 0:
                    line = self.ser.readline().decode('utf-8').strip()
                
                part = line.split(",")
                # Change this part inside your get_data method:
                if len(part) == 3:
                    self.latest_data = {
                        "moisture": int(float(part[0])), # First value (A0)
                        "uv":       int(float(part[1])), # Second value (A1)
                        "temp":     float(part[2])       # Third value (A2) - Keep as float for 21.8
                    
                    }
        except Exception as e:
            pass

        return self.latest_data

    