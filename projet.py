import random
import logging
import logging.config
import copy

logging.config.fileConfig("log.conf")
log = logging.getLogger("application")
nbColonne = 13
nbLigne = 8
prop = ["ordinaire","ordinaire","dur","costaud","fute","rapide"]
# propriété ,( bonus attaque , bonus défense, déplacement)
bonus = {'ordinaire':(0,0,3),'dur':(1,0,3),'costaud':(2,1,2),'fute':(0,1,3),'rapide':(-1,-1,4)}

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
		for i in range(nbLigne):
			for j in range(nbColonne):
				joueur(None,self,3,(j,i),"",0)
		print("Choix équipe 1")
		positions1 = choixPos(1)
		print("Choix équipe 2")
		positions2 = choixPos(2)
		self.equipe1 = equipe(self,1,positions1)
		self.equipe2 = equipe(self,2,positions2)
		self.ballon = ballon((7,1+random.randint(1,6)))
		self.tour = 1

	def tour(self):
		if self.tour == 1:
			self.equipe1.joue()
			self.tour = 2
		else : 
			self.equipe2.joue()
			self.tour = 1

	def resolution(self,attaquant,defenseur):
		#Est ce que l'attaquant gagne?
		attaquant.equipe.forme()
		defenseur.equipe.forme()
		vAtt = bonus[attaquant.prop][0] + attaquant.equipe.forme()
		vDef = bonus[defenseur.prop][1] + defenseur.equipe.forme()
		if vAtt != vDef:
			return vAtt>vDef
		else:
			vAtt = bonus[attaquant.prop][0] + attaquant.equipe.forme()
			vDef = bonus[defenseur.prop][1] + defenseur.equipe.forme()
			if vAtt != vDef:
				return vAtt>vDef
			else: 
				return False

	def libre(self,pos,couprestant = 0):
		return self.matrice[pos[1]][pos[2]].equipe == 3 or (self.matrice[pos[1]][pos[2]].ko and couprestant >=2)



class ballon :
	def __init__(self,position):
		self.position = position

class joueur : 
	def __init__(self,equipe,jeu,nEquipe,position,prop, numero):
		self.position = position
		self.numero = numero
		self.porteur = False
		self.jeu = jeu
		self.ko = False
		self.equipe = equipe
		self.nEquipe = nEquipe
		self.prop = prop
		self.jeu.matrice[position[0]][position[1]] = self
		self.couprestant = 

	def deplacement(self,pos):
		#pas par pas c'est plus simple
		if not self.ko:
			if abs(self.position  - pos)==1 and self.jeu.libre(pos,self.couprestant) and self.onGrid():
				pass
				#modifmatrice

	def onGrid(self):
		if self.nEquipe==1:
			if self.porteur:
				return (posx>=0 and posx<12 and posy>=0 and posy<8)
			else:
				return (posx>0 and posx<12 and posy>=0 and posy<8)
		else :
			if self.porteur:
				return (posx>0 and posx<=12 and posy>=0 and posy<8)
			else:
				return (posx>0 and posx<12 and posy>=0 and posy<8)


	def enArriere(self,joueur2):
		#joueur2 est il derrière joueur 1?
		if self.nEquipe == 1:
			return (self.pos[0]-joueur2.pos[0])>0
		else :
			return (self.pos[0]-joueur2.pos[0])<0

	def passe(self,joueur2):
		if self.porteur:
			if self.enArriere(joueur2):
				interc = self.jeu.interception(self.posx,self.posy,joueur2.posx,joueur2.posy)
				if interc[0]:
					if askIntercepter():
						jeu.resolution(self,interc[1])
					else:
						log.info("L'adversaire n'intercepte pas")
				else:
					log.info("passe sans interception")
					self.porteur = False
					joueur2.porteur = True
			else:
				log.error("passe: passe en avant")
		else:
			log.error("passe: le joueur n'est pas porteur")


class equipe :
	def __init__(self,jeu,nEquipe,positions):
		self.equipe = [joueur(self,jeu,nEquipe,positions[i],prop[i],i) for i in range(6)]
		self.score = 0
		self.coup = 0
		self.jeu = jeu
		self.carte = [True for i in range(6)]

	def joue(self):
		self.coup = 2
		while True:
			optionJeu()
			opt = intInput("Action: ")
			# 0 =  passe
			if opt == 0:
				reglePasse()
				j1 = intInput("Joueur 1: ")
				while True:
					try :
						j2 = intInput("Joueur 2: ")
						assert j2!=j1
						jeu.passe(equipe[j1],equipe[j2])
						break
					except:
						pass
			elif opt == 1:
				regleDeplacement()
				j = intInput("Joueur: ")



		#on lui demande quoi jouer

	def forme(self):
		if self.carte == [False for i in range(6)]:
			self.carte = [True for i in range(6)]
		cartePossible = []
		for i in range(len(self.carte)):
			if carte[i]:
				cartePossible.append(i)
		e = random.randint(0,len(cartPossible)-1)
		return cartePossible(e)+1



jeu = jeu()
print(jeu.matrice)


#garder en liste quel joueur a été joué, on passe quand on dit ok on a fini
#verifier qu'il n'y a pas de joueur retourné sur la case d'arrêt