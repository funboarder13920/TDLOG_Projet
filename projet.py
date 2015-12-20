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

def add(p1,p2):
    return(p1[0]+p2[0],p1[1]+p2[1])

def absol(point):
        return (abs(point[0]),abs(point[1]))

def droite(point1,point2):
        # retourne a,b,c de la droite ax+by+c=0 passant par point1 et point2
        assert point1 != point2
        if point1[0] == point2[0]:
                return(1,0,-point1[0])
        else:
                pinter = (point1[0] - point2[0],point1[1] - point2[1])
                a = -pinter[1] / pinter[0]
                return(a,1,-a * point1[0] - point1[1])

def calcPosDroite(r,pos):
        return r[0] * pos[0] + r[1] * pos[1] + r[2]

def inRange(pos):
        return (pos[0] > 0 and pos[0] < 12 and pos[1] >= 0 and pos[1] < 8)

def intInput(strarg=""):
        while True:
                try:
                        num1 = int(input(strarg))
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
                        if (posx >= 1 and posx <= 2 and posy >= 0 and posy < 8):
                                if not (posx,posy) in positions:
                                        log.info("ChoixPos: append de (%d,%d)",posx,posy)
                                        k+=1
                                        positions.append((posx,posy))
                                else:
                                        log.info("ChoixPos: position déjà occupée")
                        else:
                                log.info("ChoixPos : (%d,%d) hors limite",posx,posy)
                else :
                        if (posx >= 10 and posx <= 11 and posy >= 0 and posy < 8):
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
                self.ballon = ballon((7,1 + random.randint(1,6)))
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
                formeAtt = attaquant.equipe.forme()
                formeDef = defenseur.equipe.forme()
                vAtt = bonus[attaquant.prop][0] + formeAtt
                vDef = bonus[defenseur.prop][1] + formeDef
                if vAtt != vDef:
                        return vAtt > vDef
                else:
                        vAtt = bonus[attaquant.prop][0] + attaquant.equipe.forme()
                        vDef = bonus[defenseur.prop][1] + defenseur.equipe.forme()
                        if vAtt != vDef:
                                return vAtt > vDef
                        else: 
                                return False

        def libre(self,pos,couprestant=0):
                assert(pos[0]>=0 and pos[0]<nbColonne and pos[1]>=0 and pos[1]<nbLigne)
                print(self.matrice[pos[0]][pos[1]].nEquipe)
                return self.matrice[pos[0]][pos[1]].nEquipe == 3 or (self.matrice[pos[0]][pos[1]].ko and couprestant >= 2)

        def finTour(self):
                for joueur in self.equipe:
                        if len(self.matrice[joueur.pos[0]][self.joueur.pos[1]]) != 1:
                                return False
                return True

        def interception(self,joueur1,joueur2):
                pos1 = joueur1.pos
                pos2 = joueur2.pos
                r1 = droite(add(pos1 ,(-1 / 2,-1 / 2)),add(pos2 ,(-1 / 2,-1 / 2)))
                r2 = droite(add(pos1 ,(1 / 2,1 / 2)),add(pos2 , (1 / 2,1 / 2)))
                v1 = droite(add(pos1 , (-1 / 2,1 / 2)),add(pos2 , (-1 / 2,1 / 2)))
                v2 = droite(add(pos1 , (1 / 2,-1 / 2)),add(pos2 , (1 / 2,-1 / 2)))
                c1=droite(pos1,add(pos1,(1/2,0)))
                c2=droite(pos2,add(pos2,(1/2,0)))
                d1=droite(pos1,add(pos1,(0,1/2)))
                d2=droite(pos2,add(pos2,(0,1/2)))
                inter = []
                if joueur1.nEquipe == 1:
                        for joueur in self.equipe2.equipe:
                                if ((calcPosDroite(r1,joueur.pos) * calcPosDroite(r2,joueur.pos) <= 0 or 
                                    calcPosDroite(v1,joueur.pos) * calcPosDroite(v2,joueur.pos)<=0) and
                                    (calcPosDroite(d1,joueur.pos)*calcPosDroite(d2,joueur.pos)<0 or
                                    calcPosDroite(c1,joueur.pos)*calcPosDroite(c2,joueur.pos)<0)):
                                        inter.append(joueur)
                else:
                        for joueur in self.equipe1.equipe:
                                if ((calcPosDroite(r1,joueur.pos) * calcPosDroite(r2,joueur.pos) <= 0 or 
                                    calcPosDroite(v1,joueur.pos) * calcPosDroite(v2,joueur.pos)<=0)
                                    and (calcPosDroite(d1,joueur.pos)*calcPosDroite(d2,joueur.pos)<0 or
                                    calcPosDroite(c1,joueur.pos)*calcPosDroite(c2,joueur.pos)<0)):
                                        inter.append(joueur)
                return inter



class ballon :
        def __init__(self,position):
                self.position = position

        #Réinitialisation de la position du ballon sur celle du joueur porteur
        def porteur(self,jeu):
                for j in jeu.equipe1.equipe:
                        if j.porteur:
                                self.position = j.pos
                for k in jeu.equipe2.equipe:
                        if k.porteur:
                                self.position = k.pos


class joueur : 
        def __init__(self,equipe,jeu,nEquipe,position,prop, numero):
                self.pos = position
                self.numero = numero
                self.porteur = False
                self.jeu = jeu
                self.ko = False
                self.equipe = equipe
                self.nEquipe = nEquipe
                self.prop = prop
                self.jeu.matrice[position[0]][position[1]] = self
                if nEquipe != 3:
                        self.depRestant = bonus[self.prop][2]
                else:
                        self.depRestant = 0

        def deplace(self,pos):
                self.jeu.matrice[self.pos[0]][self.pos[1]],self.jeu.matrice[pos[0]][pos[1]] = self.jeu.matrice[pos[0]][pos[1]],self.jeu.matrice[self.pos[0]][self.pos[1]]
                self.depRestant -= 1
                self.pos = pos

        def deplacement(self,pos):
                #pas par pas c'est plus simple
                # le joueur ne doit pas être KO et le déplacement doit être
                # d'au plus 1
                if not self.ko:
                        if abs(self.position - pos) == 1 and self.jeu.libre(pos,self.couprestant) and self.onGrid():
                                if self.coupRestant == bonus[self.prop][2] and self.coupRestant != 0:
                                        #Le joueur ne s'est pas encore déplacé
                                        if self.equipe.coupRestant > 0:
                                                self.coupRestant -=1
                                                self.deplace(pos)
                                                if self.ballon.pos == pos:
                                                        self.porteur = True
                                elif self.equipe[j].coupRestant != 0 and self.equipe[j].coupRestant != bonus[self.equipe[j].prop][2]:
                                        self.deplace(pos)
                                        if self.ballon.pos == pos:
                                                        self.porteur = True

        def onGrid(self):
                posx = self.pos[0]
                posy = self.pos[1]
                if self.nEquipe == 1:
                        if self.porteur:
                                return (posx >= 0 and posx < 12 and posy >= 0 and posy < 8)
                        else:
                                return (posx > 0 and posx < 12 and posy >= 0 and posy < 8)
                else :
                        if self.porteur:
                                return (posx > 0 and posx <= 12 and posy >= 0 and posy < 8)
                        else:
                                return (posx > 0 and posx < 12 and posy >= 0 and posy < 8)


        def enArriere(self,joueur2):
                #joueur2 est il derrière joueur 1?
                if self.nEquipe == 1:
                        return (self.pos[0] - joueur2.pos[0]) > 0 and max(absol(self.pos - joueur2.pos)) <= 2
                else :
                        return (self.pos[0] - joueur2.pos[0]) < 0 and max(absol(self.pos - joueur2.pos)) <= 2

        def passe(self,joueur2):
                if self.porteur:
                        if self.enArriere(joueur2):
                                self.porteur = False
                                joueur2.porteur = True
                                interc = self.jeu.interception(self.posx,self.posy,joueur2.posx,joueur2.posy)
                                for adv in interc:
                                        if askIntercepter():
                                                if jeu.resolution(self,adv):
                                                        adv.porteur = True
                                                        joueur2.porteur = False
                                                        break
                                        else:
                                                log.info("L'adversaire n'intercepte pas")
                        else:
                                log.error("passe: passe en avant")
                else:
                        log.error("passe: le joueur n'est pas porteur")

        def placage(self,joueur2):
                if abs(self.pos - joueur2.pos) == 1 and self.depRestant > 1:
                        if joueur2.nEquipe != 3 and joueur2.nEquipe != self.nEquipe and not joueur2.KO and joueur2.porteur: #On ne peut plaquer le joueur que si il a le ballon
                                if self.jeu.resolution(self,joueur2):
                                        joueur2.KO = True
                                        self.jeu.matrice[self.pos[0]][self.pos[1]] = joueur(None,self,3,self.pos,"",0)
                                        self.pos = joueur2.pos
                                        self.jeu.matrice[self.pos[0]][self.pos[1]] = [self.jeu.matrice[self.pos[0]][self.pos[1]],self]
                                        self.depRestant -= 1
                                        #Le ballon va derriere joueur2
                                        if joueur2.nEquipe == 1:
                                                self.jeu.ballon.position += (0,-1)
                                        else:
                                                self.jeu.ballon.position += (0,1)
                                else:
                                        self.KO = True
                                        if len(self.jeu.matrice[self.pos[0]][self.pos[1]]) != 1:
                                                (dx,dy) = -joueur2.pos + self.pos
                                                if inRange(dx + self.pos) and len(self.jeu.matrice[(dx + self.pos)[0]][(dy + self.pos)[1]]) == 1:
                                                        self.deplace(self.pos + (dx,dy))
                                                else:
                                                        if inRange(2 * (dx,dy) + self.pos) and len(self.jeu.matrice[(2 * dx + self.pos)[0]][(2 * dy + self.pos)[1]]) == 1:
                                                                self.deplace(self.pos + 2 * (dx,dy))
                                                        elif inRange((dy,dx) + self.pos) and len(self.jeu.matrice[(dy + self.pos)[0]][(dx + self.pos)[1]]) == 1:
                                                                self.deplace(self.pos + (dy,dx))
                                                        elif inRange((-dy,-dx) + self.pos) and len(self.jeu.matrice[(-dy + self.pos)[0]][(-dx + self.pos)[1]]) == 1:
                                                                self.deplace(self.pos + (-dx,-dy))
                                                        else :
                                                                assert False
                                                                #Pour le test,
                                                                #à enlever
                                                                #normalement
        
        def nobodyFront(self):
                if self.nEquipe == 1:
                        for joueur in self.equipe:
                                if joueur.pos[0] > self.pos[0]:
                                        return False
                        return True
                else:
                        for joueur in self.equipe:
                                if joueur.pos[0] < self.pos[0]:
                                        return False
                        return True

        def front(self,pos):
                if self.nEquipe == 1:
                        return pos[0] - self.pos[0] > 0 and pos[0] - self.pos[0] <= 3
                else:
                        return pos[0] - self.pos[0] < 0 and -pos[0] + self.pos[0] <= 3


        def tirAvant(self,pos):
                if self.porteur:
                        if self.nobodyFront(pos) and self.front(pos) and self.jeu.matrice[pos].nEquipe == 3: #doit attérir sur une case vide
                                self.porteur = False
                                self.ballon.position = pos




class equipe :
        def __init__(self,jeu,nEquipe,positions):
                self.equipe = [joueur(self,jeu,nEquipe,positions[i],prop[i],i) for i in range(6)]
                self.score = 0
                self.coupRestant = 2
                self.jeu = jeu
                self.carte = [True for i in range(6)]

        def joue(self):
                #Reinitialisation
                self.coupRestant = 2
                for joueur in self.equipe:
                        joueur.depRestant = bonus[joueur.prop][2]
                cont = True
                while cont:
                        optionJeu()
                        opt = intInput("Action: ")
                        # 0 = passe
                        if opt == 0:
                                reglePasse()
                                j1 = intInput("Joueur 1: ")
                                while True:
                                        try :
                                                j2 = intInput("Joueur 2: ")
                                                assert j2 != j1
                                                self.equipe[j1].passe(self.equipe[j2])
                                                break
                                        except:
                                                pass
                        elif opt == 1:
                                regleDeplacement()
                                j = intInput("Joueur: ")
                                posx = intInput("posx: ")
                                posy = intInput("posy: ")
                                self.equipe[j].deplacement((posx,posy))
                                if self.equipe[j].pos[0] == 0 or self.equipe[j].pos[0] == 12:
                                        cont = True
                                        self.score += 1
                                        self.jeu.fin()
                                        break
                        elif opt == -1:
                                if self.jeu.finTour():
                                        cont = False
                                else:
                                        print("Des joueurs se superposent")
                #on lui demande quoi jouer


        def forme(self):
                if self.carte == [False for i in range(6)]:
                        self.carte = [True for i in range(6)]
                cartePossible = []
                for i in range(len(self.carte)):
                        if self.carte[i]:
                                cartePossible.append(i)
                e = random.randint(0,len(cartePossible) - 1)
                self.carte[cartePossible[e]]=False
                return cartePossible[e] + 1



if __name__ == "__main__":
        jeu = jeu()