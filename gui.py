import PyQt4.QtCore as qtc
import PyQt4.QtGui as qtg
import globalQueue
import queue
import threading
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


class askInter(qtc.QThread):

    def __init__(self, parent=None):
        qtc.QThread.__init__(self, parent)

    def run(self):
        while True:
            adv = globalQueue.interAdv.get()
            self.emit(qtc.SIGNAL("interception"),
                      "Voulez vous essayer d'intercepter la passe avec le joueur " + str(adv.numero) + " ?")


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


class choixThread(threading.Thread):

    def __init__(self, gui, nb):
        super().__init__()
        self.nb = nb
        self.gui = gui

    def run(self):
        self.gui.choixPos(self.nb)
        if self.nb == 2:
            self.gui.buttonChoix.hide()


class buttonPos(qtg.QPushButton):

    def __init__(self, parent, nEquipe, nJoueur):
        super(buttonPos,self).__init__(parent)
        if nEquipe != 0:
            print("ki")
            self.clicked.connect(self.printoui)
                #lambda x: parent.send(x, self, nEquipe, nJoueur))
    
    def printoui(self):
        print("oui")

    def mousePressEvent(self, QMouseEvent):
        if globalQueue.cond:
            x = QMouseEvent.x() + self.x()
            y = QMouseEvent.y() + self.y()
            queuePos.put((x, y))


class gui1(qtg.QWidget):

    def __init__(self, parent=None):
        self.app = qtg.QApplication([])
        super(gui1, self).__init__()
        self.endChoix = False
        self.nEquipeTemp = -1
        self.nJoueurTemp = -1
        self.posTemp = (-1, -1)
        self.goChoix = queue.Queue()
        self.resize(800, 600)
        self.buttonFinTour = qtg.QPushButton("Fin du tour", self)
        self.buttonFinTour.resize(70, 25)
        self.buttonFinTour.move(85, 20)
        self.button = buttonPos(self, 0, 0)
        self.button.resize(700, 492)
        self.blockSend = False
        self.button.move(20, 90)
        self.button.setIcon(qtg.QIcon("./images/plateau.jpg"))
        self.button.setIconSize(qtc.QSize(700, 492))
        self.button.show()
        self.buttonEquipe1 = [None for j in range(6)]
        self.buttonEquipe2 = [None for j in range(6)]
        for i in range(6):
            self.buttonEquipe1[i] = buttonPos(self, 1, i)
            self.buttonEquipe1[i].resize(46.7, 47.2)
            self.buttonEquipe1[i].move(67 + i * 46.7, 47.2)
            self.buttonEquipe1[i].setIcon(qtg.QIcon("./images/1_" + token[i]))
            self.buttonEquipe1[i].setIconSize(qtc.QSize(35, 35))
            self.buttonEquipe1[i].setStyleSheet(
                "background-color: transparent")
            self.buttonEquipe1[i].show()
            self.buttonEquipe2[i] = buttonPos(self, 2, i)
            self.buttonEquipe2[i].resize(46.7, 47.2)
            self.buttonEquipe2[i].move(67 + (7 + i) * 46.7, 47.2)
            self.buttonEquipe2[i].setIcon(qtg.QIcon("./images/2_" + token[i]))
            self.buttonEquipe2[i].setIconSize(qtc.QSize(35, 35))
            self.buttonEquipe2[i].setStyleSheet(
                "background-color: transparent")
            self.buttonEquipe2[i].show()
        self.buttonBallon = buttonPos(self, 0, 0)
        self.buttonBallon.resize(46.7, 47.2)
        self.buttonBallon.move(67, 478)
        self.buttonBallon.setStyleSheet("background-color: transparent")
        self.buttonBallon.setIcon(qtg.QIcon("./images/ballon.png"))
        self.buttonBallon.setIconSize(qtc.QSize(20, 20))
        self.buttonBallon.show()
        self.show()
        self.thread = listen()
        self.interc = askInter()
        self.depThread = depThread()
        self.buttonChoix = qtg.QPushButton("Fin du choix", self)
        self.buttonChoix.resize(70, 20)
        self.buttonChoix.move(160, 20)
        self.buttonChoix.clicked.connect(self.endChoixTrue)
        self.buttonChoix.show()
        choix1 = choixThread(self, 1)
        # choix1.start()
        choix2 = choixThread(self, 2)
        # choix2.start()
        self.connect(self.thread, qtc.SIGNAL("update"), self.update)
        self.connect(self.interc, qtc.SIGNAL(
            "interception"), self.askInterception)
        self.buttonFinTour.clicked.connect(self.finTour)
        self.depThread.start()
        self.thread.start()
        self.interc.start()
        sys.exit(self.app.exec_())

    def printoui(self):
        print("oui")

    def endChoixTrue(self):
        self.endChoix = True

    def send(self, button, nJoueur, nEquipe):
        if not self.blockSend:
            self.nJoueurTemp = nJoueur
            self.nEquipeTemp = nEquipe
            self.posTemp = reverse((self.button.x(), self.button.y()))
            self.goChoix.put(True)

    def choixPos(self, nEquipe):
        print("in")
        globalQueue.waitChoix.get()
        print("in1")
        positions = [(-1, -1) for i in range(6)]
        k = 0
        while True:
            if self.nEquipeTemp == nEquipe:
                self.goChoix.get()
                self.blockSend = True
                click = queuePos.get()
                (posx, posy) = reverse(click)
                if (1 == nEquipe):
                    if (posx >= 1 and posx <= 2 and posy >= 0 and posy < 8):
                        if not (posx, posy) in positions:
                            if positions[self.nJoueurTemp] == (-1, -1):
                                k += 1
                            positions[self.nJoueurTemp] = (posx, posy)
                            log.debug(
                                "Append de ({0},{1})".format(posx, posy))
                        else:
                            print(
                                "Veuillez réessayer : la position choisie est déjà occupée.")
                            log.warning(
                                "Position ({0},{1}) déjà occupée".format(posx, posy))
                    else:
                        print(
                            "Veuillez réessayer : la position choisie est hors limite. Il faut que 1=<x<=2 et 0<=y<=7")
                        log.warning(
                            "({0},{1}) est hors limite".format(posx, posy))
                else:
                    if (posx >= 10 and posx <= 11 and posy >= 0 and posy < 8):
                        if not (posx, posy) in positions:
                            if positions[self.nJoueurTemp] == (-1, -1):
                                k += 1
                            positions[self.nJoueurTemp] = (posx, posy)
                            log.info(
                                "Append de ({0},{1})".format(posx, posy))
                        else:
                            print(
                                "Veuillez réessayer : la position choisie est déjà occupée.")
                            log.warning(
                                "Position ({0},{1}) déjà occupée".format(posx, posy))
                    else:
                        print(
                            "Veuillez réessayer : la position choisie est hors limite. Il faut que 1=<x<=2 et que 0<=y<=7")
                        log.warning(
                            "({0},{1}) est hors limite".format(posx, posy))
                self.blockSend = False
                if k == 6 and self.endChoix:
                    globalQueue.sendPosition.put(positions)
                    self.endChoix = False
                    break
                else:
                    self.endChoix = False

    def askInterception(self, str):
        reply = qtg.QMessageBox.question(
            self, 'Message', str, qtg.QMessageBox.Yes, qtg.QMessageBox.No)
        if reply == qtg.QMessageBox.Yes:
            globalQueue.askInter.put(True)
        else:
            globalQueue.askInter.put(False)

    def finTour(self):
        if globalQueue.waitOut:
            globalQueue.waitOut = False
            globalQueue.queueAction.put(["fin"])

    def update(self, value):
        for i in range(6):
            if value.equipe1.equipe[i].ko:
                self.buttonEquipe1[i].move(67 - 10 + (value.equipe1.equipe[i].pos[0]) * (46.7),
                                           478 + 10 - value.equipe1.equipe[i].pos[1] * (47.2))
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
                print(value.equipe2.equipe[i].pos[0],
                      value.equipe2.equipe[i].pos[1])
                self.buttonEquipe2[i].move(67 - 10 + (value.equipe2.equipe[i].pos[0]) * (46.7),
                                           478 + 10 - value.equipe2.equipe[i].pos[1] * (47.2))
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
        self.buttonBallon.move(67 + 10 + i * 46.7, 478 - 10 - j * 47.2)
        self.buttonBallon.show()
        self.show()
