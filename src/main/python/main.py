import json
import os
import time
import sys

from PyQt5.QtCore import QThread, pyqtSignal
from fbs_runtime.application_context import ApplicationContext
from PyQt5.QtWidgets import QMainWindow, QApplication
import requests as req
from configparser import ConfigParser

from MainUI import Ui_MainWindow

# TODO Replace this line with "from src.main.python.MainUI import Ui_MainWindow" before coding

SERVER_URL = ""
SERVER_PORT = ""
PROXY_URL = ""
PROXY_PORT = ""
msgLen = 0


class AppContext(ApplicationContext):  # 1. Subclass ApplicationContext
    def run(self):  # 2. Implement run()
        window = Dlog()
        window.setWindowTitle("flint chat room")

        def online_work(num):
            online_lable.clear()
            online_lable.setText(num)

        online_thread = RefreshOnlineNumThread()
        online_thread._signal.connect(online_work)
        online_thread.start()

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


class RefreshOnlineNumThread(QThread):
    _signal = pyqtSignal(str)

    def __int__(self):
        super(RefreshOnlineNumThread, self).__init__()

    def run(self):
        while True:
            if SERVER_URL is "" or SERVER_PORT is "":
                pass
            else:
                if PROXY_URL is "" or PROXY_PORT is "":
                    try:
                        r = req.get(SERVER_URL + ":" + SERVER_PORT + "/online")
                    except:
                        pass
                else:
                    proxies = {
                        "http": PROXY_URL + ":" + PROXY_PORT
                    }
                    try:
                        r = req.get(SERVER_URL + ":" + SERVER_PORT + "/online", proxies=proxies)
                    except:
                        pass
                if r.text.__contains__("Online"):
                    num = r.text.count(",") + 1
                    self._signal.emit(str(num))
                time.sleep(5)


class RefreshThread(QThread):
    trigger = pyqtSignal(list)

    def __int__(self):
        super(RefreshThread, self).__init__()

    def run(self):
        while True:
            url = SERVER_URL
            if url.__contains__("http"):
                try:
                    li = refresh_list()
                except:
                    pass
                self.trigger.emit(li)
                time.sleep(1)


class Dlog(QMainWindow, Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        super(QMainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # Config parser
        conf = Configer()
        conf_li = conf.getConfig()
        self.lineEdit_2.setText(conf_li[0])
        self.lineEdit_3.setText(conf_li[1])
        self.lineEdit_4.setText(conf_li[2])
        self.lineEdit_5.setText(conf_li[3])

        global lw
        lw = self.listWidget
        global online_lable
        online_lable = self.label_7
        self.pushButton.pressed.connect(self.puch_btn)

        self.pushButton_2.pressed.connect(self.push_connect_btn)

        self.show()

    def push_connect_btn(self):
        self.label_5.setText("connecting...")

        server_url = self.lineEdit_2.text()
        server_port = self.lineEdit_3.text()
        proxy_url = self.lineEdit_4.text()
        proxy_port = self.lineEdit_5.text()

        if str(proxy_url) is "" or str(proxy_port) is "":
            try:
                r = req.get(server_url + ":" + server_port + "/test_connect")
            except:
                self.label_5.setText("connect failed")
        else:
            proxies = {
                "http": proxy_url + ":" + proxy_port
            }
            try:
                r = req.get(server_url + ":" + server_port + "/test_connect", proxies=proxies)
            except:
                self.label_5.setText("connect failed")

        if str(r.text).__contains__("success"):
            self.label_5.setText("connect success")
            self.listWidget.clear()
            global SERVER_URL
            global SERVER_PORT
            global PROXY_URL
            global PROXY_PORT
            SERVER_URL = server_url
            SERVER_PORT = server_port
            PROXY_URL = proxy_url
            PROXY_PORT = proxy_port
            conf = Configer()
            conf.setConfig()
        else:
            self.label_5.setText("connect failed")

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
            else:
                self.lineEdit.clear()
                self.listWidget.insertItem(self.listWidget.count(), str)

            self.listWidget.scrollToBottom()


def send_to_server(text):
    j_data = '{"0":"' + text + '"}'
    send_data = json.loads(j_data)

    if SERVER_URL is "" or SERVER_PORT is "":
        pass
    else:
        if PROXY_URL is "" or PROXY_PORT is "":
            try:
                r = req.get(SERVER_URL + ":" + SERVER_PORT + "/put_history", json=send_data)
            except:
                return False
        else:
            proxies = {
                "http": PROXY_URL + ":" + PROXY_PORT
            }
            try:
                r = req.post(SERVER_URL + ":" + SERVER_PORT + "/put_history", proxies=proxies, json=send_data)
            except:
                return False
        if r.text.__contains__("success"):
            return True
        else:
            return False


def refresh_list():
    global msgLen
    global isNewMsg

    if SERVER_URL is "" or SERVER_PORT is "":
        pass
    else:
        if PROXY_URL is "" or PROXY_PORT is "":
            r = req.get(SERVER_URL + ":" + SERVER_PORT + "/get_history")
        else:
            proxies = {
                "http": PROXY_URL + ":" + PROXY_PORT
            }
            r = req.get(SERVER_URL + ":" + SERVER_PORT + "/get_history", proxies=proxies)
        r = json.loads(str(r.text))
        ret = []
        isNewMsg = False if msgLen is len(r) else True
        msgLen = len(r)
        for i in range(len(r)):
            add_text = r[str(i)]
            str(add_text).encode("utf-8")
            add_text = add_text[:-1]  # 去掉\n
            ret.append(add_text)
        return ret


class Configer:

    def __init__(self):
        self.server_url = SERVER_URL
        self.server_port = SERVER_PORT
        self.proxy_url = PROXY_URL
        self.proxy_port = PROXY_PORT

        if not self.checkIsConfigExist():
            f = open(os.getcwd().replace("\\", "/") + "/config.ini", "w", newline="")
            templete = "[SERVER]\n" \
                       "url=\n" \
                       "port=\n" \
                       "\n" \
                       "[PROXY]\n" \
                       "url=\n" \
                       "port=\n"
            f.write(templete)
            f.close()
        self.PATH = os.getcwd().replace("\\", "/") + "/config.ini"

    def checkIsConfigExist(self):
        cur_path_files = os.listdir(os.getcwd().replace("\\", "/"))
        for file in cur_path_files:
            if os.path.isfile(file):
                if file == "config.ini":
                    return True
        return False

    def getConfig(self):
        cfg = ConfigParser()
        cfg.read(self.PATH)
        global SERVER_URL
        global SERVER_PORT
        global PROXY_URL
        global PROXY_PORT
        SERVER_URL = cfg.get("SERVER", "url")
        SERVER_PORT = cfg.get("SERVER", "port")
        PROXY_URL = cfg.get("PROXY", "url")
        PROXY_PORT = cfg.get("PROXY", "port")
        return cfg.get("SERVER", "url"), cfg.get("SERVER", "port"), cfg.get("PROXY", "url"), cfg.get("PROXY", "port")

    def setConfig(self):
        cfg = ConfigParser()
        cfg.read(self.PATH)
        cfg.set("SERVER", "url", self.server_url)
        cfg.set("SERVER", "port", self.server_port)
        cfg.set("PROXY", "url", self.proxy_url)
        cfg.set("PROXY", "port", self.proxy_port)
        f = open(self.PATH, 'w')
        cfg.write(f)


if __name__ == '__main__':
    app = QApplication([])
    app.setStyle('Fusion')

    appctxt = AppContext()  # 4. Instantiate the subclass
    exit_code = appctxt.run()  # 5. Invoke run()
    sys.exit(exit_code)
