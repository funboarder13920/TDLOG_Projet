#!/usr/bin/python
# -*- coding: latin-1 -*-
import random
import globalQueue
#import fakeNone
import logging
import logging.config
import copy
import os

logging.config.fileConfig("log.conf")
log = logging.getLogger("application")
nbColonne = 13
nbLigne = 8
prop = ["ordinaire", "ordinaire", "dur", "costaud", "fute", "rapide"]
# propriété ,( bonus attaque , bonus défense, déplacement)
bonus = {'ordinaire': (0, 0, 3), 'dur': (1, 0, 3), 'costaud': (
    2, 1, 2), 'fute': (0, 1, 3), 'rapide': (-1, -1, 4)}


def add(p1, p2):
    return(p1[0] + p2[0], p1[1] + p2[1])


def sub(p1, p2):
    return(p1[0] - p2[0], p1[1] - p2[1])


def absol(point):
    return (abs(point[0]), abs(point[1]))


def droite(point1, point2):
    log.debug("droite({0},{0})", point1, point2)
    # retourne a,b,c de la droite ax+by+c=0 passant par point1 et point2
    assert point1 != point2
    if point1[0] == point2[0]:
        return(1, 0, -point1[0])
    else:
        pinter = sub(point1, point2)
        a = -pinter[1] / pinter[0]
        return(a, 1, -a * point1[0] - point1[1])


def calcPosDroite(r, pos):
    return r[0] * pos[0] + r[1] * pos[1] + r[2]


def inRange(pos):
    return (pos[0] > 0 and pos[0] < 12 and pos[1] >= 0 and pos[1] < 8)


def intInput(strarg=""):
    log.debug("Saisie de l'entier %s", strarg)
    while True:
        try:
            num1 = int(input(strarg))
        except ValueError as e:
            print("Vous devez saisir un nombre")
            log.error("Nombre %s invalide", strarg)
            continue
        else:
            break
    return num1


def choixPos(nEquipe):
    log.info("Choix de l'équipe %d ...", nEquipe)
    if not (nEquipe == 2 or nEquipe == 1):
        log.error("Equipe {0} impossible", nEquipe)
        assert nEquipe == 2 or nEquipe == 1
    positions = []
    k = 0
    while k < 6:
        print("\n")
        # print "Joueur " , (k+1) , prop[k] , "..."
        posx = intInput("x: ")
        posy = intInput("y: ")
        log.debug("Un joueur %s est choisi sur (%d,%d)", prop[k], posx, posy)
        if (nEquipe == 1):
            if (posx >= 1 and posx <= 2 and posy >= 0 and posy < 8):
                if not (posx, posy) in positions:
                    k += 1
                    positions.append((posx, posy))
                    log.debug("Append de (%d,%d)", posx, posy)
                else:
                    print("Veuillez réessayer : la position est déjà occupée.")
                    log.warn("Position (%d,%d) déjà occupée", posx, posy)
            else:
                print(
                    "Veuillez réessayer : la position est hors limite. 1=<x<=2 0<=y<=7")
                log.warn("(%d,%d) est hors limite", posx, posy)
        else:
            if (posx >= 10 and posx <= 11 and posy >= 0 and posy < 8):
                if not (posx, posy) in positions:
                    k += 1
                    positions.append((posx, posy))
                    log.info("Append de (%d,%d)", posx, posy)
    return positions

def libre(self,pos,depRestant=0):
        log.debug("Test Libre de la position ({0},{0})",pos[0],pos[1])
        assert(pos[0]>=0 and pos[0]<nbColonne and pos[1]>=0 and pos[1]<nbLigne)
        isLibre = (self.matrice[pos[0]][pos[1]][-1].nEquipe == 3 or (self.matrice[pos[0]][pos[1]][-1].ko and depRestant >= 2))
        log.debug("Résultat : %d", isLibre)                
        return isLibre

def finTour(self):
        log.debug("Test fin du tour")
        for joueur in self.equipe:
                if len(self.matrice[joueur.pos[0]][self.joueur.pos[1]]) != 1:
                    log.debug("Le tour n'est pas fini")
                    return False
        log.debug("Le tour est fini")
        return True

def interception(self,joueur1,joueur2):
        pos1 = joueur1.pos
        pos2 = joueur2.pos
        log.info("Interception entre ({0},{0}) et ({0},{0})",pos1[0],pos1[1],pos2[0],pos2[1] )
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
                        if ((calcPosDroite(r1,joueur.pos) * calcPosDroite(r2,joueur.pos) < 0 or 
                            calcPosDroite(v1,joueur.pos) * calcPosDroite(v2,joueur.pos)<0) and
                            (calcPosDroite(d1,joueur.pos)*calcPosDroite(d2,joueur.pos)<0 or
                            calcPosDroite(c1,joueur.pos)*calcPosDroite(c2,joueur.pos)<0)):
                                inter.append(joueur)
                                log.debug("Interception par l'équipe 1 du joueur %d",joueur.numero)
        else:
                for joueur in self.equipe1.equipe:
                        if ((calcPosDroite(r1,joueur.pos) * calcPosDroite(r2,joueur.pos) < 0 or 
                            calcPosDroite(v1,joueur.pos) * calcPosDroite(v2,joueur.pos)<0)
                            and (calcPosDroite(d1,joueur.pos)*calcPosDroite(d2,joueur.pos)<0 or
                            calcPosDroite(c1,joueur.pos)*calcPosDroite(c2,joueur.pos)<0)):
                                inter.append(joueur)
                                log.debug("Interception par l'équipe 2 du joueur %d",joueur.numero)
        return inter


class ballon :
        def __init__(self,position,jeu):
                log.debug("Initialisation du ballon à la position (%d,%d)",position[0],position[1])
                self.position = position
                self.jeu = jeu
                self.porteur = self.jeu.matrice[position[0]][position[1]]

        def deplacement(self):
                if self.porteur.nEquipe!=3:
                        self.position = self.porteur.pos
                        log.debug("Le ballon se deplace à la postion (%d,%d)",self.position[0],self.position[1])

class jeu:

    def __init__(self):
        log.info("Création du jeu")
        self.matrice = [[0 for i in range(nbLigne)] for j in range(nbColonne)]
        for i in range(nbLigne):
            for j in range(nbColonne):
                joueur(None, self, 3, (j, i), "", 0)
        os.system('clear')
        # TODO :Mettre ce texte dans une fonction printIntro
        print("****************************************** Kahmaté ******************************************")
        print("Auteurs : Valentin B., Quentin B., François D (2015) ")
        print("\nLe Kahmaté se joue à deux joueurs, amusez-vous bien !")
        print("Voir règle du jeu sur : http://jeuxstrategie1.free.fr/jeu_kahmate/regle.pdf")
        print("\n")
        print("Instructions: ")
        print("* Suivre les instructions de la console")
        print("* Pour arrêter la partie : CTRL+D ")  # TODO : à implémenter
        print("**********************************************************************************************")
        print("\nChoix de la position des joueurs de l'équipe 1")
        positions1 = choixPos(1)
        print("\nChoix de la position des joueurs de l'équipe 2")
        positions2 = choixPos(2)
        self.equipe1 = equipe(self, 1, positions1)
        self.equipe2 = equipe(self, 2, positions2)
        self.ballon = ballon((6, 1 + random.randint(1, 6)), self)
        self.tour = 1
        globalQueue.queue.put(self)
        # self.equipe1.joue()

    def changeTour(self):
        log.info("Début des tours de jeu")
        if self.tour == 1:
            log.info("Tour de jeu équipe 1")
            self.equipe1.joue()
            self.tour = 2
        else:
            log.info("Tour de jeu équipe 2")
            self.equipe2.joue()
            self.tour = 1

    def resolution(self, attaquant, defenseur):
        log.info("Résolution attaquant %d équipe %d - défenseur %d équipe %d ",
                 attaquant.numero, attaquant.nEquipe, defenseur.numero, defenseur.nEquipe)
        vAtt = bonus[attaquant.prop][0] + attaquant.equipe.forme()
        vDef = bonus[defenseur.prop][1] + defenseur.equipe.forme()
        print("Attaquant : %d,Défenseur : %d", (vAtt, vDef))
        if vAtt > vDef:
            print("\n Victoire de l'attaquant par %d", vAtt - vDef)
            log.debug("Résultat : %d", vAtt - vDef)
            return vAtt - vDef
        elif vDef > vAtt:
            print("\n Victoire du défenseur par %d", vDef - vAtt)
            log.debug("Résultat : %d", vAtt - vDef)
            return vAtt - vDef
        else:
            print("Egalité, on tire une nouvelle carte forme")
            vAtt = bonus[attaquant.prop][0] + attaquant.equipe.forme()
            vDef = bonus[defenseur.prop][1] + defenseur.equipe.forme()
            log.debug("Résultat : %d", vAtt - vDef)
            return vAtt - vDef

    def libre(self, pos, depRestant=0):
        log.debug("Test Libre de la position ({0},{0})", pos[0], pos[1])
        assert(pos[0] >= 0 and pos[0] < nbColonne and pos[
               1] >= 0 and pos[1] < nbLigne)
        isLibre = (self.matrice[pos[0]][pos[1]][-1].nEquipe ==
                   3 or (self.matrice[pos[0]][pos[1]][-1].ko and depRestant >= 2))
        log.debug("Résultat : %d", isLibre)
        return isLibre

    def finTour(self):
        log.debug("Test fin du tour")
        for joueur in self.equipe:
            if len(self.matrice[joueur.pos[0]][self.joueur.pos[1]]) != 1:
                log.debug("Le tour n'est pas fini")
                return False
        log.debug("Le tour est fini")
        return True

    def interception(self, joueur1, joueur2):
        pos1 = joueur1.pos
        pos2 = joueur2.pos
        log.info("Interception entre ({0},{0}) et ({0},{0})", pos1[
                 0], pos1[1], pos2[0], pos2[1])
        r1 = droite(add(pos1, (-1 / 2, -1 / 2)), add(pos2, (-1 / 2, -1 / 2)))
        r2 = droite(add(pos1, (1 / 2, 1 / 2)), add(pos2, (1 / 2, 1 / 2)))
        v1 = droite(add(pos1, (-1 / 2, 1 / 2)), add(pos2, (-1 / 2, 1 / 2)))
        v2 = droite(add(pos1, (1 / 2, -1 / 2)), add(pos2, (1 / 2, -1 / 2)))
        c1 = droite(pos1, add(pos1, (1 / 2, 0)))
        c2 = droite(pos2, add(pos2, (1 / 2, 0)))
        d1 = droite(pos1, add(pos1, (0, 1 / 2)))
        d2 = droite(pos2, add(pos2, (0, 1 / 2)))
        inter = []
        if joueur1.nEquipe == 1:
            for joueur in self.equipe2.equipe:
                if ((calcPosDroite(r1, joueur.pos) * calcPosDroite(r2, joueur.pos) < 0 or
                     calcPosDroite(v1, joueur.pos) * calcPosDroite(v2, joueur.pos) < 0) and
                    (calcPosDroite(d1, joueur.pos) * calcPosDroite(d2, joueur.pos) < 0 or
                     calcPosDroite(c1, joueur.pos) * calcPosDroite(c2, joueur.pos) < 0)):
                    inter.append(joueur)
                    log.debug(
                        "Interception par l'équipe 1 du joueur %d", joueur.numero)
        else:
            for joueur in self.equipe1.equipe:
                if ((calcPosDroite(r1, joueur.pos) * calcPosDroite(r2, joueur.pos) < 0 or
                     calcPosDroite(v1, joueur.pos) * calcPosDroite(v2, joueur.pos) < 0)
                    and (calcPosDroite(d1, joueur.pos) * calcPosDroite(d2, joueur.pos) < 0 or
                         calcPosDroite(c1, joueur.pos) * calcPosDroite(c2, joueur.pos) < 0)):
                    inter.append(joueur)
                    log.debug(
                        "Interception par l'équipe 2 du joueur %d", joueur.numero)
        return inter


class ballon:

    def __init__(self, position, jeu):
        log.debug("Initialisation du ballon à la position (%d,%d)",
                  position[0], position[1])
        self.position = position
        self.jeu = jeu
        self.porteur = self.jeu.matrice[position[0]][position[1]][-1]

    def deplacement(self):
        print(self.porteur.nEquipe)
        if self.porteur.nEquipe != 3:
            self.position = self.porteur.pos
            log.debug("Le ballon se deplace à la postion (%d,%d)",
                      self.position[0], self.position[1])


class joueur:

    def __init__(self, equipe, jeu, nEquipe, position, prop, numero):
        log.debug("Initialisation du joueur %d de l'équipe %d", numero, nEquipe)
        self.pos = position
        self.numero = numero
        self.porteur = False
        self.jeu = jeu
        self.ko = False
        self.equipe = equipe
        self.nEquipe = nEquipe
        self.prop = prop
        self.jeu.matrice[position[0]][position[1]] = [self]
        if nEquipe != 3:
            self.depRestant = bonus[self.prop][2]
        else:
            self.depRestant = 0

    def deplace(self, pos):
        log.debug("Le joueur %d se déplace à (%d,%d)",
                  self.numero, pos[0], pos[1])
        # Cas où on va sur une case où il y a un joueur ko
        if self.jeu.matrice[pos[0]][pos[1]][0].ko and not self.jeu.matrice[self.pos[0]][self.pos[1]][0].ko:
            self.jeu.matrice[pos[0]][pos[1]].append(self)
            self.jeu.matrice[self.pos[0]][self.pos[1]][0] = joueur(
                        None, self.jeu, 3, self.pos, "", 0)  # joueur de l'équipe 3 pour compléter
        elif self.jeu.matrice[self.pos[0]][self.pos[1]][0].ko and not self.jeu.matrice[pos[0]][pos[1]][0].ko:  # Cas où on part d'une case où il y a un joueur ko
            self.jeu.matrice[pos[0]][pos[1]][0] = self
            self.jeu.matrice[self.pos[0]][self.pos[1]].remove(self)
        # Cas où on part d'une case où un joueur est ko pour arriver ù une case
        # où un autre joueur est ko
        elif self.jeu.matrice[self.pos[0]][self.pos[1]][0].ko and self.jeu.matrice[pos[0]][pos[1]][0].ko:
            self.jeu.matrice[pos[0]][pos[1]].append(self)
            self.jeu.matrice[self.pos[0]][self.pos[1]].remove(self)
        else:  # Cas où les joueurs ko ne sont pas impliqués
            self.jeu.matrice[pos[0]][pos[1]][0] = self
            self.jeu.matrice[self.pos[0]][self.pos[1]][0] = joueur(
                        None, self.jeu, 3, self.pos, "", 0)
        self.depRestant -= 1
        self.pos = pos


    def deplacement(self, pos):
        log.info("Déplacement du joueur %d", self.numero)
        # pas par pas c'est plus simple
        # le joueur ne doit pas être KO et le déplacement doit être
        # d'au plus 1
        if not self.ko:
            if (absol(sub(self.pos, pos)) == (1, 0) or absol(sub(self.pos, pos)) == (0, 1)) and self.jeu.libre(pos, self.depRestant) and self.onGrid():
                if self.depRestant == bonus[self.prop][2] and self.depRestant > 0:
                    # Le joueur ne s'est pas encore déplacé
                    if self.equipe.coupRestant > 0:
                        self.equipe.coupRestant -= 1
                        self.deplace(pos)
                        if self.jeu.ballon.position == pos:
                            self.porteur = True
                            self.jeu.ballon.porteur = self
                    else:
                        log.error(
                            "Vous ne pouvez pas déplacer plus de joueurs")

                elif self.depRestant != bonus[self.prop][2]:
                    self.deplace(pos)
                    if self.jeu.ballon.position == pos:
                        self.porteur = True
                        self.jeu.ballon.porteur = self
                        print(self.numero)
            if self.porteur:
                log.info("Le joueur est porteur, le ballon doit aussi se déplacer")
                print(self.jeu.ballon.position, self.pos,
                      self.jeu.ballon.porteur.nEquipe)
                self.jeu.ballon.deplacement()
                print(self.jeu.ballon.position, self.pos,
                      self.jeu.ballon.porteur.nEquipe)
            else:
                log.error(
                    "Le joueur doit être libre et se déplacer d'une seule valeur")
        else:
            log.error("Le joueur ne doit pas être KO")
        globalQueue.queue.put(self.jeu)

    def onGrid(self):
        log.debug("Test si la postion du joueur est bonne")
        posx = self.pos[0]
        posy = self.pos[1]
        if self.nEquipe == 1:
            if self.porteur:
                return (posx >= 0 and posx < 12 and posy >= 0 and posy < 8)
            else:
                return (posx > 0 and posx < 12 and posy >= 0 and posy < 8)
        else:
            if self.porteur:
                return (posx > 0 and posx <= 12 and posy >= 0 and posy < 8)
            else:
                return (posx > 0 and posx < 12 and posy >= 0 and posy < 8)

    def enArriere(self, joueur2):
        log.debug("Test si le joueur 2 est derrière joueur 1")
        # joueur2 est il derrière joueur 1?
        if self.nEquipe == 1:
            return (self.pos[0] - joueur2.pos[0]) > 0 and max(absol(sub(self.pos, joueur2.pos))) <= 2
        else:
            return (self.pos[0] - joueur2.pos[0]) < 0 and max(absol(sub(self.pos, joueur2.pos))) <= 2

    def askIntercepter(self, joueur1, joueur2):
        log.info("Demande au joueur adverse l'interception")
        print("Au joueur de l'équipe %d", joueur1.nEquipe)
        print("Voulez-vous intercepter le lancer du joueur adverse %s de coordonnées (%d,%d) au joueur adverse %s de coordonnées (%d,%d)",
              (prop[joueur1.numero], joueur1.pos[1], joueur1.pos[0], prop[joueur2.numero], joueur2.pos[1], joueur2.pos[0]))
        print("\n , avec votre joueur %s de coordonnées de coordonnées (%d,%d)",
              (prop[self.numero], self.pos[1], self.pos[0]))
        print("\n")
        print("Si oui, tapez 1. Sinon tapez 0")
        intercepte = intInput("Interception: ")
        if (intercepte == 1):
            return True
        else:
            return False

    def passe(self, joueur2):
        log.info(
            "Le joueur %s essayer de passer au joueur {0}", self.numero, joueur2.numero)
        if self.porteur:
            if self.enArriere(joueur2):
                self.porteur = False
                joueur2.porteur = True
                self.jeu.ballon.porteur = joueur2
                self.jeu.ballon.deplacement()
                interc = self.jeu.interception(self, joueur2)
                print(len(interc))
                for adv in interc:
                    if adv.askIntercepter(self, joueur2):
                        if jeu.resolution(self, adv) <= 0:
                            adv.porteur = True
                            joueur2.porteur = False
                            self.jeu.ballon.deplacement()
                            break
                    else:
                        log.info("La passe est réussie")
            else:
                log.error(
                    "La passe est impossible car le joueur %d n'est pas derrière", self.numero)
        else:
            log.error(
                "La passe est impossible car le joueur {0} n'est pas porteur", self.numero)
        globalQueue.queue.put(self.jeu)

    def placage(self, joueur2, plaquer):
        log.info("Le joueur {0} essaie de plaquer le joueur {0}",
                 self.numero, joueur2.numero)
        if absol(sub(self.pos, joueur2.pos)) == 1 and self.depRestant > 1:
            if joueur2.nEquipe != 3 and joueur2.nEquipe != self.nEquipe and not joueur2.KO and joueur2.porteur:
                if self.jeu.resolution(self, joueur2) > 0:
                    if self.jeu.resolution(self, joueur2) >= 2 and plaquer:
                        log.debug("Plaquage parfait")
                        self.porteur = True
                        self.jeu.ballon.porteur = self
                        self.jeu.ballon.deplacement()
                    else:
                        log.debug("Plaquage classique ou passage en force")
                        if joueur2.pos[0] > self.pos[0]:
                            log.debug("joueur plaqué à gauche du plaqueur")
                            if joueur2.pos[0] < nbColonne - 2:
                                self.jeu.ballon.position += (1, 0)
                            else:
                                log.debug("Joueur2 est sur le bord droit")
                                if joueur2.pos[1] < nbLigne / 2:
                                    self.jeu.ballon.position += (0, 1)
                                else:
                                    self.jeu.ballon.position += (0, -1)
                        elif joueur2.pos[0] < self.pos[0]:
                            log.debug("Joueur plaqué à droite du plaqueur")
                            if joueur2.pos[0] > 1:
                                self.jeu.ballon.position += (-1, 0)
                            else:
                                log.debug(
                                    "Cas particulier où le joueur plaqué est sur le bord gauche")
                                if joueur2.pos[1] < nbLigne / 2:
                                    self.jeu.ballon.position += (0, 1)
                                else:
                                    self.jeu.ballon.position += (0, -1)
                        else:
                            if joueur2.pos[1] < self.pos[1]:
                                log.debug(
                                    "Joueur plaqué au dessus du plaqueur")
                                if joueur2.pos[1] > 0:
                                    self.jeu.ballon.position += (0, -1)
                                else:
                                    log.debug(
                                        "Le joueur plaqué est tout en haut")
                                    if joueur2.pos[0] < nbColonne / 2:
                                        self.jeu.ballon.position += (1, 0)
                                    else:
                                        self.jeu.ballon.position += (-1, 0)
                            else:
                                log.debug(
                                    "Joueur plaqué en dessous du plaqueur")
                                if joueur2.pos[1] < nbLigne - 1:
                                    self.jeu.ballon.position += (0, 1)
                                else:
                                    log.debug(
                                        "Le joueur plaqué est tout en bas")
                                    if joueur2.pos[0] < nbColonne / 2:
                                        self.jeu.ballon.position += (1, 0)
                                    else:
                                        self.jeu.ballon.position += (-1, 0)
                        log.debug(
                            "Un joueur sur la case du ballon qui le récupère")
                        self.jeu.ballon.porteur = self.jeu.matrice[
                            self.jeu.ballon.position[0]][self.jeu.ballon.position[1]]
                        if self.jeu.ballon.porteur.nEquipe != 3:
                            self.jeu.ballon.porteur.porteur = True
                    joueur2.KO = True
                    joueur2.porteur = False
                    self.jeu.matrice[self.pos[0]][self.pos[1]][0] = joueur(
                        None, self.jeu, 3, self.pos, "", 0)
                    self.pos = joueur2.pos
                    self.jeu.matrice[self.pos[0]][self.pos[1]] = [
                        self.jeu.matrice[self.pos[0]][self.pos[1]], self]
                    if plaquer:
                        self.depRestant = 0
                    else:
                        self.depRestant -= 1
                else:
                    self.KO = True
        globalQueue.queue.put(self.jeu)

    def nobodyFront(self):
        log.debug("Test personne en face")
        if self.nEquipe == 1:
            for joueur in self.equipe.equipe:
                if joueur.pos[0] > self.pos[0]:
                    #log.debug("Résultat : Faux")
                    return False
            log.debug("Résultat : Vrai")
            return True
        else:
            for joueur in self.equipe.equipe:
                if joueur.pos[0] < self.pos[0]:
                    log.debug("Résultat : faux")
                    return False
            log.debug("Résultat : Vrai")
            return True

    def front(self, pos):
        log.debug("Test endroit où on envoie le ballon")
        if self.nEquipe == 1:
            return pos[0] - self.pos[0] > 0 and pos[0] - self.pos[0] <= 3
        else:
            return pos[0] - self.pos[0] < 0 and -pos[0] + self.pos[0] <= 3

    def tirAvant(self, pos):
        log.info("Le joueur {0} essaie de tirer en avant", self.numero)
        if self.porteur:
            if self.nobodyFront() and self.front(pos):
                self.porteur = False
                self.jeu.ballon.position = pos
                self.jeu.ballon.porteur = self.jeu.matrice[pos[0]][pos[1]][-1]
                self.jeu.matrice[pos[0]][pos[1]][-1].porteur = True
            elif (not self.nobodyFront(pos)):
                log.error(
                    "Le tir en avant est impossible car le joueur {0} a un joueur devant lui", self.numero)
            elif (not self.front(pos)):
                log.error(
                    "La case choisie n'est pas en avant du joueur {0}", self.numero)
                print("case non remplie")
            else:
                print("case non vide")
        globalQueue.queue.put(self.jeu)


class equipe:

    def __init__(self, jeu, nEquipe, positions):
        log.debug("Initialisation de l'équipe %d", nEquipe)
        self.equipe = [joueur(self, jeu, nEquipe, positions[
                              i], prop[i], i) for i in range(6)]
        self.score = 0
        self.coupRestant = 2
        self.jeu = jeu
        self.carte = [True for i in range(6)]
        self.nEquipe = nEquipe
        self.equipe = [joueur(self, jeu, nEquipe, positions[
                              i], prop[i], i) for i in range(6)]
        self.tutoriel = 1
        self.interception = False

    def optionJeu(self):
        if (self.tutoriel == 1):
            print("Pour passer la balle, entrez 0")
            print("\n Pour vous déplacer, entrez 1")
            print("\n Pour finir votre tour, entrez -1")
            print("\n \n Voulez-vous désactiver le tutoriel?")
            print("\n Si oui, tapez 0. Sinon, tapez 1")
            #activer_tutoriel=intInput("Tutoriel :")
            # self.tutoriel=activer_tutoriel
            self.tutoriel = 0
            if (self.tutoriel == 0):
                log.debug("tutoriel désactivé")

    def regleDeplacement(self):
        if (self.tutoriel == 1):
            print("RAPPEL DES REGLES DE PASSE")
            print("Vous pouvez faire autant de passes que vous voulez")
            print(
                "\n Vous ne pouvez passer la balle qu'à un joueur à l'arrière du porteur")
            print("\n Le receveur doit être positionné à 1 ou 2 cases de distance sur une ligne droite orthogonale ou diagonale")
            print("\n Attention, si un joueur adverse est sur la trajectoire de la balle, il risque de l'intercepter")
            print("\n \n Voulez-vous désactiver le tutoriel?")
            print("\n Si oui, tapez 0. Sinon, tapez 1")
            activer_tutoriel = intInput("Tutoriel :")
            self.tutoriel = activer_tutoriel
            if (activer_tutoriel == 0):
                log.info("tutoriel désactivé")

    def reglePasse(self):
        if (self.tutoriel == 1):
            print("RAPPEL DES REGLES DE PASSE")
            print("\n Vous ne pouvez pas déplacer plus de 2 joueurs différents par tour")
            print(
                "\n Toutefois, vous pouvez utiliser vos déplacements dans l'ordre que vous voulez")
            print("Vous ne pouvez pas courir sur un autre joueur à moins qu'il ne soit KO ou que vous forciez le passage")
            print(
                "\n Rappel : les joueurs ordinaires (joueur 0 et 1) peuvent se déplacer de 3 cases par tour")
            print(
                "\n Rappel : le gros costaud (joueur 2) peut se déplacer de 2 cases par tour")
            print("\n Rappel : le dur (joueur 3) peut se déplacer de 3 cases par tour")
            print("\n Rappel : le rapide (joueur 4) peut se déplacer de 4 cases par tour")
            print("\n Rappel : le futé (joueur 5) peut se déplacer de 3 cases par tour")
            print("\n Attention, si un joueur adverse est sur la trajectoire de la balle, il risque de l'intercepter")
            print("\n \n Voulez-vous désactiver le tutoriel?")
            print("\n Si oui, tapez 0. Sinon, tapez 1")
            activer_tutoriel = intInput("Tutoriel :")
            self.tutoriel = activer_tutoriel
            if (activer_tutoriel == 0):
                log.info("tutoriel désactivé")

    def possibilitesDeplacement(self):
        if (self.coupRestant == 2):
            print("Vous pouvez encore déplacer 2 nouveaux joueurs ce tour")
            print("\n Rappel : le premier joueur ordinaire (numéro 0) peut encore se déplacer de %d cases ",
                  (self.equipe)[0].depRestant)
            print("\n Rappel : le deuxième joueur ordinaire (numéro 0) peut encore se déplacer de %d cases ",
                  (self.equipe)[1].depRestant)
            print("\n Rappel : le gros costaud numéro 0) peut encore se déplacer de %d cases """,
                  (self.equipe)[2].depRestant)
            print("\n Rappel : le dur numéro 0) peut encore se déplacer de %d cases ",
                  (self.equipe)[3].depRestant)
            print("\n Rappel : le rapide numéro 0) peut encore se déplacer de %d cases ",
                  (self.equipe)[4].depRestant)
            print("\n Rappel : le futé numéro 0) peut encore se déplacer de %d cases ",
                  (self.equipe)[5].depRestant)
        elif (self.coupRestant == 1):
            k = 0
            while k < 6:
                if (not (self.equipe[k].depRestant == bonus[self.equipe[k].prop][2])):
                    break
            # KO bien gérés?
            print("Vous pouvez encore déplacer un nouveau joueur ce tour")
            print("\n Le joueur %s de numéro %d s'est déjà déplacé ",
                  (prop[k], k))
            print("Vous pouvez encore déplacer 1 nouveau joueur ce tour")
            print("\n Rappel : le premier joueur ordinaire (numéro 0) peut encore se déplacer de %d cases ",
                  (self.equipe)[0].depRestant)
            print("\n Rappel : le premier joueur ordinaire (numéro 1) peut encore se déplacer de %d cases ",
                  (self.equipe)[1].depRestant)
            print("\n Rappel : le gros costaud (numéro 2) peut encore se déplacer de %d cases """,
                  (self.equipe)[2].depRestant)
            print("\n Rappel : le dur (numéro 3) peut encore se déplacer de %d cases ",
                  (self.equipe)[3].depRestant)
            print("\n Rappel : le rapide (numéro 4) peut encore se déplacer de %d cases ",
                  (self.equipe)[4].depRestant)
            print("\n Rappel : le futé (numéro 5) peut encore se déplacer de %d cases ",
                  (self.equipe)[5].depRestant)
        else:
            k1 = 0
            k2 = 0
            i = 0
            while k2 < 6:
                if ((not (self.equipe[k2].depRestant == bonus[self.equipe[k2].prop][2])) and (i == 0)):
                    k1 = k2
                    i += 1
                elif ((not (self.equipe[k2].depRestant == bonus[self.equipe[k2].prop][2])) and (i == 1)):
                    break
            # KO bien gérés?
            print("Vous ne pouvez plus déplacer de nouveau joueur ce tour")
            print("\n Le joueur %s de numéro %d peut encore se déplacer de d  ",
                  (prop[k1], k1, self.equipe[k1].depRestant))
            print("\n Le joueur %s de numéro %d peut encore se déplacer de d  ",
                  (prop[k2], k2, self.equipe[k2].depRestant))
            print("\n Rappel : le joueur %s (numéro %d) peut encore se déplacer de %d cases ",
                  (self.equipe)[0].depRestant)

    def reglePlaquage(self):
        if (self.tutoriel == 1):
            print("RAPPEL DES REGLES DE PLAQUAGE")
            print("\n Vous devez être à côté d'un joueur pour le plaquer")
            print(
                "\n Toutefois, vous pouvez utiliser vos déplacements dans l'ordre que vous voulez")
            print("Vous ne pouvez pas courir sur un autre joueur à moins qu'il ne soit KO ou que vous forciez le passage")
            print(
                "\n Rappel : les joueurs ordinaires (joueur 0 et 1) peuvent se déplacer de 3 cases par tour")
            print(
                "\n Rappel : le gros costaud (joueur 2) peut se déplacer de 2 cases par tour")
            print("\n Rappel : le dur (joueur 3) peut se déplacer de 3 cases par tour")
            print("\n Rappel : le rapide (joueur 4) peut se déplacer de 4 cases par tour")
            print("\n Rappel : le futé (joueur 5) peut se déplacer de 3 cases par tour")
            print("\n Attention, si un joueur adverse est sur la trajectoire de la balle, il risque de l'intercepter")
            print("\n \n Voulez-vous désactiver le tutoriel?")
            print("\n Si oui, tapez 0. Sinon, tapez 1")
            #activer_tutoriel=intInput("Tutoriel :")
            # self.tutoriel=activer_tutoriel
            self.tutoriel = 0
            if (self.tutoriel == 0):
                log.info("tutoriel désactivé")

    def joue(self, interception=False):
        # Reinitialisation
        log.debug("L'équipe %d joue un tour", self.nEquipe)
        self.coupRestant = 2
        for joueur in self.equipe:
            joueur.depRestant = bonus[joueur.prop][2]
        cont = True
        while cont:
            self.optionJeu()
            opt = intInput("Action: ")
            if opt == 0:
                self.reglePasse()
                j1 = intInput("Joueur 1: ")
                while True:
                    try:
                        j2 = intInput("Joueur 2: ")
                        assert j2 != j1
                        self.equipe[j1].passe(self.equipe[j2])
                        break
                    except:
                        pass
            elif opt == 1:
                self.regleDeplacement()
                self.possibilitesDeplacement()
                j = intInput("Joueur qui passe: ")
                posx = intInput("posx: ")
                posy = intInput("posy: ")
                self.equipe[j].deplacement((posx, posy))
                if self.equipe[j].pos[0] == 0 or self.equipe[j].pos[0] == 12:
                    cont = True
                    self.score += 1
                    self.jeu.fin()
                    break
            elif opt == 2:
                self.reglePlaquage()
                j1 = intInput("Joueur qui plaque:")
                j2 = intInput("Joueur plaqué")
                self.equipe[j1].placage(self.equipe[j2], 1)
            elif opt == -1:
                if self.jeu.finTour():
                    cont = False
                else:
                    print("Des joueurs se superposent")
        self.jeu.changeTour()

    def forme(self):
        log.debug("Calcul de la forme de l'équipe %d", self.nEquipe)
        if self.carte == [False for i in range(6)]:
            log.debug(
                "Toutes les cartes de l'équipe %d ont été utilisées", self.nEquipe)
            self.carte = [True for i in range(6)]
        cartePossible = []
        for i in range(len(self.carte)):
            if self.carte[i]:
                cartePossible.append(i)
        e = random.randint(0, len(cartePossible) - 1)
        log.debug(
            "Toutes les cartes de l'équipe %d ont été utilisées", self.nEquipe)
        self.carte[cartePossible[e]] = False
        return cartePossible[e] + 1

if __name__ == "__main__":
    jeu = jeu()
    print("Fin du jeu")
