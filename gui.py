import PyQt4.QtCore as qtc
import PyQt4.QtGui as qtg
import globalQueue
import sys
import random
import time

token = ["normal1.png","normal2.png","dur.png","costaud.png","fute.png","rapide.png","ko.png"]

class listen(qtc.QThread):
	def __init__(self,parent=None):
		qtc.QThread.__init__(self,parent)

	def run(self):
		while True:
			print(globalQueue.queue.qsize())
			instant = globalQueue.queue.get()
			self.emit(qtc.SIGNAL("update"),instant)

class gui1(qtg.QWidget):
	def __init__(self, parent =None):
		self.app = qtg.QApplication([])
		self.window = qtg.QWidget()
		self.window.resize(800, 600)
		self.button = qtg.QPushButton(self.window)
		self.button.resize(700, 492)
		self.button.move(20, 90)
		self.button.setIcon(qtg.QIcon("./images/plateau.jpg"))
		self.button.setIconSize(qtc.QSize(700,492))
		self.button.show()
		self.buttonEquipe1=[None for j in range(6)]
		self.buttonEquipe2 = [None for j in range(6)]
		for i in range(6):
				self.buttonEquipe1[i]=qtg.QPushButton(self.window)
				self.buttonEquipe1[i].resize(46.7,47.2)
				self.buttonEquipe1[i].move(67+i*46.7,47.2)
				self.buttonEquipe1[i].setIcon(qtg.QIcon("./images/1_"+ token[i]))
				self.buttonEquipe1[i].setIconSize(qtc.QSize(35,35))
				self.buttonEquipe1[i].setStyleSheet("background-color: transparent")			
				self.buttonEquipe1[i].show()
				self.buttonEquipe2[i]=qtg.QPushButton(self.window)
				self.buttonEquipe2[i].resize(46.7,47.2)
				self.buttonEquipe2[i].move(67+(7+i)*46.7,47.2)
				self.buttonEquipe2[i].setIcon(qtg.QIcon("./images/2_"+ token[i]))
				self.buttonEquipe2[i].setIconSize(qtc.QSize(35,35))
				self.buttonEquipe2[i].setStyleSheet("background-color: transparent")			
				self.buttonEquipe2[i].show()
		self.buttonBallon = qtg.QPushButton(self.window)
		self.buttonBallon.resize(46.7,47.2)
		self.buttonBallon.move(67,478)
		self.buttonBallon.setStyleSheet("background-color: transparent")
		self.buttonBallon.setIcon(qtg.QIcon("./images/ballon.png"))
		self.buttonBallon.setIconSize(qtc.QSize(25,25))			
		self.buttonBallon.show()
		self.window.show()
		self.thread = listen()
		self.window.connect(self.thread, qtc.SIGNAL("update"), self.update)
		self.thread.start()
		sys.exit(self.app.exec_())

	def update(self,value):
		for i in range(6):
			if value.equipe1.equipe[i].ko:
				self.buttonEquipe1[i].move(67+(value.equipe1.equipe[i].pos[0])*(46.7-10),
					478-value.equipe1.equipe[i].pos[1]*(47.2+10))
				self.buttonEquipe1[i].setIcon(qtg.QIcon("./images/1_"+ token[6]))
				self.buttonEquipe1[i].setIconSize(qtc.QSize(25,25))
				self.buttonEquipe1[i].show()

			else:
				self.buttonEquipe1[i].move(67+(value.equipe1.equipe[i].pos[0])*(46.7),
					478-value.equipe1.equipe[i].pos[1]*(47.2))
				self.buttonEquipe1[i].setIcon(qtg.QIcon("./images/1_"+ token[i]))
				self.buttonEquipe1[i].setIconSize(qtc.QSize(35,35))
				self.buttonEquipe1[i].show()

			if value.equipe2.equipe[i].ko:
				self.buttonEquipe2[i].move(67+(value.equipe2.equipe[i].pos[0])*(46.7-10),
					478-value.equipe2.equipe[i].pos[1]*(47.2+10))
				self.buttonEquipe2[i].setIcon(qtg.QIcon("./images/2_"+ token[6]))
				self.buttonEquipe2[i].setIconSize(qtc.QSize(25,25))
				self.buttonEquipe2[i].show()

			else:
				self.buttonEquipe2[i].move(67+(value.equipe2.equipe[i].pos[0])*(46.7),
					478-value.equipe2.equipe[i].pos[1]*(47.2))
				self.buttonEquipe2[i].setIcon(qtg.QIcon("./images/2_"+ token[i]))
				self.buttonEquipe2[i].setIconSize(qtc.QSize(35,35))
				self.buttonEquipe2[i].show()		


		(i,j) = value.ballon.position
		self.buttonBallon.move(67+i*46.7,478-j*47.2)
		self.buttonBallon.show()
		self.window.show()




"""
if __name__ == "__main__" :
	app = qtg.QApplication([])

	window = qtg.QMainWindow()
	window.resize(800,600)
	


	button = qtg.QPushButton(window)
	button.resize(700, 492)
	button.move(20, 90)
	button.setIcon(qtg.QIcon("./images/plateau.jpg"))
	button.setIconSize(qtc.QSize(700,492))
	button.show()
	window.show()
	#button2 = qtg.QPushButton(window)
	#button2.resize(48, 48)
	#button2.move(67, 478)
	#button2.show()
	button=[[None for j in range(8)] for i in range(13)]
	for i in range(13):
		for j in range(8):
			button[i][j]=qtg.QPushButton(window)
			button[i][j].resize(46.7,47.2)
			button[i][j].move(67+i*46.7,478-j*47.2)
			button[i][j].setIcon(qtg.QIcon("./images/1_normal1.png"))
			button[i][j].setIconSize(qtc.QSize(35,35))
			button[i][j].setStyleSheet("background-color: transparent")			
			button[i][j].show()
	window.show()
	app.exec_()"""