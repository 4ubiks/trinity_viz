from PySide6.QtCore import QRunnable, QThreadPool, QTimer, Slot, Signal, QObject
from PySide6.QtWidgets import QApplication, QPushButton, QLabel, QVBoxLayout, QWidget
import time

class Worker(QRunnable):
    """ A QRunnable-based worker that runs a task in a separate thread. """

    def __init__(self, task_id, callback):
        super().__init__()
        self.task_id = task_id
        self.callback = callback

    def run(self):
        """ Simulate a long-running task. """
        time.sleep(2)  # Simulate delay
        self.callback(self.task_id, "Completed!")  # Call callback when done

class ExampleApp(QWidget):
    """ Main GUI application that manages tasks using QThreadPool. """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("QThreadPool Example")
        self.layout = QVBoxLayout()
        self.label = QLabel("Press the button to start a task.")
        self.button = QPushButton("Start Task")
        self.button.clicked.connect(self.start_task)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)
        self.threadpool = QThreadPool.globalInstance()  # Get the thread pool

    def start_task(self):
        """ Create and start a worker in the thread pool. """
        task_id = "Task-1"
        worker = Worker(task_id, self.task_finished)
        self.threadpool.start(worker)
        self.label.setText(f"Running {task_id}...")

    def task_finished(self, task_id, message):
        """ Update the UI when a task is complete. """
        self.label.setText(f"{task_id}: {message}")

if __name__ == "__main__":
    app = QApplication([])
    window = ExampleApp()
    window.show()
    app.exec()