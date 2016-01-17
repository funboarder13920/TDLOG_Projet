import projet

dicoactions = {}
dicoactions["deplacement"] = projet.joueur.deplacement
dicoactions["placage"] = projet.joueur.placage
dicoactions["passe"] = projet.joueur.passe
dicoactions["tirAvant"] = projet.joueur.tirAvant

class IA:
    def __init__(self,jeu):
        self.jeu = jeu
        self.scoremax = 0
        self.actionsmax = []

    def actionsopt(self):
        while(condition):
            score = 0
            actions = []
            #On stocke les actions sous forme de liste : le joueur qui effectuel l'action, l'action, et l'argument éventuel de l'action (joueur ou position par exemple)
            if self.jeu.ballon.porteur.nEquipe == 1: #l'adversaire a le ballon
                pass
            elif self.jeu.ballon.porteur.nEquipe == 2: #l'IA a le ballon
                pass
            else: #le ballon est au sol
                pass
            if score > self.scoremax:
                self.scoremax = score
                self.actionsmax = action

    def joue(self):
        for e in range(len(self.actionsmax)):
            if self.actionsmax[e][1] == "placage":
                if self.jeu.ballon.porteur.nEquipe == 1:
                    self.actionsmax[e][0].dicoactions[self.actionsmax[e][1]](self.actionsmax[e][2],True)
                elif self.jeu.ballon.porteur.nEquipe == 2:
                    self.actionsmax[e][0].dicoactions[self.actionsmax[e][1]](self.actionsmax[e][2],False)
            else:
                self.actionsmax[e][0].dicoactions[self.actionsmax[e][1]](self.actionsmax[e][2])
