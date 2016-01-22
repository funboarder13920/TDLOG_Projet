import random
import globalQueue
import logging
import logging.config
import copy
import os

logging.config.fileConfig("log.conf")
log = logging.getLogger("application")
log.propagate = False
nbColonne = 13
nbLigne = 8
prop = ["ordinaire", "ordinaire", "dur", "costaud", "fute", "rapide"]
# propriété ,( bonus attaque , bonus défense, déplacement)
bonus = {"ordinaire": (0, 0, 3), "dur": (1, 0, 3), "costaud": (
    2, 1, 2), "fute": (0, 1, 3), "rapide": (-1, -1, 4)}


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


def inRangeGrid(pos):
    return (pos[0] >= 0 and pos[0] <= 12 and pos[1] >= 0 and pos[1] < 8)


def choixPos(nEquipe):
    log.info("Choix de l'équipe {0} ...".format(nEquipe))
    globalQueue.waitChoix.put(True)
    positions = globalQueue.sendPosition.get()
    return positions


class jeu:

    def __init__(self):
        log.info("Création du jeu")
        self.matrice = [[0 for i in range(nbLigne)] for j in range(nbColonne)]
        for i in range(nbLigne):
            for j in range(nbColonne):
                joueur(None, self, 3, (j, i), "", 0)
        # TODO :Mettre ce texte dans une fonction printIntro
        print("****************************************** Kahmaté ******************************************")
        print("Auteurs : Valentin B., Quentin B., François D (2015) ")
        print("\nLe Kahmaté se joue à deux joueurs, amusez-vous bien !")
        print("Voir règle du jeu sur : http://jeuxstrategie1.free.fr/jeu_kahmate/regle.pdf")
        print("\n")
        print("Instructions: ")
        print("* Suivre les instructions de la console")
        print("**********************************************************************************************")
        print("\nChoix de la position des joueurs de l'équipe 1")
        positions1 = choixPos(1)
        print("\nChoix de la position des joueurs de l'équipe 2")
        positions2 = choixPos(2)
        self.equipe1 = equipe(self, 1, positions1)
        self.equipe2 = equipe(self, 2, positions2)
        self.ballon = ballon((6, random.randint(1, 6)), self)
        self.tour = random.randint(1,2)
        globalQueue.queue.put(self)
        self.changeTour()

    def changeTour(self):
        log.info("Début des tours de jeu")
        if self.tour == 2:
            log.info("Tour de jeu équipe 1")
            self.tour = 1
            self.equipe1.joue()
        else:
            log.info("Tour de jeu équipe 2")
            self.tour = 2
            self.equipe2.joue()

    def resolution(self, attaquant, defenseur):
        log.info("Résolution attaquant{0}/équipe {1} - défenseur {2}/équipe {3}".format(
            attaquant.numero, attaquant.nEquipe, defenseur.numero, defenseur.nEquipe))
        vAtt = bonus[attaquant.prop][0] + attaquant.equipe.forme()
        vDef = bonus[defenseur.prop][1] + defenseur.equipe.forme()
        print("\nAttaquant : {0},Défenseur : {1}".format(vAtt, vDef))
        if vAtt > vDef:
            print("Victoire de l'attaquant par {0}".format(vAtt - vDef))
        elif vDef > vAtt:
            print("Victoire du défenseur par {0}".format(vDef - vAtt))
        else:
            print("Egalité, on tire une nouvelle carte forme")
            vAtt = bonus[attaquant.prop][0] + attaquant.equipe.forme()
            vDef = bonus[defenseur.prop][1] + defenseur.equipe.forme()
            if vAtt > vDef:
                print("Victoire de l'attaquant par {0}".format(vAtt - vDef))
            else:
                print("Victoire du défenseur par {0}".format(vDef - vAtt))
        log.debug("Résultat : {0}".format(vAtt - vDef))
        return vAtt - vDef

    def libre(self, pos, depRestant=0):
        log.debug("Test Libre de la position ({0},{1})".format(pos[0], pos[1]))
        assert(pos[0] >= 0 and pos[0] < nbColonne and pos[
               1] >= 0 and pos[1] < nbLigne)
        isLibre = (self.matrice[pos[0]][pos[1]][-1].nEquipe ==
                   3 or (self.matrice[pos[0]][pos[1]][-1].ko and depRestant >= 2))
        log.debug("Résultat : {0}".format(isLibre))
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
                if not(joueur.ko):
                    if ((calcPosDroite(r1, joueur.pos) * calcPosDroite(r2, joueur.pos) < 0 or
                         calcPosDroite(v1, joueur.pos) * calcPosDroite(v2, joueur.pos) < 0) and
                        (calcPosDroite(d1, joueur.pos) * calcPosDroite(d2, joueur.pos) < 0 or
                         calcPosDroite(c1, joueur.pos) * calcPosDroite(c2, joueur.pos) < 0)):
                        inter.append(joueur)
                        log.debug(
                            "Interception par l'équipe 1 du joueur {0}".format(joueur.numero))
        else:
            for joueur in self.equipe1.equipe:
                if not(joueur.ko):
                    if ((calcPosDroite(r1, joueur.pos) * calcPosDroite(r2, joueur.pos) < 0 or
                         calcPosDroite(v1, joueur.pos) * calcPosDroite(v2, joueur.pos) < 0)
                        and (calcPosDroite(d1, joueur.pos) * calcPosDroite(d2, joueur.pos) < 0 or
                             calcPosDroite(c1, joueur.pos) * calcPosDroite(c2, joueur.pos) < 0)):
                        inter.append(joueur)
                        log.debug(
                            "Interception par l'équipe 2 du joueur {0}".format(joueur.numero))
        return inter

    def fin(self):
        print("Vous avez gagné")


class ballon:

    def __init__(self, position, jeu):
        log.debug("Initialisation du ballon à la position ({0},{1})".format(
            position[0], position[1]))
        self.position = position
        self.jeu = jeu
        self.porteur = self.jeu.matrice[position[0]][position[1]][-1]

    def deplacement(self):
        if self.porteur.nEquipe != 3:
            self.position = self.porteur.pos
            log.debug("Le ballon se deplace à la postion ({0},{1})".format(
                self.position[0], self.position[1]))


class joueur:

    def __init__(self, equipe, jeu, nEquipe, position, prop, numero):
        log.debug("Initialisation du joueur {0} de l'équipe {1}".format(
            numero, nEquipe))
        self.pos = position
        self.numero = numero
        self.porteur = False
        self.jeu = jeu
        self.ko = False
        self.koCount = -1
        self.equipe = equipe
        self.nEquipe = nEquipe
        self.prop = prop
        self.jeu.matrice[position[0]][position[1]] = [self]
        if nEquipe != 3:
            self.depRestant = bonus[self.prop][2]
        else:
            self.depRestant = 0

    def deplace(self, pos):
        log.debug("Le joueur {0} se déplace à ({1},{2})".format(
            self.numero, pos[0], pos[1]))
        # Cas où on va sur une case où il y a un joueur ko
        if self.jeu.matrice[pos[0]][pos[1]][0].ko and not self.jeu.matrice[self.pos[0]][self.pos[1]][0].ko:
            self.jeu.matrice[pos[0]][pos[1]].append(self)
            self.jeu.matrice[self.pos[0]][self.pos[1]][0] = joueur(
                None, self.jeu, 3, self.pos, "", 0)  # joueur de l'équipe 3 pour compléter
        # Cas où on part d'une case où il y a un joueur ko
        elif self.jeu.matrice[self.pos[0]][self.pos[1]][0].ko and not self.jeu.matrice[pos[0]][pos[1]][0].ko:
            self.jeu.matrice[pos[0]][pos[1]][0] = self
            self.jeu.matrice[self.pos[0]][self.pos[1]].remove(self)
        # Cas où on part d'une case où un joueur est ko pour arriver ù une case
        # où un autre joueur est ko
        elif self.jeu.matrice[self.pos[0]][self.pos[1]][0].ko and self.jeu.matrice[pos[0]][pos[1]][0].ko:
            self.jeu.matrice[pos[0]][pos[1]].append(self)
            self.jeu.matrice[self.pos[0]][self.pos[1]].remove(self)
        else:  # Cas où les joueurs ko ne sont pas impliqués
            self.jeu.matrice[pos[0]][pos[1]][0] = self
            self.jeu.matrice[self.pos[0]][self.pos[1]][
                0] = joueur(None, self.jeu, 3, self.pos, "", 0)
        self.depRestant -= 1
        self.pos = pos

    def deplacement(self, pos):
        log.info("Déplacement du joueur {0}".format(self.numero))
        # pas par pas c'est plus simple
        # le joueur ne doit pas être KO et le déplacement doit être
        # d'au plus 1
        if not self.ko:
            if self.depRestant > 0 and sum(absol(sub(self.pos, pos))) == 1 and self.jeu.libre(pos, self.depRestant) and self.onGrid(pos):
                if self.depRestant == bonus[self.prop][2]:
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
                else:
                    self.deplace(pos)
                    if self.jeu.ballon.position == pos:
                        self.porteur = True
                        self.jeu.ballon.porteur = self
            if self.porteur:
                log.info("Le joueur est porteur, le ballon doit aussi se déplacer")
                self.jeu.ballon.deplacement()
        else:
            log.error("Le joueur ne doit pas être KO")
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
        log.debug("Test si le joueur 2 est derrière joueur 1")
        # joueur2 est il derrière joueur 1?
        if self.nEquipe == 1:
            return (self.pos[0] - joueur2.pos[0]) > 0 and max(absol(sub(self.pos, joueur2.pos))) <= 2
        else:
            return (self.pos[0] - joueur2.pos[0]) < 0 and max(absol(sub(self.pos, joueur2.pos))) <= 2

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
                for adv in interc:
                    globalQueue.interAdv.put(adv)
                    if globalQueue.askInter.get():
                        if self.jeu.resolution(self, adv) <= 0:
                            adv.porteur = True
                            joueur2.porteur = False
                            self.jeu.ballon.porteur = adv
                            self.jeu.ballon.deplacement()
                            break
                    else:
                        log.info("La passe est réussie")
            else:
                log.error("La passe est impossible car le joueur {0} n'est pas derrière".format(
                    self.numero))
        else:
            log.error("La passe est impossible car le joueur {0} n'est pas porteur".format(
                self.numero))
        globalQueue.queue.put(self.jeu)

    def poseballon(self, joueur2):
        log.debug("Plaquage classique ou passage en force")
        if joueur2.pos[0] > self.pos[0]:
            log.debug("Joueur plaqué à gauche du plaqueur")
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
            log.debug("Joueur plaqué à droite du plaqueur")
            if joueur2.pos[0] > 1:
                self.jeu.ballon.position = add(
                    self.jeu.ballon.position, (-1, 0))
            else:
                log.debug(
                    "Cas particulier où le joueur plaqué est sur le bord gauche")
                if joueur2.pos[1] < nbLigne / 2:
                    self.jeu.ballon.position = add(
                        self.jeu.ballon.position, (0, 1))
                else:
                    self.jeu.ballon.position = add(
                        self.jeu.ballon.position, (0, -1))
        else:
            if joueur2.pos[1] < self.pos[1]:
                log.debug(
                    "Joueur plaqué au dessus du plaqueur")
                if joueur2.pos[1] > 0:
                    self.jeu.ballon.position = add(
                        self.jeu.ballon.position, (0, -1))
                else:
                    log.debug(
                        "Le joueur plaqué est tout en haut")
                    if joueur2.pos[0] < nbColonne / 2:
                        self.jeu.ballon.position = add(
                            self.jeu.ballon.position, (1, 0))
                    else:
                        self.jeu.ballon.position = add(
                            self.jeu.ballon.position, (-1, 0))
            else:
                log.debug(
                    "Joueur plaqué en dessous du plaqueur")
                if joueur2.pos[1] < nbLigne - 1:
                    self.jeu.ballon.position = add(
                        self.jeu.ballon.position, (0, 1))
                else:
                    log.debug(
                        "Le joueur plaqué est tout en bas")
                    if joueur2.pos[0] < nbColonne / 2:
                        self.jeu.ballon.position = add(
                            self.jeu.ballon.position, (1, 0))
                    else:
                        self.jeu.ballon.position = add(
                            self.jeu.ballon.position, (-1, 0))
        log.debug(
            "Un joueur sur la case du ballon qui le récupère")
        self.jeu.ballon.porteur = self.jeu.matrice[
            self.jeu.ballon.position[0]][self.jeu.ballon.position[1]][-1]
        if self.jeu.ballon.porteur.nEquipe != 3:
            self.jeu.ballon.porteur.porteur = True

    def placage(self, joueur2, plaquer=True):
        log.info("Le joueur {0} essaie de plaquer le joueur {1}".format(
            self.numero, joueur2.numero))
        if sum(absol(sub(self.pos, joueur2.pos))) == 1 and (plaquer or self.depRestant > 1) and not(self.jeu.matrice[self.pos[0]][self.pos[1]][0].ko):
            if joueur2.nEquipe != 3 and joueur2.nEquipe != self.nEquipe and not (joueur2.ko or self.ko) and ((self.porteur and not(plaquer)) or (joueur2.porteur and plaquer)):
                resolution = self.jeu.resolution(self, joueur2)
                if resolution > 0:
                    if resolution >= 2 and plaquer:
                        log.debug("Plaquage parfait")
                        self.porteur = True
                        self.jeu.ballon.porteur = self
                        self.jeu.ballon.deplacement()
                    else:
                        self.poseballon(joueur2)
                    joueur2.ko = True
                    joueur2.koCount = 1
                    joueur2.porteur = False
                    if plaquer:
                        self.depRestant = 0
                    else:
                        self.deplacement(joueur2.pos)
                        self.depRestant -= 1
                else:
                    self.ko = True
                    self.koCount = 1
                    if not plaquer :
                        joueur2.poseballon(self)
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
        log.info("Le joueur {0} essaie de tirer en avant".format(self.numero))
        if self.porteur:
            if self.nobodyFront() and self.front(pos):
                self.porteur = False
                self.jeu.ballon.position = pos
                self.jeu.ballon.porteur = self.jeu.matrice[pos[0]][pos[1]][-1]
                self.jeu.matrice[pos[0]][pos[1]][-1].porteur = True
            elif (not self.nobodyFront()):
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
        log.debug("Initialisation de l'équipe {0}".format(nEquipe))
        self.equipe = [joueur(self, jeu, nEquipe, positions[
                              i], prop[i], i) for i in range(6)]
        self.score = 0
        self.coupRestant = 2
        self.jeu = jeu
        self.carte = [True for i in range(6)]
        self.nEquipe = nEquipe
        self.equipe = [joueur(self, jeu, nEquipe, positions[
                              i], prop[i], i) for i in range(6)]

    def joue(self):
        # Reinitialisation
        log.debug("L'équipe {0} joue un tour".format(self.nEquipe))
        self.coupRestant = 2
        for joueur in self.equipe:
            joueur.depRestant = bonus[joueur.prop][2]
        for joueur in self.jeu.equipe1.equipe:
            if joueur.ko and joueur.koCount <= -1:
                joueur.ko = False
                joueur.koCount = -1
        for joueur in self.jeu.equipe2.equipe:
            if joueur.ko and joueur.koCount <= -1:
                joueur.ko = False
                joueur.koCount = -1

        globalQueue.queue.put(self.jeu)
        cont = True
        while cont:
            globalQueue.waitOut = True
            globalQueue.waitInput.put(True)
            globalQueue.equipeJoue.put(self.nEquipe)
            args = globalQueue.queueAction.get()
            globalQueue.waitOut = False
            if args[0] == "fin":
                if self.finTour():
                    cont = False
                else:
                    print("Des joueurs se superposent")
            else:
                pos1 = args[0]
                pos2 = args[1]
                if inRangeGrid(pos1) and inRangeGrid(pos2):
                    j1 = self.jeu.matrice[pos1[0]][pos1[1]][-1]
                    j2 = self.jeu.matrice[pos2[0]][pos2[1]][-1]
                    if sum(absol(sub(pos1, pos2))) > 1:
                        if (j1.nEquipe == self.nEquipe and j2.nEquipe == j1.nEquipe):
                            j1.passe(j2)
                        else:
                            j1.tirAvant(pos2)
                    else:
                        if (j2.nEquipe == 3 or j2.ko) and j1.nEquipe == self.nEquipe:
                            j1.deplacement(pos2)
                            if j1.pos[0] == 0 or j1.pos[0] == 12:
                                break
                        elif (j1.nEquipe == self.nEquipe and j2.nEquipe != j1.nEquipe and j1.porteur and j2.nEquipe != 3):
                            j1.placage(j2, False)
                        elif (j1.nEquipe == self.nEquipe and j2.nEquipe == j1.nEquipe):
                            j1.passe(j2)
                        elif (j1.nEquipe == self.nEquipe and j2.nEquipe != self.nEquipe and j2.nEquipe != 3):
                            j1.placage(j2)
        for joueur in self.jeu.equipe1.equipe:
            if joueur.ko:
                joueur.koCount -= 1
        for joueur in self.jeu.equipe2.equipe:
            if joueur.ko:
                joueur.koCount -= 1

        if not cont:
            self.jeu.changeTour()
        else:
            print("L'équipe " + str(self.nEquipe) + " a gagné!")

    def forme(self):
        log.debug("Calcul de la forme de l'équipe {0}".format(self.nEquipe))
        if self.carte == [False for i in range(6)]:
            log.debug(
                "Toutes les cartes de l'équipe {0} ont été utilisées".format(self.nEquipe))
            self.carte = [True for i in range(6)]
        cartePossible = []
        for i in range(len(self.carte)):
            if self.carte[i]:
                cartePossible.append(i)
        e = random.randint(0, len(cartePossible) - 1)
        log.debug("La carte {0} de l'équipe {1} a été utilisée ".format(
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
