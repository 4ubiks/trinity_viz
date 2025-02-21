import re
import serial
import time
import threading as th

gps_data = {
            "Hour": 0,
            "Minute": 0,
            "Seconds": 0,
            "Milliseconds": 0,
            "Altitude": 0,
            "Latitude": 0,
            "Longitude": 0,
            "Horizontal_Velocity": 0,
            "Horizontal_Heading": 0,
            "Vertical_Velocity": 0,
            "Satellite": 0
        }
ser: serial.Serial

running = False

# Parse a string of data into a dictionary
def parse_data(parsed_data: dict, line: str) -> None:
    global gps_data

    # Regular expression to match the data
    data_regex = re.compile(
        r"(\d{2}):(\d{2}):(\d{2})\.(\d{3}).*Alt\s+(\d+)\s+lt\s+([\+\-]?\d+\.\d+)\s+ln\s+([\+\-]?\d+\.\d+)\s+Vel\s+([\+\-]\d+)\s+([\+\-]\d+)\s+([\+\-]\d+)\s+Fix\s+(\d+)")

    # Parse the input string
    match = re.search(data_regex, line)
    if match:
        # Obtain data and insert it into dictionary
        parsed_data.update({
            "Hour": float(match.group(1)),
            "Minute": float(match.group(2)),
            "Seconds": float(match.group(3)),
            "Milliseconds": float(match.group(4)),
            "Altitude": float(match.group(5)),
            "Latitude": float(match.group(6)),
            "Longitude": float(match.group(7)),
            "Horizontal_Velocity": float(match.group(8)),
            "Horizontal_Heading": float(match.group(9)),
            "Vertical_Velocity": float(match.group(10)),
            "Satellite": float(match.group(11))
        })
        gps_data.update(parsed_data)

# Connect to serial port 'com_port'
def connect_serial(com_port: str) -> None:
    global ser
    global running

    # Serial communication setup
    ser = serial.Serial(
        port=com_port,
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=0)

    print("connected to: " + ser.portstr)
    running = True

    # Variables for storing parsed data
    final = {}
    seq = []
    count = 1

    while True:
        for c in ser.read():
            seq.append(chr(c))
            joined_seq = ''.join(str(v) for v in seq)

            if chr(c) == '\n':
                #print(joined_seq)

                # Check if the line starts with "@ GPS_STAT"
                if joined_seq.startswith("@ GPS_STAT"):
                    parse_data(final, joined_seq)
                    print(final)

                seq = []
                count += 1
                break

# Disconnect serial reader
def disconnect_serial() -> None:
    global ser
    global running

    running = False

    if 'ser' in globals() and ser is not None:
        ser.close()
        ser = None