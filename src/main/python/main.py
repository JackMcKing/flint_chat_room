import json
import time

from PyQt5.QtCore import QThread, pyqtSignal
from fbs_runtime.application_context import ApplicationContext
from PyQt5.QtWidgets import QMainWindow, QApplication
import requests as req

import sys

from ChatRoomUI import Ui_MainWindow

SERVER_URL = "http://127.0.0.1"
SERVER_PORT = "5000"
msgLen = 0


class AppContext(ApplicationContext):  # 1. Subclass ApplicationContext
    def run(self):  # 2. Implement run()
        window = Dlog()
        window.setWindowTitle("flint chat room")

        def work(li):
            lw.clear()
            for item in li:
                lw.insertItem(lw.count(), str(item))
                global isNewMsg
                if isNewMsg is True:
                    lw.scrollToBottom()

        thread = RefreshThread()
        thread.trigger.connect(work)
        thread.start()
        return self.app.exec_()  # 3. End run() with this line


class RefreshThread(QThread):
    trigger = pyqtSignal(list)

    def __int__(self):
        super(RefreshThread, self).__init__()

    def run(self):
        while True:
            li = refresh_list()
            self.trigger.emit(li)
            time.sleep(1)


class Dlog(QMainWindow, Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        super(QMainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        global lw
        lw = self.listWidget
        self.pushButton.pressed.connect(self.puch_btn)

        self.show()

    def puch_btn(self):
        str = self.lineEdit.text()
        isJustNoneLetterflag = True
        for i in str:
            if i is not " ":
                isJustNoneLetterflag = False
        if str is "":
            return
        elif isJustNoneLetterflag is True:
            return
        else:
            r = send_to_server(str)
            if r is False:
                self.listWidget.insertItem(self.listWidget.count(), "(系统错误)")
            self.lineEdit.clear()
            self.listWidget.insertItem(self.listWidget.count(), str)
            self.listWidget.scrollToBottom()


def send_to_server(text):
    j_data = '{"0":"' + text + '"}'
    send_data = json.loads(j_data)
    r = req.post(SERVER_URL + ":" + SERVER_PORT + "/put_history", json=send_data)
    if r.text.__contains__("success"):
        return True
    else:
        return False


def refresh_list():
    global msgLen
    global isNewMsg
    r = req.get(SERVER_URL + ":" + SERVER_PORT + "/get_history")
    r = json.loads(str(r.text))
    ret = []
    isNewMsg = False if msgLen is len(r) else True
    msgLen = len(r)
    for i in range(len(r)):
        add_text = r[str(i)]
        str(add_text).encode("utf-8")
        add_text = add_text[:-1]  # 去掉\n
        ret.append(add_text)
        # self.listWidget.insertItem(self.listWidget.count(), add_text)
    return ret


if __name__ == '__main__':
    app = QApplication([])
    app.setStyle('Fusion')

    appctxt = AppContext()  # 4. Instantiate the subclass
    exit_code = appctxt.run()  # 5. Invoke run()
    sys.exit(exit_code)
