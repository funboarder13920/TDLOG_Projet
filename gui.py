import PyQt4.QtCore as qtc
import PyQt4.QtGui as qtg
import globalQueue
import queue
import logging
import logging.config
import threading
import sys
import random
import time

prop = ["ordinaire", "ordinaire", "dur", "costaud", "futé", "rapide"]
token = ["normal1.png", "normal2.png", "dur.png",
         "costaud.png", "fute.png", "rapide.png", "ko.png"]


queuePos = queue.Queue()
queueListen = queue.Queue()
log = logging.getLogger("gui")
log.propagate = True


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
            print("depThread: reception de l'équipe qui attend une action")
            wait = globalQueue.waitInput.get()
            nEquipe = globalQueue.equipeJoue.get()
            print("depThread: équipe reçue")
            self.emit(qtc.SIGNAL("showEquipe"), nEquipe)
            if wait:
                globalQueue.cond = True
                click = queuePos.get()
                if click != (-1, -1):
                    pos1 = reverse(click)
                    self.emit(qtc.SIGNAL("showPlayerInfo"), pos1)
                    click = queuePos.get()
                    if click != (-1, -1):
                        globalQueue.cond = False
                        self.emit(qtc.SIGNAL("hidePlayerInfo"))
                        pos2 = reverse(click)
                        globalQueue.queueAction.put((pos1, pos2))


class choixThread(qtc.QThread):

    def __init__(self, gui):
        qtc.QThread.__init__(self, None)
        self.gui = gui

    def run(self):
        print("ChoixThread : enter")
        self.gui.equipeActu = 1
        while not(queuePos.empty()):
            queuePos.get()
        while not(self.gui.goChoix.empty()):
            self.gui.goChoix.get()
        self.blockSend = False
        self.gui.choixPos(1)
        while not(queuePos.empty()):
            queuePos.get()
        while not(self.gui.goChoix.empty()):
            self.gui.goChoix.get()
        self.gui.equipeActu = 2
        self.gui.choixPos(2)
        self.emit(qtc.SIGNAL("play"))
        self.blockSend = True


class buttonPos(qtg.QPushButton):

    def __init__(self, parent, nEquipe, nJoueur):
        super(buttonPos, self).__init__(parent)
        self.nEquipe = nEquipe
        self.nJoueur = nJoueur
        self.parent = parent

    def mousePressEvent(self, QMouseEvent):
        print("click bouton")
        if self.nEquipe == self.parent.equipeActu and self.nEquipe != 0:
            self.parent.send(self, self.nJoueur, self.nEquipe)
        if globalQueue.cond:
            x = QMouseEvent.x() + self.x()
            y = QMouseEvent.y() + self.y()
            if queuePos.empty():
                queuePos.put((x, y))


class gui1(qtg.QWidget):

    def __init__(self, parent=None):
        self.app = qtg.QApplication([])
        super(gui1, self).__init__()
        self.endChoix = False
        self.jeu = None
        self.playerInfo = qtg.QTextEdit(self)
        self.equipeInfo = qtg.QTextEdit(self)
        self.nEquipeTemp = -1
        self.nJoueurTemp = -1
        self.equipeActu = 0
        self.posTemp = (-1, -1)
        self.goChoix = queue.Queue()
        self.resize(800, 600)
        self.buttonFinTour = qtg.QPushButton("Fin du tour", self)
        self.button = buttonPos(self, 0, 0)
        self.blockSend = True
        self.buttonEquipe1 = [None for j in range(6)]
        self.buttonEquipe2 = [None for j in range(6)]
        for i in range(6):
            self.buttonEquipe1[i] = buttonPos(self, 1, i)
            self.buttonEquipe2[i] = buttonPos(self, 2, i)
        self.buttonBallon = buttonPos(self, 0, 0)
        self.thread = listen()
        self.interc = askInter()
        self.depThread = depThread()
        self.buttonChoix = qtg.QPushButton("Fin du choix", self)
        self.choix = choixThread(self)
        self.initAll()
        print("fin de l'initialisation")
        sys.exit(self.app.exec_())

    def initAll(self):
        self.buttonFinTour.resize(70, 25)
        self.buttonFinTour.move(85, 20)
        self.buttonFinTour.hide()
        self.button.resize(700, 492)
        self.button.move(20, 90)
        self.button.setIcon(qtg.QIcon("./images/plateau.jpg"))
        self.button.setIconSize(qtc.QSize(700, 492))
        self.button.show()
        self.playerInfo.setReadOnly(True)
        self.playerInfo.move(80, 60)
        self.playerInfo.setFontWeight(200)
        self.playerInfo.resize(400, 35)
        self.playerInfo.setStyleSheet(
            "QFrame {background: rgba(0,255,0,0%); border: rgba(0,255,0,0%)}")
        self.equipeInfo.setReadOnly(True)
        self.equipeInfo.move(400, 15)
        self.equipeInfo.setFontWeight(200)
        self.equipeInfo.setFontPointSize(20)
        self.equipeInfo.resize(400, 50)
        self.equipeInfo.setStyleSheet(
            "QFrame {background: rgba(0,255,0,0%); border: rgba(0,255,0,0%)}")
        self.equipeInfo.show()
        for i in range(6):
            self.buttonEquipe1[i].resize(46.7, 47.2)
            self.buttonEquipe1[i].move(67 + i * 46.7, 47.2)
            self.buttonEquipe1[i].setIcon(qtg.QIcon("./images/1_" + token[i]))
            self.buttonEquipe1[i].setIconSize(qtc.QSize(35, 35))
            self.buttonEquipe1[i].setStyleSheet(
                "background-color: transparent")
            self.buttonEquipe1[i].show()
            self.buttonEquipe2[i].resize(46.7, 47.2)
            self.buttonEquipe2[i].move(67 + (7 + i) * 46.7, 47.2)
            self.buttonEquipe2[i].setIcon(qtg.QIcon("./images/2_" + token[i]))
            self.buttonEquipe2[i].setIconSize(qtc.QSize(35, 35))
            self.buttonEquipe2[i].setStyleSheet(
                "background-color: transparent")
            self.buttonEquipe2[i].show()
        self.buttonBallon.resize(46.7, 47.2)
        self.buttonBallon.move(67, 478)
        self.buttonBallon.setStyleSheet("background-color: transparent")
        self.buttonBallon.setIcon(qtg.QIcon("./images/ballon.png"))
        self.buttonBallon.setIconSize(qtc.QSize(20, 20))
        self.buttonBallon.show()
        self.show()
        self.buttonChoix.resize(70, 25)
        self.buttonChoix.move(85, 20)
        self.buttonChoix.clicked.connect(self.endChoixTrue)
        self.buttonChoix.show()
        self.choix.start()
        self.connect(self.depThread, qtc.SIGNAL(
            "showPlayerInfo"), self.showPlayerInfo)
        self.connect(self.depThread, qtc.SIGNAL(
            "showEquipe"), self.showEquipe)
        self.connect(self.depThread, qtc.SIGNAL(
            "hidePlayerInfo"), self.hidePlayerInfo)
        self.connect(self.thread, qtc.SIGNAL("update"), self.update)
        self.connect(self.interc, qtc.SIGNAL(
            "interception"), self.askInterception)
        self.connect(self.choix, qtc.SIGNAL("play"), self.changeAffich)
        self.buttonFinTour.clicked.connect(self.finTour)
        self.depThread.start()
        self.thread.start()
        self.interc.start()
        print("initAll : fin de l'affichage")

    def showEquipe(self, nEquipe):
        print("showEquip: affiche équipe")
        if nEquipe == 1:
            self.equipeInfo.setTextColor(qtg.QColor("blue"))
            self.equipeInfo.setText("Equipe 1")
        else:
            self.equipeInfo.setTextColor(qtg.QColor("red"))
            self.equipeInfo.setText("Equipe 2")

    def showPlayerInfo(self, pos1):
        try:
            print("showPlayerInfo: Affiche les infos du joueur")
            if self.jeu.matrice[pos1[0]][pos1[1]][-1].nEquipe != 3:
                joueur = self.jeu.matrice[pos1[0]][pos1[1]][-1]
                self.playerInfo.setText("Le joueur {0} de l'équipe {1} a {2} déplacement(s) restant(s)".format(
                    prop[joueur.numero], joueur.nEquipe, joueur.depRestant))
                self.playerInfo.show()
        except:
            print("showPlayerInfo: Fail de l'affichage des infos du joueur")

    def hidePlayerInfo(self):
        self.playerInfo.hide()

    def changeAffich(self):
        self.buttonChoix.hide()
        self.buttonFinTour.show()

    def endChoixTrue(self):
        print("endChoixTrue: mettre fin au choix")
        self.endChoix = True
        if queuePos.empty():
            print("endChoixTrue: remplir queue.pos pour finir la thread")
            queuePos.put((-1, -1))
        if self.goChoix.empty():
            print("endChoixTrue: remplir goChoix pour sortir d'une thread")
            self.goChoix.put(True)

    def send(self, button, nJoueur, nEquipe):
        if not self.blockSend:
            print("Send: envoyer les infos du joueur sur lequel on vient de cliquer")
            self.nJoueurTemp = nJoueur
            self.nEquipeTemp = nEquipe
            self.posTemp = reverse((self.button.x(), self.button.y()))
            if self.goChoix.empty():
                print("Send: Maintenant il faut une position sur le plateau")
                self.goChoix.put(True)

    def choixPos(self, nEquipe):
        globalQueue.waitChoix.get()
        positions = [(-1, -1) for i in range(6)]
        k = 0
        print("ChoixPos: enter")
        while True:
            if self.nEquipeTemp == nEquipe and not(self.endChoix):
                if self.endChoix:
                    continue
                else:
                    print("choixPos: récupérer goChoix")
                    self.goChoix.get()
                    print("choixPos: goChoix a été correctement récupéré")
                stop = False
                while not queuePos.empty():
                    if queuePos.get()==(-1,-1):
                        stop = True
                    print("choixPos: vider queue.pos")
                if not(stop):
                    self.blockSend = True
                    globalQueue.cond = True
                    if self.endChoix:
                        continue
                    else:
                        click = queuePos.get()
                    globalQueue.cond = False
                    (posx, posy) = reverse(click)
                    if not(self.endChoix):
                        if (1 == self.nEquipeTemp):
                            if (posx >= 1 and posx <= 2 and posy >= 0 and posy < 8):
                                if not (posx, posy) in positions:
                                    if not self.endChoix:
                                        if positions[self.nJoueurTemp] == (-1, -1):
                                            k += 1
                                        positions[self.nJoueurTemp] = (posx, posy)
                                        self.buttonEquipe1[self.nJoueurTemp].move(
                                            67 + posx * 46.7, 478 - posy * 47.2)
                                else:
                                    print(
                                        "Veuillez réessayer : la position choisie est déjà occupée.")
                            else:
                                print(
                                    "Veuillez réessayer : la position choisie est hors limite. Il faut que 1=<x<=2 et 0<=y<=7")
                        else:
                            if (posx >= 10 and posx <= 11 and posy >= 0 and posy < 8):
                                if not (posx, posy) in positions:
                                    if not self.endChoix:
                                        if positions[self.nJoueurTemp] == (-1, -1):
                                            k += 1
                                        positions[self.nJoueurTemp] = (posx, posy)
                                        self.buttonEquipe2[self.nJoueurTemp].move(
                                            67 + posx * 46.7, 478 - posy * 47.2)

                                else:
                                    print(
                                        "Veuillez réessayer : la position choisie est déjà occupée.")
                            else:
                                print(
                                    "Veuillez réessayer : la position choisie est hors limite. Il faut que 1=<x<=2 et que 0<=y<=7")
                        self.blockSend = False
            else:
                self.blockSend = False
            if k == 6 and self.endChoix:
                globalQueue.sendPosition.put(positions)
                self.endChoix = False
                self.blockSend = False
                if self.equipeActu == 2:
                    self.blockSend = True
                break
            else:
                self.endChoix = False
                self.blockSend = False
            self.blockSend = False

    def askInterception(self, str):
        reply = qtg.QMessageBox.question(
            self, 'Message', str, qtg.QMessageBox.Yes, qtg.QMessageBox.No)
        if reply == qtg.QMessageBox.Yes:
            globalQueue.askInter.put(True)
        else:
            globalQueue.askInter.put(False)

    def finTour(self):
        if globalQueue.waitOut:
            while(not queuePos.empty()):
                queuePos.get()
            queuePos.put((-1, -1))
            globalQueue.waitOut = False
            globalQueue.queueAction.put(["fin"])

    def update(self, value):
        self.jeu = value
        for i in range(6):
            if value.equipe1.equipe[i].ko:
                self.buttonEquipe1[i].move(67 - 10 + (value.equipe1.equipe[i].pos[0]) * (46.7),
                                           478 + 10 - value.equipe1.equipe[i].pos[1] * (47.2))
                self.buttonEquipe1[i].setIcon(
                    qtg.QIcon("./images/1_" + token[6]))
                self.buttonEquipe1[i].setIconSize(qtc.QSize(25, 25))
                self.buttonEquipe1[i].show()
            if value.equipe2.equipe[i].ko:
                self.buttonEquipe2[i].move(67 - 10 + (value.equipe2.equipe[i].pos[0]) * (46.7),
                                           478 + 10 - value.equipe2.equipe[i].pos[1] * (47.2))
                self.buttonEquipe2[i].setIcon(
                    qtg.QIcon("./images/2_" + token[6]))
                self.buttonEquipe2[i].setIconSize(qtc.QSize(25, 25))
                self.buttonEquipe2[i].show()

        for i in range(6):
            if not value.equipe1.equipe[i].ko:
                self.buttonEquipe1[i].move(67 + (value.equipe1.equipe[i].pos[0]) * (46.7),
                                           478 - value.equipe1.equipe[i].pos[1] * (47.2))
                self.buttonEquipe1[i].setIcon(
                    qtg.QIcon("./images/1_" + token[i]))
                self.buttonEquipe1[i].setIconSize(qtc.QSize(35, 35))
                self.buttonEquipe1[i].show()

            if not value.equipe2.equipe[i].ko:
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
