nbColonne = 13
nbLigne = 8

class jeu :
	def __init__(self):
		self.matrice = [ [0 for i in range(nbColonne)] for j in nbLigne]
		self.equipe1 = 
		self.equipe2
		self.ballon

class ballon :
	def __init__(self):
		self.position

class joueur : 
	def __init__(self,jeu,nbEquipe,position,classe ):
		self.position = position
		self.classe = classe
		self.porteur = False
		self.jeu = jeu
		self.ko = False
		self.equipe 

class equipe :
	def __init__(self,jeu,nbEquipe,position,classe):
		self.equipe = [joueur(jeu,nbEquipe,position[i],classe[i]) for i in range(6)]
		self.score = 0
		self.jeu = jeu
		self.carte = [True for i in range(6)]

