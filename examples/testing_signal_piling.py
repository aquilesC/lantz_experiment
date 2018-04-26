from time import sleep
from PyQt5.QtCore import QObject, QTimer, QThread
from PyQt5.QtWidgets import QApplication


class Worker(QObject):
    def __init__(self):
        super().__init__()
        self.i = 0

    def run(self):
        sleep(2)
        print(self.i)
        self.i += 1
        return 1


class MainThread(QObject):
    def __init__(self):
        super().__init__()
        self.thread = QThread()
        self.thread.start()
        # self.thread.moveToThread(self.worker)
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.timer = QTimer()
        self.timer.timeout.connect(self.print_loop)
        self.timer.timeout.connect(self.worker.run)
        self.i = 0

    def run(self):
        self.timer.start(100)

    def print_loop(self):
        print('Main Thread: ', self.i)
        self.i += 1
        if self.i == 10:
            self.timer.stop()

app = QApplication([])

m = MainThread()
m.run()

app.exit(app.exec_())