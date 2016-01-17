import gui
import projet
import threading
import PyQt4.QtCore as qtc
import PyQt4.QtGui as qtg
import globalQueue
import sys
import random
import time


class guik(threading.Thread):

    def __init__(self):
        super().__init__()

    def run(self):
        gui.gui1()


class rules(threading.Thread):

    def __init__(self):
        super().__init__()

    def run(self):
        jeu = projet.jeu()
        jeu.equipe1.joue()
        print("Fin du jeu")

t1 = rules()
t2 = guik()
t1.start()
t2.start()
print(globalQueue.queue.qsize())
t1.join()
t2.join()
