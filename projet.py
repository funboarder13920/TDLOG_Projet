import random
import logging
import logging.config


logging.config.fileConfig("log.conf")
log = logging.getLogger("application")
nbColonne = 13
nbLigne = 8
prop = ["ordinaire","ordinaire","dur","costaud","fute","rapide"]

def intInput(str):
	while True:
		try:
			num1 = int(input(str))
		except ValueError:
			continue
		else:
			break
	return num1

def choixPos(nEquipe):
	log.debug("choixPos sur nEquipe = %d",nEquipe)
	if not (nEquipe == 2 or nEquipe == 1):
		log.error("Erreur dans choixPos avec nEquipe = %d",nEquipe)
		assert nEquipe == 2 or nEquipe == 1
	positions = []
	k = 0
	while k < 6 :
		print(prop[k],"?")
		posx = intInput("x: ")
		posy = intInput("y: ")
		log.info("ChoixPos : input (%d,%d)",posx,posy)
		if (nEquipe == 1):
			if (posx>= 1 and posx <=2 and posy>=0 and posy < 8):
				if not (posx,posy) in positions:
					log.info("ChoixPos: append de (%d,%d)",posx,posy)
					k+=1
					positions.append((posx,posy))
				else:
					log.info("ChoixPos: position déjà occupée")
			else:
				log.info("ChoixPos : (%d,%d) hors limite",posx,posy)
		else :
			if (posx>= 10 and posx <=11 and posy>=0 and posy < 8):
				if not (posx,posy) in positions:
					log.info("ChoixPos: append de (%d,%d)",posx,posy)
					k+=1
					positions.append((posx,posy))
				else:
					log.info("ChoixPos: position déjà occupée")
			else:
				log.info("ChoixPos : (%d,%d) hors limite",posx,posy)

	return positions

class jeu :
	def __init__(self):
		log.debug("Initialisation du jeu")
		self.matrice = [ [0 for i in range(nbLigne)] for j in range(nbColonne)]
		print("Choix équipe 1")
		positions1 = choixPos(1)
		print("Choix équipe 2")
		positions2 = choixPos(2)
		self.equipe1 = equipe(self,1,positions1)
		self.equipe2 = equipe(self,2,positions2)
		self.ballon = ballon((7,1+random.randint(1,6)))
		self.tour = 1

class ballon :
	def __init__(self,position):
		self.position = position

class joueur : 
	def __init__(self,equipe,jeu,nEquipe,position,prop):
		self.position = position
		self.porteur = False
		self.jeu = jeu
		self.ko = False
		self.equipe = equipe
		self.prop = prop
		jeu.matrice[position[0]][position[1]] = self 

class equipe :
	def __init__(self,jeu,nEquipe,positions):
		self.equipe = [joueur(self,jeu,nEquipe,positions[i],prop[i]) for i in range(6)]
		self.score = 0
		self.jeu = jeu
		self.carte = [True for i in range(6)]

jeu = jeu()
print(jeu.matrice[5][2])