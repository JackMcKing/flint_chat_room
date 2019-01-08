import json
import os
import time
import sys
import webbrowser

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWebEngineWidgets import QWebEngineView
from fbs_runtime.application_context import ApplicationContext
from PyQt5.QtWidgets import QMainWindow, QApplication
import requests as req
from configparser import ConfigParser

from src.main.python.MainWindowNCL import Ui_MainWindow

# TODO Replace this line with "from src.main.python.MainUI import Ui_MainWindow" before coding

SERVER_URL = ""
SERVER_PORT = ""
PROXY_URL = ""
PROXY_PORT = ""
USER_ID = ""
msgLen = 0


class AppContext(ApplicationContext):  # 1. Subclass ApplicationContext
    def run(self):  # 2. Implement run()
        window = MWindow()
        window.setWindowTitle("flint chat room")

        def online_work(num):
            window.label_7.clear()
            window.label_7.setText(num)

        online_thread = RefreshOnlineNumThread()
        online_thread._signal.connect(online_work)
        online_thread.start()

        def work(li):
            window.listWidget.clear()
            for item in li:
                window.listWidget.insertItem(window.listWidget.count(), str(item))
                global isNewMsg
                if isNewMsg is True:
                    window.listWidget.scrollToBottom()

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
                try:
                    if r.text.__contains__("Online"):
                        num = r.text.count(",") + 1
                        self._signal.emit(str(num))
                    else:
                        self._signal.emit("No Redis Service")
                except:
                    pass
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
                    self.trigger.emit(li)
                except:
                    pass

                time.sleep(1)


class MWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        super(QMainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # Config parser
        conf = Configer()
        # init setting line edit
        self.lineEdit_2.setText(conf.server_url)
        self.lineEdit_3.setText(conf.server_port)
        self.lineEdit_4.setText(conf.proxy_url)
        self.lineEdit_5.setText(conf.proxy_port)
        self.ID_LINEEDIT.setText(conf.user_id)

        # init global var
        global SERVER_URL
        global SERVER_PORT
        global PROXY_URL
        global PROXY_PORT
        global USER_ID
        SERVER_URL = conf.server_url
        SERVER_PORT = conf.server_port
        PROXY_URL = conf.proxy_url
        PROXY_PORT = conf.proxy_port
        USER_ID = conf.user_id

        self.actionGitHub.triggered.connect(self.goto_github)
        self.actionTrello.triggered.connect(self.goto_trello)
        self.pushButton.pressed.connect(self.push_btn)
        self.UPDATE_ID_BTN.pressed.connect(self.push_update_id_btn)
        self.pushButton_2.pressed.connect(self.push_connect_btn)

        self.show()

    def goto_github(self):
        webbrowser.open_new("https://github.com/JackMcKing/flint_chat_room")

    def goto_trello(self):
        webbrowser.open_new("https://trello.com/b/YH3RcfOA/flint-chat-room")

    def push_update_id_btn(self):
        conf = Configer()
        old_id = conf.user_id
        new_id = self.ID_LINEEDIT.text()
        send_to_server("flint bot", str(time.time()), "User "+old_id+" have changed id as "+new_id)
        global USER_ID
        USER_ID = new_id
        conf.setConfig("USER", "id", new_id)

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
            conf.setConfig("SERVER", "url", server_url)
            conf.setConfig("SERVER", "url", server_url)
            conf.setConfig("SERVER", "url", server_url)
            conf.setConfig("SERVER", "url", server_url)
        else:
            self.label_5.setText("connect failed")

    def push_btn(self):
        msg_lineedit = self.lineEdit.text()
        isJustNoneLetterflag = True
        for i in msg_lineedit:
            if i is not " ":
                isJustNoneLetterflag = False
        if msg_lineedit is "":
            return
        elif isJustNoneLetterflag is True:
            return
        else:
            r = send_to_server(USER_ID, str(time.time()), msg_lineedit)
            if r is False:
                self.STATUS_LABEL.setText("发送失败（没有填写用户ID或网络连接丢失）")
            else:
                self.STATUS_LABEL.clear()
                self.lineEdit.clear()
                self.listWidget.insertItem(self.listWidget.count(), "(Sending...)"+msg_lineedit)

            self.listWidget.scrollToBottom()


def send_to_server(id, timestamp, text):
    data_template = {"ID": id, "TIMESTAMP": timestamp, "TEXT": text}
    send_data = json.dumps(data_template)

    if id is "":
        return False

    if SERVER_URL is "" or SERVER_PORT is "":
        pass
    else:
        if PROXY_URL is "" or PROXY_PORT is "":
            try:
                r = req.post(SERVER_URL + ":" + SERVER_PORT + "/put_history", json=send_data)
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
        for msg in list(r):
            msg = dict(msg)
            ID = (msg.get('ID'))
            TIMESTAMP = (msg.get('TIMESTAMP'))
            TEXT = (msg.get('TEXT'))
            ret.append(str(ID + " [" + TIMESTAMP + "]" + " : " + TEXT))
        # for i in range(len(r)):
        #     add_text = r[str(i)]
        #     str(add_text).encode("utf-8")
        #     add_text = add_text[:-1]  # 去掉\n
        #     ret.append(add_text)
        return list(ret)


class Configer:

    def __init__(self):
        self.PATH = os.getcwd().replace("\\", "/") + "/config.ini"
        # self.PATH = "./config.ini"

        if not self.checkIsConfigExist():
            f = open(self.PATH, "w", newline="")
            templete = "[SERVER]\n" \
                       "url=\n" \
                       "port=\n" \
                       "\n" \
                       "[PROXY]\n" \
                       "url=\n" \
                       "port=\n" \
                       "\n" \
                       "[USER]\n" \
                       "id=\n"
            f.write(templete)
            f.close()

        conf = ConfigParser()
        conf.read(self.PATH)
        self.server_url = conf.get("SERVER", "url")
        self.server_port = conf.get("SERVER", "port")
        self.proxy_url = conf.get("PROXY", "url")
        self.proxy_port = conf.get("PROXY", "port")
        self.user_id = conf.get("USER", "id")

    def checkIsConfigExist(self):
        cur_path_files = os.listdir(os.getcwd().replace("\\", "/"))
        for file in cur_path_files:
            if os.path.isfile(file):
                if file == "config.ini":
                    return True
        return False

    # def getConfig(self):
    #     cfg = ConfigParser()
    #     cfg.read(self.PATH)
    #     global SERVER_URL
    #     global SERVER_PORT
    #     global PROXY_URL
    #     global PROXY_PORT
    #     SERVER_URL = cfg.get("SERVER", "url")
    #     SERVER_PORT = cfg.get("SERVER", "port")
    #     PROXY_URL = cfg.get("PROXY", "url")
    #     PROXY_PORT = cfg.get("PROXY", "port")
    #     return cfg.get("SERVER", "url"), cfg.get("SERVER", "port"), cfg.get("PROXY", "url"), cfg.get("PROXY", "port"), cfg.get("USER", "id")

    def setConfig(self, section, option, value):
        cfg = ConfigParser()
        cfg.read(self.PATH)
        cfg.set(section, option, value)
        # cfg.set("SERVER", "url", self.server_url)
        # cfg.set("SERVER", "port", self.server_port)
        # cfg.set("PROXY", "url", self.proxy_url)
        # cfg.set("PROXY", "port", self.proxy_port)
        f = open(self.PATH, 'w')
        cfg.write(f)


if __name__ == '__main__':
    app = QApplication([])
    app.setStyle('Fusion')

    appctxt = AppContext()  # 4. Instantiate the subclass
    exit_code = appctxt.run()  # 5. Invoke run()
    sys.exit(exit_code)
