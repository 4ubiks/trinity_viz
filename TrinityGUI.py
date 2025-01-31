# External dependencies
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from datetime import datetime, timedelta
import matplotlib.dates as mdates
from pyautogui import size
from tkintermapview import TkinterMapView
from psutil import cpu_percent
import time
import threading
import re
import serial
import time
import threading as th

# import multiprocessing // never used
import os

#import live_data

os.chdir(os.path.dirname(__file__))
#os.chdir("../resources")

"""
BG_COLOR = "#c8d6d8"
FEATURE_COLOR = "#d9d9d9"
FEATURE_BG = "#F1F1F1"

"""


SCREEN_SIZE = tuple(size())
WIN_GEOMETRY = "x".join((str(SCREEN_SIZE[0]-20), str(SCREEN_SIZE[1]-80)))
WIN_TITLE = "Liberty Rocketry Ground Station"
BG_COLOR = "#c8d6d8"
FEATURE_COLOR = "#d9d9d9"
FEATURE_BG = "#F1F1F1"
WHITE = "#ffffff"
START_FULLSCREEN = False
PADDING = 5

## Global variables ##
serial_buffer: list[str] = []

class FrameBase(tk.Frame):
    def __init__(self, parent: tk.Tk):
        super().__init__(parent, bg=WHITE)
        self.pack(expand=True, fill="both", padx=PADDING, pady=PADDING)

        self.construct_section()

    def construct_section(self) -> None:     # dummy method to be defined by children
        pass

class MapFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=WHITE)
        self.pack(expand=True, fill="both", padx=PADDING, pady=PADDING)

        self.construct_section()

    def construct_section(self):
        map_widget = TkinterMapView(self, width=SCREEN_SIZE[0]//30 - 60, corner_radius=0)
        map_widget.place(anchor='nw', relx=0, rely=0, relwidth=1, relheight=1)

        # Set Google normal tile server
        map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

        # Set an address for the marker
        map_widget.set_address("New York City", marker=True)

class ControlsFrame(FrameBase):
    TOP_ROW_REL_POS = 0.095
    TOP_ROW_HEIGHT = 35
    SECOND_ROW_REL_POS = 0.57

    class ButtonsFrame(tk.Frame):
        def __init__(self,  parent):
            super().__init__(parent, bg=WHITE)
            self.place(anchor="w", relx=0.025, rely=ControlsFrame.SECOND_ROW_REL_POS)

            buttons = ["Toggle cameras", "Start/stop flight", "Export flight", "View flights", \
                       "MISC 1"]
            if len(buttons) > 10:
                pass
            for btn in buttons:
                tk.Button(
                    self,
                    text=btn,
                    command=lambda: alert(f"'{btn}' pressed"),
                    padx=10,
                    bg=FEATURE_COLOR,
                    relief="flat"
                ).pack(pady=2, expand=True, fill="both")

    class COMSelector(tk.Frame):
        def __init__(self, parent):
            options: tuple[str] = ("- select -",) + tuple(("0" + str(x) for x in range(1, 10)))

            super().__init__(parent, bg=FEATURE_COLOR, height=ControlsFrame.TOP_ROW_HEIGHT, \
                                    width=400)
            self.place(anchor="w", relx=0.025, rely=ControlsFrame.TOP_ROW_REL_POS)

            com_selector_label = ttk.Label(self, text="COM Port:", font="Noto 16", \
                                        anchor="w", background=FEATURE_COLOR)
            com_selector_label.pack(side="left", padx=10)

            com_selector_drop_down = ttk.Combobox(self, textvariable = None, font=None, state='readonly')
            com_selector_drop_down['values'] = options
            com_selector_drop_down.current(0)
            com_selector_drop_down.unbind_class("TCombobox", "<MouseWheel>")
            com_selector_drop_down.configure(width=7)
            com_selector_drop_down.pack(padx=10, pady=5)

    def construct_section(self) -> None:
        self.configure(height=300)
        self.pack(expand=False, fill="x", padx=PADDING, pady=PADDING)

        # Controls Label
        section_label = ttk.Label(self, text="Controls", font="Noto 20", \
                                  anchor="center", background=FEATURE_COLOR)
        section_label.place(anchor="center", relx=0.5, rely=ControlsFrame.TOP_ROW_REL_POS, \
                            height=ControlsFrame.TOP_ROW_HEIGHT, width=150)
        # COM Selector
        ControlsFrame.COMSelector(self)
        # Button Column
        ControlsFrame.ButtonsFrame(self)
        # Console Panel
        self.sc = ScrolledText(self, relief="solid")
        self.sc.configure(height=12, width=60)
        self.sc.place(anchor="w", relx=0.325, rely=ControlsFrame.SECOND_ROW_REL_POS)
        self.sc.insert(tk.INSERT, "- Console Output -")
        self.sc.config(state=tk.DISABLED)

        self.sc.after(1000, self.new_text)

    def new_text(self) -> None:
        buff_copy = list(serial_buffer)
        for e, i in enumerate(buff_copy):
            self.sc.insert(tk.INSERT, str(e))
            del serial_buffer[i]

        self.sc.after(1000, self.new_text)

class GraphsFrame(FrameBase):
    class Graph(tk.Frame):
        def __init__(self, parent: tk.Frame):
            # nb_points: number of points for the graph
            nb_points = 100
            super().__init__(parent, bg=FEATURE_BG)
            self.pack(expand=True, fill="both", padx=PADDING, pady=PADDING)
            # matplotlib figure
            self.figure = Figure(constrained_layout=True, dpi=100)
            self.ax = self.figure.add_subplot(111)
            # format the x-axis to show the time
            myFmt = mdates.DateFormatter("%H:%M:%S")
            self.ax.xaxis.set_major_formatter(myFmt)

            # initial x and y data
            dateTimeObj = datetime.now() + timedelta(seconds=-nb_points)
            self.x_data = [dateTimeObj + timedelta(seconds=i) for i in range(nb_points)]
            self.y_data = [0]*nb_points
            # create the plot
            self.plot = self.ax.plot(self.x_data, self.y_data, label='CPU')[0]
            self.ax.set_ylim(0, 100)
            self.ax.set_xlim(self.x_data[0], self.x_data[-1])

            label = tk.Label(self, text="Example of Live Plotting")
            label.place(anchor='n', relheight=0.1, relwidth=1, relx=0.5, rely=0)
            self.canvas = FigureCanvasTkAgg(self.figure, self)
            self.canvas.get_tk_widget()\
                       .place(anchor='n', 
                              relwidth=1, 
                              relheight=0.9,
                              relx=0.5,
                              rely=0.1)
            # self.animate()

        def animate(self):
            # append new data point to the x and y data
            self.x_data.append(datetime.now())
            self.y_data.append(cpu_percent())
            # remove oldest data point
            self.x_data = self.x_data[1:]
            self.y_data = self.y_data[1:]
            #  update plot data
            self.plot.set_xdata(self.x_data)
            self.plot.set_ydata(self.y_data)
            self.ax.set_xlim(self.x_data[0], self.x_data[-1])
            self.canvas.draw_idle()  # redraw plot
            self.after(250, self.animate)  # repeat after 1s

    def construct_section(self) -> None:
        # Padding frame
        content_frame = tk.Frame(self, bg=WHITE)
        content_frame.pack(expand=True, fill="both", padx=PADDING, pady=PADDING)

        GraphsFrame.Graph(content_frame)
        GraphsFrame.Graph(content_frame)
        GraphsFrame.Graph(content_frame)

class ReadoutFrame(FrameBase):
    class Section(tk.Frame):
        def __init__(self, parent: tk.Frame, lbl_txt: str, unit: str):
            super().__init__(parent, bg=FEATURE_BG)
            self.pack(expand=True, fill="both", padx=PADDING, pady=PADDING)

            l = tk.Label(self, text=lbl_txt, font="Noto 20", justify='left', bg=FEATURE_BG)
            l.place(anchor='w', relx=0.03, rely=0.16)
            data_frame = tk.Frame(self, bg=WHITE)
            data_frame.place(anchor='n', relx=0.5, rely=0.27, relwidth=0.955, relheight=0.65)

            self.add_content(data_frame, unit)

        def add_content(self, data_frame: tk.Frame, unit: str) -> None:
            val_label = tk.Label(data_frame, text="0.00", font=("default", 60), anchor='e', bg=WHITE)
            val_label.place(anchor='w', relheight=0.6, relwidth=0.65, relx=0, rely=0.52)

            unit_label = tk.Label(data_frame, text=unit, font=("default", 45), anchor='sw', bg=WHITE)
            unit_label.place(anchor='e', relheight=0.6, relwidth=0.35, relx=1, rely=0.51)

    class GolbalPositionSection(Section):
        def add_content(self, data_frame: tk.Frame, unit: str) -> None:
            RELY = 0.51
            RELWIDTH = 0.70

            lat_val_label = tk.Label(data_frame, text="0.000000", font=("default", 40), anchor='e', bg=WHITE)
            lat_val_label.place(anchor='sw', relheight=0.3, relwidth=RELWIDTH, relx=0, rely=RELY + 0.01)

            lat_unit_label = tk.Label(data_frame, text=unit + " N", font=("default", 30), anchor='sw', bg=WHITE)
            lat_unit_label.place(anchor='se', relheight=0.3, relwidth=1-RELWIDTH, relx=1, rely=RELY)

            long_val_label = tk.Label(data_frame, text="0.000000", font=("default", 40), anchor='e', bg=WHITE)
            long_val_label.place(anchor='nw', relheight=0.3, relwidth=RELWIDTH, relx=0, rely=RELY + 0.01)

            long_unit_label = tk.Label(data_frame, text=unit + " W", font=("default", 30), anchor='sw', bg=WHITE)
            long_unit_label.place(anchor='ne', relheight=0.3, relwidth=1-RELWIDTH, relx=1, rely=RELY)

    def construct_section(self) -> None:
        pad_frame = tk.Frame(self)
        pad_frame.pack(expand=True, fill="both", padx=PADDING, pady=PADDING)

        l_column = tk.Frame(pad_frame, bg=WHITE)
        l_column.place(anchor='nw', relheight=1, relwidth=0.5, relx=0, rely=0)
        r_column = tk.Frame(pad_frame, bg=WHITE)
        r_column.place(anchor='nw', relheight=1, relwidth=0.5, relx=0.5, rely=0)

        s1 = ReadoutFrame.Section(l_column, "Altitude:", "ft")
        s2 = ReadoutFrame.Section(l_column, "Velocity:", "ft/s")
        s3 = ReadoutFrame.GolbalPositionSection(r_column, "Global position:", "°")
        s4 = ReadoutFrame.Section(r_column, "Acceleration:", "ft/s\u00B2")

class CustomTk(tk.Tk):
    def __init__(self):
        # Window properties
        super().__init__()

        self.attributes('-fullscreen', START_FULLSCREEN)
        if not START_FULLSCREEN:
            self.geometry(WIN_GEOMETRY + "+0+0")
        self.config(bg=BG_COLOR)
        #logo = tk.PhotoImage(file="logo.png")
        #self.iconphoto(False, logo)
        self.title(WIN_TITLE)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # Variables
        self._bg_color = tk.StringVar(self, BG_COLOR)

        # Construct columns
        content_frame = FrameBase(self)
        self.__add_content(content_frame)

    def __add_content(self, parent: tk.Frame) -> None:
        # column frame
        right_column = tk.Frame(parent, bg=BG_COLOR)
        right_column.pack(side="left", expand=True, fill="both")

        left_column = tk.Frame(parent, bg=BG_COLOR)
        left_column.pack(side="left", expand=True, fill="both")

        # Controls section
        ControlsFrame(right_column)
        # Graphs section
        GraphsFrame(right_column)
        # Map section
        MapFrame(left_column)
        # Live readout section
        ReadoutFrame(left_column)

def alert(s: str) -> None:
    wn = tk.Tk()
    size = (400, 50)
    wn.geometry(
        str(size[0]) + "x" \
        + str(size[1]) + "+" \
        + str(SCREEN_SIZE[0]//2 - size[0]//2) + "+" \
        + str(SCREEN_SIZE[1]//2 - size[1]//2)
    )
    tk.Label(wn, text="ALERT: " + s, font="Noto 16").pack(padx=50, pady=5)
    wn.mainloop()

def thread1(data: list) -> None:
    i = 0
    while True:
        time.sleep(1)
        data.append(i)

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

if __name__ == "__main__":
    # t = threading.Thread(target=thread1, args=(serial_buffer,))
    # t.start()
    #t = live_data.live_data_th()
    wn = CustomTk()
    wn.mainloop()
    #t.join()

