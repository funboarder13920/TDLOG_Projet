import PyQt4.QtCore as qtc
import PyQt4.QtGui as qtg
import sys
import random
import time


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
	app.exec_()