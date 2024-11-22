import re
import serial
import time
import threading as th

def parse_data(parsed_data: dict, line: str) -> None:
    # Regular expression to match the data
    data_regex = re.compile(
        r"(\d{2}):(\d{2}):(\d{2})\.(\d{3}).*Alt\s+(\d+)\s+lt\s+([\+\-]?\d+\.\d+)\s+ln\s+([\+\-]?\d+\.\d+)\s+Vel\s+([\+\-]\d+)\s+([\+\-]\d+)\s+([\+\-]\d+)\s+Fix\s+(\d+)")

    # Parse the input string
    match = re.search(data_regex, line)
    if match:
        # Obtain data and insert it into dictionary
        parsed_data.update({
            "Hour": match.group(1),
            "Minute": match.group(2),
            "Seconds": match.group(3),
            "Milliseconds": match.group(4),
            "Altitude": match.group(5),
            "Latitude": match.group(6),
            "Longitude": match.group(7),
            "Horizontal_Velocity": match.group(8),
            "Horizontal_Heading": match.group(9),
            "Vertical_Velocity": match.group(10),
            "Satellite": match.group(11)
        })

def connect_serial(com_port: str) -> None:
    # Serial communication setup
    ser = serial.Serial(
        port=com_port,
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=0)

    print("connected to: " + ser.portstr)

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

                # Check if the line starts with "@GPS_STAT"
                if joined_seq.startswith("@ GPS_STAT"):
                    parse_data(final, joined_seq)
                    print(final)

                seq = []
                count += 1
                break

    ser.close()

def thread():
    for i in range(50):
        print(f"Counting thread: {i}")
        time.sleep(1)

def live_data_th() -> th.Thread:
    t = th.Thread(target=thread, args=[])
    t.start()
    return t

if __name__ == '__main__':
    connect_serial('COM4')
else:
    print("'live_dtat.py' imported.")