import sys
import numpy as np
import cv2
import live
from math import sin
from threading import Thread
from time import sleep
from random import randint
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QComboBox, QTextEdit, QLabel, QSlider
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import QUrl, Qt, Slot, QTimer
from PySide6.QtQuickWidgets import QQuickWidget
from pyqtgraph import PlotWidget
from pglive.sources.data_connector import DataConnector
from pglive.sources.live_plot import LiveLinePlot
from pglive.sources.live_plot_widget import LivePlotWidget
from camera_thread import CameraThread
from rotation_handler import RotationHandler
from preferences import rtsp_url

# Global variables
running = True

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Liberty Rocketry Ground Station")
        self.setGeometry(10, 10, 1280, 720)

        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)

        # Controls frame
        controls_widget = QWidget()
        controls_layout = QVBoxLayout(controls_widget)

        # COM Selector
        com_selector = QComboBox()
        com_selector.addItems(["- select -"] + [f"COM{x}" for x in range(1, 11)])
        com_selector.setEditable(True)
        com_selector.setInsertPolicy(QComboBox.InsertPolicy.InsertAlphabetically)
        com_selector.currentTextChanged.connect(self.com_selector_changed)
        controls_layout.addWidget(com_selector)

        # Buttons
        buttons = ["Toggle cameras", "Start/stop flight", "Export flight", "View flights", "MISC 1"]
        for btn_text in buttons:
            button = QPushButton(btn_text)
            button.clicked.connect(lambda checked, text=btn_text: self.button_pressed(text))
            controls_layout.addWidget(button)

        # Console output
        self.console_output = QTextEdit()
        self.console_output.setReadOnly(True)
        controls_layout.addWidget(self.console_output)

        main_layout.addWidget(controls_widget)

        # Graph frame
        graph_widget = QWidget()
        graph_layout = QVBoxLayout(graph_widget)

        pyqtgraph_plot = PlotWidget()
        pyqtgraph_plot.plot(np.random.normal(size=100))
        pyqtgraph_plot.setBackground("#222222")
        graph_layout.addWidget(pyqtgraph_plot)

        # Live Plots
        self.live_plots = [
            LivePlot("Altitude", "ft"),
            LivePlot("Velocity", "ft"),
            LivePlot("Acceleration", "ft"),
            LivePlot("Langitude", "ft")
        ]
        for plot in self.live_plots:
            graph_layout.addWidget(plot)
        self.time = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plots)
        self.timer.start(10)

        main_layout.addWidget(graph_widget)

        # QQuickWidget for 3D view
        self.quick_widget = QQuickWidget()
        self.quick_widget.setSource(QUrl('main.qml'))
        self.quick_widget.setResizeMode(QQuickWidget.SizeRootObjectToView)
        main_layout.addWidget(self.quick_widget)

        # Viewport for cameras
        self.viewport_widget = QLabel()
        self.viewport_widget.setFixedSize(640, 480)  # Set a fixed size for the viewport
        self.viewport_widget.hide()  # Initially hidden
        graph_layout.addWidget(self.viewport_widget)

        # Rotation controls
        self.rotation_controls = QWidget()
        rotation_layout = QVBoxLayout(self.rotation_controls)
        
        self.sliderX = QSlider(Qt.Horizontal)
        self.sliderX.setRange(0, 360)
        self.sliderX.valueChanged.connect(self.update_rotationX)
        rotation_layout.addWidget(self.sliderX)

        self.sliderY = QSlider(Qt.Horizontal)
        self.sliderY.setRange(0, 360)
        self.sliderY.valueChanged.connect(self.update_rotationY)
        rotation_layout.addWidget(self.sliderY)

        self.sliderZ = QSlider(Qt.Horizontal)
        self.sliderZ.setRange(0, 360)
        self.sliderZ.valueChanged.connect(self.update_rotationZ)
        rotation_layout.addWidget(self.sliderZ)

        graph_layout.addWidget(self.rotation_controls)

        self.setCentralWidget(main_widget)

        # Setup camera
        self.camera_thread = CameraThread()
        self.camera_thread.frame_ready.connect(self.update_camera)

        # Setup rotation handler
        self.rotation_handler = RotationHandler()
        context = self.quick_widget.rootContext()
        context.setContextProperty("rotationHandler", self.rotation_handler)

    def com_selector_changed(self, text):
        # Connect to the selected COM port
        live.disconnect_serial()
        Thread(target=live.connect_serial, args=(text,)).start()

    def button_pressed(self, text):
        self.console_output.append(f"'{text}' pressed")
        if text == "Toggle cameras":
            self.toggle_viewport()

    def toggle_viewport(self):
        if self.viewport_widget.isVisible():
            self.viewport_widget.hide()
            self.camera_thread.stop_camera()
        else:
            self.viewport_widget.show()
            self.camera_thread.start_camera(rtsp_url)

    def update_plots(self):
        if running:
            self.time += 1
            for plot in self.live_plots:
                plot.update_graph(self.time)

    @Slot(np.ndarray)
    def update_camera(self, frame):
        # Convert the frame to QImage
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame.shape
        bytes_per_line = ch * w
        qimg = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        # Display the image in the QLabel
        self.viewport_widget.setPixmap(QPixmap.fromImage(qimg))

    @Slot(int)
    def update_rotationX(self, value):
        self.rotation_handler.rotationX = value

    @Slot(int)
    def update_rotationY(self, value):
        self.rotation_handler.rotationY = value

    @Slot(int)
    def update_rotationZ(self, value):
        self.rotation_handler.rotationZ = value

class LivePlot(LivePlotWidget):
    data_type = ""
    prev_time = 0

    def __init__(self, data_ref, unit):
        super().__init__()

        global data_type
        data_type = data_ref

        self.setTitle(title=f"{data_ref} [{unit}]")
        self.live_plot_curve = LiveLinePlot()
        self.addItem(self.live_plot_curve)
        self.data_connector = DataConnector(self.live_plot_curve, max_points=60, update_rate=1)
        self.setBackground("#222222")

    def update_graph(self, time):
        data_point = randint(0, 100)
        if time != self.prev_time and data_point != 0:
            self.prev_time = time
            self.data_connector.cb_append_data_point(data_point, self.prev_time)

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