import PyQt4.QtCore as qtc
import PyQt4.QtGui as qtg
import globalQueue
import queue
import sys
import random
import time

token = ["normal1.png", "normal2.png", "dur.png",
         "costaud.png", "fute.png", "rapide.png", "ko.png"]


queuePos = queue.Queue()
queueListen = queue.Queue()


def reverse(click):
    return (int((click[0] - 67) / 46.7), int(1 + -(click[1] - 478) / 47.2))


class listen(qtc.QThread):

    def __init__(self, parent=None):
        qtc.QThread.__init__(self, parent)

    def run(self):
        while True:
            instant = globalQueue.queue.get()
            self.emit(qtc.SIGNAL("update"), instant)


class depThread(qtc.QThread):

    def __init__(self, parent=None):
        qtc.QThread.__init__(self, parent)

    def run(self):
        while True:
            wait = globalQueue.waitInput.get()
            if wait:
                globalQueue.cond = True
                click = queuePos.get()
                pos1 = reverse(click)
                click = queuePos.get()
                globalQueue.cond = False
                pos2 = reverse(click)
                globalQueue.queueAction.put((pos1, pos2))


class buttonPos(qtg.QPushButton):

    def __init__(self, parent):
        super().__init__(parent)

    def mousePressEvent(self, QMouseEvent):
        if globalQueue.cond:
            x = QMouseEvent.x() + self.x()
            y = QMouseEvent.y() + self.y()
            queuePos.put((x, y))


class gui1(qtg.QWidget):

    def __init__(self, parent=None):
        self.app = qtg.QApplication([])
        super(gui1, self).__init__()
        self.resize(800, 600)
        self.buttonDeplace = qtg.QPushButton("Déplacer", self)
        self.buttonDeplace.resize(50, 25)
        self.buttonDeplace.move(20, 20)
        self.buttonFinTour = qtg.QPushButton("Fin du tour", self)
        self.buttonFinTour.resize(50, 25)
        self.buttonFinTour.move(85, 20)
        self.button = buttonPos(self)
        self.button.resize(700, 492)
        self.button.move(20, 90)
        self.button.setIcon(qtg.QIcon("./images/plateau.jpg"))
        self.button.setIconSize(qtc.QSize(700, 492))
        self.button.show()
        self.buttonEquipe1 = [None for j in range(6)]
        self.buttonEquipe2 = [None for j in range(6)]
        for i in range(6):
            self.buttonEquipe1[i] = buttonPos(self)
            self.buttonEquipe1[i].resize(46.7, 47.2)
            self.buttonEquipe1[i].move(67 + i * 46.7, 47.2)
            self.buttonEquipe1[i].setIcon(qtg.QIcon("./images/1_" + token[i]))
            self.buttonEquipe1[i].setIconSize(qtc.QSize(35, 35))
            self.buttonEquipe1[i].setStyleSheet(
                "background-color: transparent")
            self.buttonEquipe1[i].show()
            self.buttonEquipe2[i] = buttonPos(self)
            self.buttonEquipe2[i].resize(46.7, 47.2)
            self.buttonEquipe2[i].move(67 + (7 + i) * 46.7, 47.2)
            self.buttonEquipe2[i].setIcon(qtg.QIcon("./images/2_" + token[i]))
            self.buttonEquipe2[i].setIconSize(qtc.QSize(35, 35))
            self.buttonEquipe2[i].setStyleSheet(
                "background-color: transparent")
            self.buttonEquipe2[i].show()
        self.buttonBallon = buttonPos(self)
        self.buttonBallon.resize(46.7, 47.2)
        self.buttonBallon.move(67, 478)
        self.buttonBallon.setStyleSheet("background-color: transparent")
        self.buttonBallon.setIcon(qtg.QIcon("./images/ballon.png"))
        self.buttonBallon.setIconSize(qtc.QSize(25, 25))
        self.buttonBallon.show()
        self.show()
        self.thread = listen()
        self.depThread = depThread()
        self.connect(self.thread, qtc.SIGNAL("update"), self.update)
        self.buttonFinTour.clicked.connect(self.finTour)
        self.depThread.start()
        self.thread.start()
        sys.exit(self.app.exec_())

    def launchDep(self):
        self.depThread.start()

    def finTour(self):
        if globalQueue.waitOut:
            globalQueue.waitOut = False
            globalQueue.queueAction.put(["fin"])

    def update(self, value):
        for i in range(6):
            if value.equipe1.equipe[i].ko:
                self.buttonEquipe1[i].move(67 + (value.equipe1.equipe[i].pos[0]) * (46.7 - 10),
                                           478 - value.equipe1.equipe[i].pos[1] * (47.2 + 10))
                self.buttonEquipe1[i].setIcon(
                    qtg.QIcon("./images/1_" + token[6]))
                self.buttonEquipe1[i].setIconSize(qtc.QSize(25, 25))
                self.buttonEquipe1[i].show()

            else:
                self.buttonEquipe1[i].move(67 + (value.equipe1.equipe[i].pos[0]) * (46.7),
                                           478 - value.equipe1.equipe[i].pos[1] * (47.2))
                self.buttonEquipe1[i].setIcon(
                    qtg.QIcon("./images/1_" + token[i]))
                self.buttonEquipe1[i].setIconSize(qtc.QSize(35, 35))
                self.buttonEquipe1[i].show()

            if value.equipe2.equipe[i].ko:
                print(value.equipe2.equipe[i].pos[0]), value.equipe2.equipe[i].pos[1])
                self.buttonEquipe2[i].move(67 + (value.equipe2.equipe[i].pos[0]) * (46.7),
                                           478 - value.equipe2.equipe[i].pos[1] * (47.2))
                self.buttonEquipe2[i].setIcon(
                    qtg.QIcon("./images/2_" + token[6]))
                self.buttonEquipe2[i].setIconSize(qtc.QSize(25, 25))
                self.buttonEquipe2[i].show()

            else:
                self.buttonEquipe2[i].move(67 + (value.equipe2.equipe[i].pos[0]) * (46.7),
                                           478 - value.equipe2.equipe[i].pos[1] * (47.2))
                self.buttonEquipe2[i].setIcon(
                    qtg.QIcon("./images/2_" + token[i]))
                self.buttonEquipe2[i].setIconSize(qtc.QSize(35, 35))
                self.buttonEquipe2[i].show()

        (i, j) = value.ballon.position
        self.buttonBallon.move(67 + i * 46.7, 478 - j * 47.2)
        self.buttonBallon.show()
        self.show()
