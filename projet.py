#!/usr/bin/python
# -*- coding: latin-1 -*-
import random
import globalQueue
import fakeNone
import logging
import logging.config
import copy
import os

logging.config.fileConfig("log.conf")
log = logging.getLogger("application")
nbColonne = 13
nbLigne = 8
prop = ["ordinaire", "ordinaire", "dur", "costaud", "fute", "rapide"]
# propri�t� ,( bonus attaque , bonus d�fense, d�placement)
bonus = {'ordinaire': (0, 0, 3), 'dur': (1, 0, 3), 'costaud': (
    2, 1, 2), 'fute': (0, 1, 3), 'rapide': (-1, -1, 4)}


def add(p1, p2):
    return(p1[0] + p2[0], p1[1] + p2[1])


def sub(p1, p2):
    return(p1[0] - p2[0], p1[1] - p2[1])


def absol(point):
    return (abs(point[0]), abs(point[1]))


def droite(point1, point2):
    log.debug("droite({0},{1})".format(point1, point2))
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
    log.debug("Saisie de l'entier {0}".format(strarg))
    while True:
        try:
            num1 = int(input(strarg))
        except ValueError as e:
            print("Vous devez saisir un nombre")
            log.error("Nombre {0} invalide".format(strarg))
            continue
        else:
            break
    return num1


def choixPos(nEquipe):
    log.info("Choix de l'�quipe {0} ...".format(nEquipe))
    if not (nEquipe == 2 or nEquipe == 1):
        log.error("Equipe {0} impossible".format(nEquipe))
        assert nEquipe == 2 or nEquipe == 1
    positions = []
    k = 0
    while k < 6:
        print("\n")
        # print "Joueur " , (k+1) , prop[k] , "..."
        posx = intInput("x: ")
        posy = intInput("y: ")
        log.debug("Un joueur {0} est choisi sur ({1},{2})".format(
            prop[k], posx, posy))
        if (nEquipe == 1):
            if (posx >= 1 and posx <= 2 and posy >= 0 and posy < 8):
                if not (posx, posy) in positions:
                    k += 1
                    positions.append((posx, posy))
                    log.debug("Append de ({0},{1})".format(posx, posy))
                else:
                    print("Veuillez r�essayer : la position choisie est d�j� occup�e.")
                    log.warning(
                        "Position ({0},{1}) d�j� occup�e".format(posx, posy))
            else:
                print(
                    "Veuillez r�essayer : la position choisie est hors limite. Il faut que 1=<x<=2 et 0<=y<=7")
                log.warning("({0},{1}) est hors limite".format(posx, posy))
        else:
            if (posx >= 10 and posx <= 11 and posy >= 0 and posy < 8):
                if not (posx, posy) in positions:
                    k += 1
                    positions.append((posx, posy))
                    log.info("Append de ({0},{1})".format(posx, posy))
                else:
                    print("Veuillez r�essayer : la position choisie est d�j� occup�e.")
                    log.warning(
                        "Position ({0},{1}) d�j� occup�e".format(posx, posy))
            else:
                print(
                    "Veuillez r�essayer : la position choisie est hors limite. Il faut que 1=<x<=2 et que 0<=y<=7")
                log.warning("({0},{1}) est hors limite".format(posx, posy))
    return positions


class jeu:

    def __init__(self):
        log.info("Cr�ation du jeu")
        self.matrice = [[0 for i in range(nbLigne)] for j in range(nbColonne)]
        for i in range(nbLigne):
            for j in range(nbColonne):
                joueur(None, self, 3, (j, i), "", 0)
        os.system('clear')
        # TODO :Mettre ce texte dans une fonction printIntro
        print("****************************************** Kahmat� ******************************************")
        print("Auteurs : Valentin B., Quentin B., Fran�ois D (2015) ")
        print("\nLe Kahmat� se joue � deux joueurs, amusez-vous bien !")
        print("Voir r�gle du jeu sur : http://jeuxstrategie1.free.fr/jeu_kahmate/regle.pdf")
        print("\n")
        print("Instructions: ")
        print("* Suivre les instructions de la console")
        print("* Pour arr�ter la partie : CTRL+D ")  # TODO : � impl�menter
        print("**********************************************************************************************")
        print("\nChoix de la position des joueurs de l'�quipe 1")
        positions1 = choixPos(1)
        print("\nChoix de la position des joueurs de l'�quipe 2")
        positions2 = choixPos(2)
        self.equipe1 = equipe(self, 1, positions1)
        self.equipe2 = equipe(self, 2, positions2)
        self.ballon = ballon((6, random.randint(1, 6)), self)
        self.tour = 1
        globalQueue.queue.put(self)

    def changeTour(self):
        log.info("D�but des tours de jeu")
        if self.tour == 2:
            log.info("Tour de jeu �quipe 1")
            self.tour = 1
            self.equipe1.joue()
        else:
            log.info("Tour de jeu �quipe 2")
            self.tour = 2
            self.equipe2.joue()

    def resolution(self, attaquant, defenseur):
        log.info("R�solution attaquant{0}/�quipe {1} - d�fenseur {2}/�quipe {3}".format(
            attaquant.numero, attaquant.nEquipe, defenseur.numero, defenseur.nEquipe))
        vAtt = bonus[attaquant.prop][0] + attaquant.equipe.forme()
        vDef = bonus[defenseur.prop][1] + defenseur.equipe.forme()
        print("\nAttaquant : {0},D�fenseur : {1}".format(vAtt, vDef))
        if vAtt > vDef:
            print("Victoire de l'attaquant par {0}".format(vAtt - vDef))
        elif vDef > vAtt:
            print("Victoire du d�fenseur par {0}".format(vDef - vAtt))
        else:
            print("Egalit�, on tire une nouvelle carte forme")
            vAtt = bonus[attaquant.prop][0] + attaquant.equipe.forme()
            vDef = bonus[defenseur.prop][1] + defenseur.equipe.forme()
            if vAtt > vDef:
                print("Victoire de l'attaquant par {0}".format(vAtt - vDef))
            else:
                print("Victoire du d�fenseur par {0}".format(vDef - vAtt))
        log.debug("R�sultat : {0}".format(vAtt - vDef))
        return vAtt - vDef

    def libre(self, pos, depRestant=0):
        log.debug("Test Libre de la position ({0},{1})".format(pos[0], pos[1]))
        assert(pos[0] >= 0 and pos[0] < nbColonne and pos[
               1] >= 0 and pos[1] < nbLigne)
        isLibre = (self.matrice[pos[0]][pos[1]][-1].nEquipe ==
                   3 or (self.matrice[pos[0]][pos[1]][-1].ko and depRestant >= 2))
        log.debug("R�sultat : {0}".format(isLibre))
        return isLibre

    def interception(self, joueur1, joueur2):
        pos1 = joueur1.pos
        pos2 = joueur2.pos
        log.info("Interception entre ({0},{1}) et ({2},{3})".format(
            pos1[0], pos1[1], pos2[0], pos2[1]))
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
                        "Interception par l'�quipe 1 du joueur {0}".format(joueur.numero))
        else:
            for joueur in self.equipe1.equipe:
                if ((calcPosDroite(r1, joueur.pos) * calcPosDroite(r2, joueur.pos) < 0 or
                     calcPosDroite(v1, joueur.pos) * calcPosDroite(v2, joueur.pos) < 0)
                    and (calcPosDroite(d1, joueur.pos) * calcPosDroite(d2, joueur.pos) < 0 or
                         calcPosDroite(c1, joueur.pos) * calcPosDroite(c2, joueur.pos) < 0)):
                    inter.append(joueur)
                    log.debug(
                        "Interception par l'�quipe 2 du joueur {0}".format(joueur.numero))
        return inter

    def fin(self):
        print("Vous avez gagn�")


class ballon:

    def __init__(self, position, jeu):
        log.debug("Initialisation du ballon � la position ({0},{1})".format(
            position[0], position[1]))
        self.position = position
        self.jeu = jeu
        self.porteur = self.jeu.matrice[position[0]][position[1]][-1]

    def deplacement(self):
        if self.porteur.nEquipe != 3:
            self.position = self.porteur.pos
            log.debug("Le ballon se deplace � la postion ({0},{1})".format(
                self.position[0], self.position[1]))


class joueur:

    def __init__(self, equipe, jeu, nEquipe, position, prop, numero):
        log.debug("Initialisation du joueur {0} de l'�quipe {1}".format(
            numero, nEquipe))
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
        log.debug("Le joueur {0} se d�place � ({1},{2})".format(
            self.numero, pos[0], pos[1]))
        # Cas o� on va sur une case o� il y a un joueur ko
        if self.jeu.matrice[pos[0]][pos[1]][0].ko and not self.jeu.matrice[self.pos[0]][self.pos[1]][0].ko:
            self.jeu.matrice[pos[0]][pos[1]].append(self)
            self.jeu.matrice[self.pos[0]][self.pos[1]][0] = joueur(
                None, self.jeu, 3, self.pos, "", 0)  # joueur de l'�quipe 3 pour compl�ter
        # Cas o� on part d'une case o� il y a un joueur ko
        elif self.jeu.matrice[self.pos[0]][self.pos[1]][0].ko and not self.jeu.matrice[pos[0]][pos[1]][0].ko:
            self.jeu.matrice[pos[0]][pos[1]][0] = self
            self.jeu.matrice[self.pos[0]][self.pos[1]].remove(self)
        # Cas o� on part d'une case o� un joueur est ko pour arriver � une case
        # o� un autre joueur est ko
        elif self.jeu.matrice[self.pos[0]][self.pos[1]][0].ko and self.jeu.matrice[pos[0]][pos[1]][0].ko:
            self.jeu.matrice[pos[0]][pos[1]].append(self)
            self.jeu.matrice[self.pos[0]][self.pos[1]].remove(self)
        else:  # Cas o� les joueurs ko ne sont pas impliqu�s
            self.jeu.matrice[pos[0]][pos[1]][0] = self
            self.jeu.matrice[self.pos[0]][self.pos[1]][
                0] = joueur(None, self.jeu, 3, self.pos, "", 0)
        self.depRestant -= 1
        self.pos = pos

    def deplacement(self, pos):
        log.info("D�placement du joueur {0}".format(self.numero))
        # pas par pas c'est plus simple
        # le joueur ne doit pas �tre KO et le d�placement doit �tre
        # d'au plus 1
        if not self.ko:
            if self.depRestant > 0 and sum(absol(sub(self.pos, pos))) == 1 and self.jeu.libre(pos, self.depRestant) and self.onGrid(pos):
                if self.depRestant == bonus[self.prop][2]:
                    # Le joueur ne s'est pas encore d�plac�
                    if self.equipe.coupRestant > 0:
                        self.equipe.coupRestant -= 1
                        self.deplace(pos)
                        if self.jeu.ballon.position == pos:
                            self.porteur = True
                            self.jeu.ballon.porteur = self
                    else:
                        log.error(
                            "Vous ne pouvez pas d�placer plus de joueurs")
                else:
                    self.deplace(pos)
                    if self.jeu.ballon.position == pos:
                        self.porteur = True
                        self.jeu.ballon.porteur = self
            if self.porteur:
                log.info("Le joueur est porteur, le ballon doit aussi se d�placer")
                self.jeu.ballon.deplacement()
            else:
                log.error(
                    "Le joueur doit �tre libre et se d�placer d'une seule valeur")
        else:
            log.error("Le joueur ne doit pas �tre KO")
        globalQueue.queue.put(self.jeu)

    def onGrid(self, pos):
        log.debug("Test si la postion du joueur est bonne")
        posx = pos[0]
        posy = pos[1]
        if self.nEquipe == 2:
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
        log.debug("Test si le joueur 2 est derri�re joueur 1")
        # joueur2 est il derri�re joueur 1?
        if self.nEquipe == 1:
            return (self.pos[0] - joueur2.pos[0]) > 0 and max(absol(sub(self.pos, joueur2.pos))) <= 2
        else:
            return (self.pos[0] - joueur2.pos[0]) < 0 and max(absol(sub(self.pos, joueur2.pos))) <= 2

    def askIntercepter(self, joueur1, joueur2):
        log.info("Demande au joueur adverse l'interception")
        print("Au joueur de l'�quipe {0}".format(joueur1.nEquipe))
        print("Voulez-vous intercepter le lancer du joueur adverse {0} de coordonn�es ({1},{2}) au joueur adverse {3} de coordonn�es ({4},{5})".format(
            prop[joueur1.numero], joueur1.pos[1], joueur1.pos[0], prop[joueur2.numero], joueur2.pos[1], joueur2.pos[0]))
        print("\n , avec votre joueur {0} de coordonn�es de coordonn�es ({1},{2})".format(
            prop[self.numero], self.pos[1], self.pos[0]))
        print("\n")
        print("Si oui, tapez 1. Sinon tapez 0")
        intercepte = intInput("Interception: ")
        if (intercepte == 1):
            return True
        else:
            return False

    def passe(self, joueur2):
        log.info("Le joueur {0} essaie de passer au joueur {1}".format(
            self.numero, joueur2.numero))
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
                        log.info("La passe est r�ussie")
            else:
                log.error("La passe est impossible car le joueur {0} n'est pas derri�re".format(
                    self.numero))
        else:
            log.error("La passe est impossible car le joueur {0} n'est pas porteur".format(
                self.numero))
        globalQueue.queue.put(self.jeu)

    def placage(self, joueur2, plaquer=True):
        log.info("Le joueur {0} essaie de plaquer le joueur {1}".format(
            self.numero, joueur2.numero))
        if sum(absol(sub(self.pos, joueur2.pos))) == 1 and (plaquer or self.depRestant > 1):
            if joueur2.nEquipe != 3 and joueur2.nEquipe != self.nEquipe and not joueur2.ko and ((self.porteur and not(plaquer)) or (joueur2.porteur and plaquer)):
                resolution = self.jeu.resolution(self, joueur2)
                if resolution > 0:
                    if resolution >= 2 and plaquer:
                        log.debug("Plaquage parfait")
                        self.porteur = True
                        self.jeu.ballon.porteur = self
                        self.jeu.ballon.deplacement()
                    else:
                        log.debug("Plaquage classique ou passage en force")
                        if joueur2.pos[0] > self.pos[0]:
                            log.debug("Joueur plaqu� � gauche du plaqueur")
                            if joueur2.pos[0] < nbColonne - 2:
                                self.jeu.ballon.position = add(
                                    self.jeu.ballon.position, (1, 0))
                            else:
                                log.debug("Joueur2 est sur le bord droit")
                                if joueur2.pos[1] < nbLigne / 2:
                                    self.jeu.ballon.position = add(
                                        self.jeu.ballon.position, (0, 1))
                                else:
                                    self.jeu.ballon.position = add(
                                        self.jeu.ballon.position, (0, -1))
                        elif joueur2.pos[0] < self.pos[0]:
                            log.debug("Joueur plaqu� � droite du plaqueur")
                            if joueur2.pos[0] > 1:
                                self.jeu.ballon.position = add(
                                    self.jeu.ballon.position, (-1, 0))
                            else:
                                log.debug(
                                    "Cas particulier o� le joueur plaqu� est sur le bord gauche")
                                if joueur2.pos[1] < nbLigne / 2:
                                    self.jeu.ballon.position = add(
                                        self.jeu.ballon.position, (0, 1))
                                else:
                                    self.jeu.ballon.position = add(
                                        self.jeu.ballon.position, (0, -1))
                        else:
                            if joueur2.pos[1] < self.pos[1]:
                                log.debug(
                                    "Joueur plaqu� au dessus du plaqueur")
                                if joueur2.pos[1] > 0:
                                    self.jeu.ballon.position = add(
                                        self.jeu.ballon.position, (0, -1))
                                else:
                                    log.debug(
                                        "Le joueur plaqu� est tout en haut")
                                    if joueur2.pos[0] < nbColonne / 2:
                                        self.jeu.ballon.position = add(
                                            self.jeu.ballon.position, (1, 0))
                                    else:
                                        self.jeu.ballon.position = add(
                                            self.jeu.ballon.position, (-1, 0))
                            else:
                                log.debug(
                                    "Joueur plaqu� en dessous du plaqueur")
                                if joueur2.pos[1] < nbLigne - 1:
                                    self.jeu.ballon.position = add(
                                        self.jeu.ballon.position, (0, 1))
                                else:
                                    log.debug(
                                        "Le joueur plaqu� est tout en bas")
                                    if joueur2.pos[0] < nbColonne / 2:
                                        self.jeu.ballon.position = add(
                                            self.jeu.ballon.position, (1, 0))
                                    else:
                                        self.jeu.ballon.position = add(
                                            self.jeu.ballon.position, (-1, 0))
                        log.debug(
                            "Un joueur sur la case du ballon qui le r�cup�re")
                        self.jeu.ballon.porteur = self.jeu.matrice[
                            self.jeu.ballon.position[0]][self.jeu.ballon.position[1]][-1]
                        if self.jeu.ballon.porteur.nEquipe != 3:
                            self.jeu.ballon.porteur.porteur = True
                    joueur2.ko = True
                    joueur2.porteur = False
                    if plaquer:
                        self.depRestant = 0
                    else:
                        self.deplacement(joueur2.pos)
                        self.depRestant -= 1
                else:
                    self.ko = True
        globalQueue.queue.put(self.jeu)

    def nobodyFront(self):
        log.debug("Test personne en face")
        if self.nEquipe == 1:
            for joueur in self.equipe.equipe:
                if joueur.pos[0] > self.pos[0]:
                    #log.debug("R�sultat : Faux")
                    return False
            log.debug("R�sultat : Vrai")
            return True
        else:
            for joueur in self.equipe.equipe:
                if joueur.pos[0] < self.pos[0]:
                    log.debug("R�sultat : faux")
                    return False
            log.debug("R�sultat : Vrai")
            return True

    def front(self, pos):
        log.debug("Test endroit o� on envoie le ballon")
        if self.nEquipe == 1:
            return pos[0] - self.pos[0] > 0 and pos[0] - self.pos[0] <= 3
        else:
            return pos[0] - self.pos[0] < 0 and -pos[0] + self.pos[0] <= 3

    def tirAvant(self, pos):
        log.info("Le joueur {0} essaie de tirer en avant".format(self.numero))
        if self.porteur:
            if self.nobodyFront() and self.front(pos):
                self.porteur = False
                self.jeu.ballon.position = pos
                self.jeu.ballon.porteur = self.jeu.matrice[pos[0]][pos[1]][-1]
                self.jeu.matrice[pos[0]][pos[1]][-1].porteur = True
            elif (not self.nobodyFront(pos)):
                log.error("Le tir en avant est impossible car le joueur {0} a un joueur devant lui".format(
                    self.numero))
            elif (not self.front(pos)):
                log.error(
                    "La case choisie n'est pas en avant du joueur {0}".format(self.numero))
                print("case non remplie")
            else:
                print("case non vide")
        globalQueue.queue.put(self.jeu)


class equipe:

    def __init__(self, jeu, nEquipe, positions):
        log.debug("Initialisation de l'�quipe {0}".format(nEquipe))
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
            print("\n Pour vous d�placer, entrez 1")
            print("\n Pour finir votre tour, entrez -1")
            print("\n \n Voulez-vous d�sactiver le tutoriel?")
            print("\n Si oui, tapez 0. Sinon, tapez 1")
            #activer_tutoriel=intInput("Tutoriel :")
            # self.tutoriel=activer_tutoriel
            self.tutoriel = 0
            if (self.tutoriel == 0):
                log.debug("Tutoriel d�sactiv�")

    def reglePasse(self):
        if (self.tutoriel == 1):
            print("RAPPEL DES REGLES DE PASSE")
            print("Vous pouvez faire autant de passes que vous voulez")
            print(
                "\n Vous ne pouvez passer la balle qu'� un joueur � l'arri�re du porteur")
            print("\n Le receveur doit �tre positionn� � 1 ou 2 cases de distance sur une ligne droite orthogonale ou diagonale")
            print("\n Attention, si un joueur adverse est sur la trajectoire de la balle, il risque de l'intercepter")
            print("\n \n Voulez-vous d�sactiver le tutoriel?")
            print("\n Si oui, tapez 0. Sinon, tapez 1")
            activer_tutoriel = intInput("Tutoriel :")
            self.tutoriel = activer_tutoriel
            if (activer_tutoriel == 0):
                log.info("Tutoriel d�sactiv�")

    def regleDeplacement(self):
        if (self.tutoriel == 1):
            print("RAPPEL DES REGLES DE PASSE")
            print("\n Vous ne pouvez pas d�placer plus de 2 joueurs diff�rents par tour")
            print(
                "\n Toutefois, vous pouvez utiliser vos d�placements dans l'ordre que vous voulez")
            print("Vous ne pouvez pas courir sur un autre joueur � moins qu'il ne soit KO ou que vous forciez le passage")
            print(
                "\n Rappel : les joueurs ordinaires (joueur 0 et 1) peuvent se d�placer de 3 cases par tour")
            print(
                "\n Rappel : le gros costaud (joueur 2) peut se d�placer de 2 cases par tour")
            print("\n Rappel : le dur (joueur 3) peut se d�placer de 3 cases par tour")
            print("\n Rappel : le rapide (joueur 4) peut se d�placer de 4 cases par tour")
            print("\n Rappel : le fut� (joueur 5) peut se d�placer de 3 cases par tour")
            print("\n Attention, si un joueur adverse est sur la trajectoire de la balle, il risque de l'intercepter")
            print("\n \n Voulez-vous d�sactiver le tutoriel?")
            print("\n Si oui, tapez 0. Sinon, tapez 1")
            activer_tutoriel = intInput("Tutoriel :")
            self.tutoriel = activer_tutoriel
            if (activer_tutoriel == 0):
                log.info("tutoriel d�sactiv�")

    def possibilitesDeplacement(self):
        if (self.coupRestant == 2):
            print("Vous pouvez encore d�placer 2 nouveaux joueurs ce tour")
            print("\n Rappel : le premier joueur ordinaire (num�ro 0) peut encore se d�placer de {0} cases ".format(
                (self.equipe)[0].depRestant))
            print("\n Rappel : le deuxi�me joueur ordinaire (num�ro 1) peut encore se d�placer de {0} cases ".format(
                (self.equipe)[1].depRestant))
            print("\n Rappel : le gros costaud (num�ro 2) peut encore se d�placer de {0} cases".format(
                (self.equipe)[2].depRestant))
            print("\n Rappel : le dur (num�ro 3) peut encore se d�placer de {0} cases ".format(
                (self.equipe)[3].depRestant))
            print("\n Rappel : le rapide (num�ro 4) peut encore se d�placer de {0} cases ".format(
                (self.equipe)[4].depRestant))
            print("\n Rappel : le fut� (num�ro 5) peut encore se d�placer de {0} cases ".format(
                (self.equipe)[5].depRestant))
        elif (self.coupRestant == 1):
            k = 0
            while k < 6:
                if (not (self.equipe[k].depRestant == bonus[self.equipe[k].prop][2])):
                    break
            # KO bien g�r�s?
            print("Vous pouvez encore d�placer un nouveau joueur ce tour")
            print(
                "\n Le joueur {0} de num�ro {1} s'est d�j� d�plac� ".format(prop[k], k))
            print("Vous pouvez encore d�placer 1 nouveau joueur ce tour")
            print("\n Rappel : le premier joueur ordinaire (num�ro 0) peut encore se d�placer de {0} cases ".format(
                (self.equipe)[0].depRestant))
            print("\n Rappel : le premier joueur ordinaire (num�ro 1) peut encore se d�placer de {0} cases ".format(
                (self.equipe)[1].depRestant))
            print("\n Rappel : le gros costaud (num�ro 2) peut encore se d�placer de {0} cases ".format(
                (self.equipe)[2].depRestant))
            print("\n Rappel : le dur (num�ro 3) peut encore se d�placer de {0} cases".format(
                (self.equipe)[3].depRestant))
            print("\n Rappel : le rapide (num�ro 4) peut encore se d�placer de {0} cases ".format(
                (self.equipe)[4].depRestant))
            print("\n Rappel : le fut� (num�ro 5) peut encore se d�placer de {0} cases ".format(
                (self.equipe)[5].depRestant))
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
            # KO bien g�r�s?
            print("Vous ne pouvez plus d�placer de nouveau joueur ce tour")
            print("\n Le joueur {0} de num�ro {1} peut encore se d�placer de {2}".format(
                prop[k1], k1, self.equipe[k1].depRestant))
            print("\n Le joueur {0} de num�ro {1} peut encore se d�placer de {2}".format(
                (prop[k2], k2, self.equipe[k2].depRestant)))
            print("\n Rappel : le joueur {0} (num�ro {1}) peut encore se d�placer de {2} cases ".format(
                (self.equipe)[0].depRestant))

    def reglePlaquage(self):
        if (self.tutoriel == 1):
            print("RAPPEL DES REGLES DE PLAQUAGE")
            print("\n Vous devez �tre � c�t� d'un joueur pour le plaquer")
            print(
                "\n Toutefois, vous pouvez utiliser vos d�placements dans l'ordre que vous voulez")
            print("Vous ne pouvez pas courir sur un autre joueur � moins qu'il ne soit KO ou que vous forciez le passage")
            print(
                "\n Rappel : les joueurs ordinaires (joueur 0 et 1) peuvent se d�placer de 3 cases par tour")
            print(
                "\n Rappel : le gros costaud (joueur 2) peut se d�placer de 2 cases par tour")
            print("\n Rappel : le dur (joueur 3) peut se d�placer de 3 cases par tour")
            print("\n Rappel : le rapide (joueur 4) peut se d�placer de 4 cases par tour")
            print("\n Rappel : le fut� (joueur 5) peut se d�placer de 3 cases par tour")
            print("\n Attention, si un joueur adverse est sur la trajectoire de la balle, il risque de l'intercepter")
            print("\n \n Voulez-vous d�sactiver le tutoriel?")
            print("\n Si oui, tapez 0. Sinon, tapez 1")
            activer_tutoriel = intInput("Tutoriel :")
            self.tutoriel = activer_tutoriel
            if (self.tutoriel == 0):
                log.info("Tutoriel d�sactiv�")

    def joue(self, interception=False):
        # Reinitialisation
        log.debug("L'�quipe {0} joue un tour".format(self.nEquipe))
        self.coupRestant = 2
        for joueur in self.equipe:
            joueur.depRestant = bonus[joueur.prop][2]
        cont = True
        while cont:
            globalQueue.waitInput = True
            args = globalQueue.queueAction.get()
            globalQueue.waitInput = False
            if args[0] == "passe":
                self.reglePasse()
                # v�rifier l'quipe qui jue?
                self.equipe[args[1]].passe(self.equipe[args[2]])
            elif args[0] == "deplace":
                pos1 = args[1]
                pos2 = args[2]
                j1 = self.jeu.matrice[pos1[0]][pos1[1]][-1]
                if j1.nEquipe == self.nEquipe:
                    j1.deplacement(pos2)
                    if j1.pos[0] == 0 or j1.pos[0] == 12:
                        cont = True
                        self.score += 1
                        self.jeu.fin()
                        break
            elif args[0] == "placage":
                self.reglePlaquage()
                j1 = intInput("Joueur qui plaque:")
                j2 = intInput("Joueur plaqu�:")
                self.equipe[j1].placage(self.jeu.equipe2.equipe[j2])
            elif args[0] == "passage":
                self.regleForcerPassage()
                j1 = intInput("Joueur qui force le passage:")
                j2 = intInput("Joueur en face:")
                self.equipe2.equipe[j2].placage(self.equipe[j1], False)
            elif args[0] == "fin":
                if self.finTour():
                    cont = False
                else:
                    print("Des joueurs se superposent")
        if not cont:
            self.jeu.changeTour()

    def forme(self):
        log.debug("Calcul de la forme de l'�quipe {0}".format(self.nEquipe))
        if self.carte == [False for i in range(6)]:
            log.debug(
                "Toutes les cartes de l'�quipe {0} ont �t� utilis�es".format(self.nEquipe))
            self.carte = [True for i in range(6)]
        cartePossible = []
        for i in range(len(self.carte)):
            if self.carte[i]:
                cartePossible.append(i)
        e = random.randint(0, len(cartePossible) - 1)
        log.debug("La carte {0} de l'�quipe {1} a �t� utilis�e ".format(
            e, self.nEquipe))
        self.carte[cartePossible[e]] = False
        return cartePossible[e] + 1

    def finTour(self):
        log.debug("Test fin du tour")
        for joueur in self.equipe:
            if len(self.jeu.matrice[joueur.pos[0]][joueur.pos[1]]) != 1:
                log.debug("Le tour n'est pas fini")
                return False
        log.debug("Le tour est fini")
        return True

if __name__ == "__main__":
    jeu = jeu()
    print("Fin du jeu")
