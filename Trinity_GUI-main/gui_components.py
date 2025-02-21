import sys
import live
from random import randint
from threading import Thread
from time import sleep
from PySide6.QtWidgets import (
    QMainWindow, QApplication, QWidget, QLabel, QToolBar, QStatusBar, QVBoxLayout, QComboBox
)
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import Qt, QTimer

from pglive.sources.data_connector import DataConnector
from pglive.sources.live_plot import LiveLinePlot
from pglive.sources.live_plot_widget import LivePlotWidget

# Fake.
running = False

class MainWindow(QMainWindow):
    def __init__(self):
        global running
        running = True
        super().__init__()
        

        self.setWindowTitle("RocketGUI")
        layout = QVBoxLayout()

        # COM Selector
        com_selector = QComboBox()
        com_selector.addItems(["- select -"] + [f"COM{x}" for x in range(1, 11)])
        com_selector.setEditable(True)
        com_selector.setInsertPolicy(QComboBox.InsertPolicy.InsertAlphabetically)
        com_selector.currentTextChanged.connect(self.com_selector_changed)
        layout.addWidget(com_selector)

        # Live Plots
        self.live_plots = [
            LivePlot("Altitude", "ft"),
            LivePlot("Velocity", "ft"),
            LivePlot("Acceleration", "ft"),
            LivePlot("Langitude", "ft"),
        ]
        for plot in self.live_plots:
            layout.addWidget(plot)
        self.time = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plots)
        self.timer.start(10)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def com_selector_changed(self, text):
        # Connect to the selected COM port
        live.disconnect_serial()
        Thread(target=live.connect_serial, args=(text,)).start()

    def update_plots(self):
        if running:
            self.time += 0.01
            for plot in self.live_plots:
                plot.update_graph(self.time)

class LivePlot(LivePlotWidget):
    data_type = ""

    def __init__(self, data_ref, unit):
        super().__init__()

        global data_type
        data_type = data_ref

        self.setTitle(title=f"{data_ref} [{unit}]")
        self.live_plot_curve = LiveLinePlot()
        self.addItem(self.live_plot_curve)
        self.data_connector = DataConnector(self.live_plot_curve, max_points=60, update_rate=100)
        self.setBackground("#222222")

    def update_graph(self, time):
        x = 0
        data_point = randint(0, 100)
        if time != x and data_point != 0:
            x = time
            self.data_connector.cb_append_data_point(data_point, x)

        """while live.running:
            time = live.gps_data["Hour"] * 3600 + live.gps_data["Minute"] * 60 + live.gps_data["Seconds"] + live.gps_data["Milliseconds"] / 1000
            data_point = live.gps_data[data_type]
            if time != x and data_point != 0:
                x = time
                connector.cb_append_data_point(data_point, x)
            sleep(0.01)"""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
    running = False
    live.disconnect_serial()