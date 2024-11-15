using System;
using System.Collections.Generic;
using System.IO.Ports;
using System.Text;
using System.Text.RegularExpressions;

class Program
{
    static void Main(string[] args)
    {
        // Serial communication setup
        SerialPort serialPort = new SerialPort
        {
            PortName = "COM3",
            BaudRate = 115200,
            Parity = Parity.None,
            StopBits = StopBits.One,
            DataBits = 8,
            ReadTimeout = 0
        };

        serialPort.Open();
        Console.WriteLine("Connected to: " + serialPort.PortName);

        // Variables for storing parsed data
        var final = new Dictionary<string, string>();
        var seq = new List<byte>();
        int count = 1;

        while (true)
        {
            try
            {
                // Reading one byte at a time
                int byteRead = serialPort.ReadByte();
                if (byteRead == -1)
                    break;

                // Append the byte to the sequence
                seq.Add((byte)byteRead);

                // Join the sequence into a string
                string joinedSeq = Encoding.ASCII.GetString(seq.ToArray());

                // Check for newline character
                if ((char)byteRead == '\n')
                {
                    // If the line starts with "@GPS_STAT", parse the data
                    if (joinedSeq.StartsWith("@ GPS_STAT"))
                    {
                        Console.WriteLine(ParseData(final, joinedSeq));
                    }

                    // Reset sequence and increment count
                    seq.Clear();
                    count++;
                }
            }
            catch (TimeoutException)
            {
                // Handle timeout if needed (optional)
            }
        }

        serialPort.Close();
    }

    static string ParseData(Dictionary<string, string> parsedData, string line)
    {
        // Regular expression to match the data
        var dataRegex = new Regex(
            @"(\d{2}):(\d{2}):(\d{2})\.(\d{3}).*Alt\s+(\d+)\s+lt\s+([\+\-]?\d+\.\d+)\s+ln\s+([\+\-]?\d+\.\d+)\s+Vel\s+([\+\-]\d+)\s+([\+\-]\d+)\s+([\+\-]\d+)\s+Fix\s+(\d+)",
            RegexOptions.Compiled);

        // Parse the input string using regex
        var match = dataRegex.Match(line);
        if (match.Success)
        {
            // Insert matched data into dictionary
            parsedData["Hour"] = match.Groups[1].Value;
            parsedData["Minute"] = match.Groups[2].Value;
            parsedData["Seconds"] = match.Groups[3].Value;
            parsedData["Milliseconds"] = match.Groups[4].Value;
            parsedData["Altitude"] = match.Groups[5].Value;
            parsedData["Latitude"] = match.Groups[6].Value;
            parsedData["Longitude"] = match.Groups[7].Value;
            parsedData["Horizontal_Velocity"] = match.Groups[8].Value;
            parsedData["Horizontal_Heading"] = match.Groups[9].Value;
            parsedData["Vertical_Velocity"] = match.Groups[10].Value;
            parsedData["Satellite"] = match.Groups[11].Value;
        }

        // Convert the parsed data to a formatted string (you can modify this format)
        StringBuilder result = new StringBuilder();
        foreach (var key in parsedData.Keys)
        {
            result.AppendLine($"{key}: {parsedData[key]}");
        }

        return result.ToString();
    }
}
