"""
Featherweight GPS Packet Reader
"""
import re

import serial

def parse_data(parsed_data, line):
    
    # Regular expression to match the data
    data_regex = re.compile(r"(\d{2}):(\d{2}):(\d{2})\.(\d{3}).*Alt\s+(\d+)\s+lt\s+([\+\-]?\d+\.\d+)\s+ln\s+([\+\-]?\d+\.\d+)\s+Vel\s+([\+\-]\d+)\s+([\+\-]\d+)\s+([\+\-]\d+)\s+Fix\s+(\d+)")

    # Parse the input strong
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
    return(final)



go="@ GPS_STAT 202 0000 00 00 00:43:45.329 CRC_OK  TRK tracker     Alt 000000 lt +00.00000 ln +00.00000 Vel +0000 +000 +0000 Fix 0 #  0  0  0  0 000_00_00 000_00_00 000_00_00 000_00_00 000_00_00 CRC: FD6F"
final={}
print(parse_data(final,go))

