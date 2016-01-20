import projet
import unittest
import unittest.mock
#import coverage

projet.log.propagate = False

positionsStr = ['1', '0', '1', '1', '2', '2', '2', '3', '1', '4', '1', '5', '10', '1', '10', '2',
                '11', '3', '11', '7', '10', '5', '10', '6']

positions = [1, 0, 1, 1, 2, 2, 2, 3, 1, 4, 1,
             5, 10, 1, 10, 2, 11, 3, 11, 7, 10, 5, 10, 6]


class test_joueur(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(test_joueur, self).__init__(*args, **kwargs)
        self.patcher = unittest.mock.patch(
            'builtins.input', unittest.mock.MagicMock(side_effect=positionsStr))
        self.patcher.start()
        self.jeu = projet.jeu()
        self.patcher.stop()

    def test_enArriere(self):
        self.assertFalse(self.jeu.equipe1.equipe[
                         0].enArriere(self.jeu.equipe1.equipe[1]))
        self.assertFalse(self.jeu.equipe1.equipe[
                         1].enArriere(self.jeu.equipe1.equipe[1]))
        self.assertTrue(self.jeu.equipe1.equipe[
                        2].enArriere(self.jeu.equipe1.equipe[1]))
        self.assertTrue(
            self.jeu.equipe1.equipe[-3].enArriere(self.jeu.equipe1.equipe[-1]))
        self.assertFalse(
            self.jeu.equipe1.equipe[-1].enArriere(self.jeu.equipe1.equipe[-3]))
        self.jeu.equipe1.equipe[2].pos = (10, 10)
        self.assertFalse(self.jeu.equipe1.equipe[
                         2].enArriere(self.jeu.equipe1.equipe[1]))

    def test_nobodyFront(self):
        self.jeu.equipe1.equipe[2].pos = (10, 10)
        self.assertTrue(self.jeu.equipe1.equipe[2].nobodyFront())
        self.assertFalse(self.jeu.equipe1.equipe[0].nobodyFront())
        self.jeu.equipe2.equipe[2].pos = (2, 2)
        self.assertTrue(self.jeu.equipe2.equipe[2].nobodyFront())
        self.assertFalse(self.jeu.equipe2.equipe[0].nobodyFront())

    def test_front(self):
        self.assertTrue(self.jeu.equipe1.equipe[2].front((3, 3)))
        self.assertFalse(self.jeu.equipe1.equipe[2].front((2, 3)))
        self.assertFalse(self.jeu.equipe1.equipe[2].front((7, 3)))
        self.assertFalse(self.jeu.equipe2.equipe[-1].front((3, 3)))
        self.assertFalse(self.jeu.equipe2.equipe[-1].front((11, 3)))
        self.assertTrue(self.jeu.equipe2.equipe[-1].front((9, 3)))

    def test_tirAvant1(self):
        self.jeu.equipe1.equipe[0].porteur = True
        self.jeu.ballon.position = (4, 2)
        self.jeu.equipe1.equipe[0].pos = (4, 2)
        self.jeu.ballon.porteur = self.jeu.equipe1.equipe[0]
        self.jeu.equipe1.equipe[0].tirAvant((7, 5))
        self.assertEqual(self.jeu.ballon.position, (7, 5))
        self.assertTrue(self.jeu.matrice[7][5][-1].porteur)

    def test_tirAvant2(self):
        self.jeu.equipe1.equipe[0].porteur = True
        self.jeu.ballon.position = (4, 2)
        self.jeu.equipe1.equipe[0].pos = (4, 2)
        self.jeu.ballon.porteur = self.jeu.equipe1.equipe[0]
        self.jeu.equipe2.equipe[0].deplace((7, 5))
        self.jeu.equipe1.equipe[0].tirAvant((7, 5))
        self.assertEqual(self.jeu.ballon.position, (7, 5))
        self.assertTrue(self.jeu.equipe2.equipe[0].porteur)

    @unittest.mock.patch('projet.jeu.resolution', unittest.mock.MagicMock(side_effect=[1]))
    def test_placage1(self):
        j1 = self.jeu.equipe1.equipe[0]
        j2 = self.jeu.equipe2.equipe[0]
        j2.porteur = True
        j1.deplace((4, 5))
        j2.deplace((5, 5))
        self.jeu.ballon.porteur = j2
        self.jeu.ballon.deplacement()
        j1.placage(j2)
        self.assertTrue(j2.ko)
        self.assertFalse(j1.porteur)
        self.assertFalse(j2.porteur)
        self.assertEqual(j1.pos,(4,5))
        self.assertEqual(self.jeu.ballon.position, (6, 5))
        self.assertEqual(self.jeu.ballon.porteur.nEquipe, 3)

    @unittest.mock.patch('projet.jeu.resolution', unittest.mock.MagicMock(side_effect=[3]))
    def test_placage2(self):
        j1 = self.jeu.equipe1.equipe[0]
        j2 = self.jeu.equipe2.equipe[0]
        j2.porteur = True
        j1.deplace((4, 5))
        j2.deplace((5, 5))
        self.jeu.ballon.porteur = j2
        self.jeu.ballon.deplacement()
        j1.placage(j2)
        self.assertTrue(j2.ko)
        self.assertTrue(j1.porteur)
        self.assertFalse(j2.porteur)
        self.assertEqual(self.jeu.ballon.position, (4, 5))
        self.assertEqual(self.jeu.ballon.porteur.nEquipe, 1)

    @unittest.mock.patch('projet.jeu.resolution', unittest.mock.MagicMock(side_effect=[1]))
    def test_placage3(self):
        j1 = self.jeu.equipe1.equipe[0]
        j2 = self.jeu.equipe2.equipe[0]
        j2.porteur = False
        j1.deplace((4, 5))
        j2.deplace((5, 5))
        pos = self.jeu.ballon.position
        j1.placage(j2)
        self.assertFalse(j2.ko)
        self.assertFalse(j1.porteur)
        self.assertFalse(j2.porteur)
        self.assertEqual(self.jeu.ballon.position, pos)
        self.assertEqual(self.jeu.ballon.porteur.nEquipe, 3)

    @unittest.mock.patch('projet.jeu.resolution', unittest.mock.MagicMock(side_effect=[-1]))
    def test_placage4(self):
        j1 = self.jeu.equipe1.equipe[0]
        j2 = self.jeu.equipe2.equipe[0]
        j2.porteur = True
        j1.deplace((4, 5))
        j2.deplace((5, 5))
        self.jeu.ballon.porteur = j2
        self.jeu.ballon.deplacement()
        j1.placage(j2)
        self.assertTrue(j1.ko)
        self.assertFalse(j2.ko)
        self.assertFalse(j1.porteur)
        self.assertTrue(j2.porteur)
        self.assertEqual(self.jeu.ballon.position, (5, 5))
        self.assertEqual(self.jeu.ballon.porteur.nEquipe, 2)

    @unittest.mock.patch('projet.jeu.resolution', unittest.mock.MagicMock(side_effect=[1]))
    def test_placage5(self):
        j1 = self.jeu.equipe1.equipe[0]
        j2 = self.jeu.equipe2.equipe[0]
        j2.porteur = True
        j1.deplace((5, 6))
        j2.deplace((5, 5))
        self.jeu.ballon.porteur = j2
        self.jeu.ballon.deplacement()
        j1.placage(j2)
        self.assertTrue(j2.ko)
        self.assertFalse(j1.porteur)
        self.assertFalse(j2.porteur)
        self.assertEqual(self.jeu.ballon.position, (5, 4))
        self.assertEqual(self.jeu.ballon.porteur.nEquipe, 3)

    @unittest.mock.patch('projet.jeu.resolution', unittest.mock.MagicMock(side_effect=[1]))
    def test_placage6(self):
        j1 = self.jeu.equipe1.equipe[0]
        j2 = self.jeu.equipe2.equipe[0]
        j2.porteur = True
        j1.deplace((10, 0))
        j2.deplace((11, 0))
        self.jeu.ballon.porteur = j2
        self.jeu.ballon.deplacement()
        j1.placage(j2)
        self.assertTrue(j2.ko)
        self.assertFalse(j1.porteur)
        self.assertFalse(j2.porteur)
        self.assertEqual(self.jeu.ballon.position, (11, 1))
        self.assertEqual(self.jeu.ballon.porteur.nEquipe, 3)

    @unittest.mock.patch('projet.jeu.resolution', unittest.mock.MagicMock(side_effect=[1]))
    def test_placage7(self):
        j1 = self.jeu.equipe1.equipe[0]
        j2 = self.jeu.equipe2.equipe[0]
        j2.porteur = True
        j1.deplace((10, 7))
        j2.deplace((11, 7))
        self.jeu.ballon.porteur = j2
        self.jeu.ballon.deplacement()
        j1.placage(j2)
        self.assertTrue(j2.ko)
        self.assertFalse(j1.porteur)
        self.assertFalse(j2.porteur)
        self.assertEqual(self.jeu.ballon.position, (11, 6))
        self.assertEqual(self.jeu.ballon.porteur.nEquipe, 3)

    @unittest.mock.patch('projet.jeu.resolution', unittest.mock.MagicMock(side_effect=[1]))
    def test_placage8(self):
        j1 = self.jeu.equipe1.equipe[0]
        j2 = self.jeu.equipe2.equipe[0]
        j1.porteur = True
        j1.deplace((1, 0))
        j2.deplace((2, 0))
        self.jeu.ballon.porteur = j1
        self.jeu.ballon.deplacement()
        j2.placage(j1)
        self.assertTrue(j1.ko)
        self.assertFalse(j2.porteur)
        self.assertFalse(j1.porteur)
        self.assertEqual(self.jeu.ballon.position, (1, 1))
        self.assertEqual(self.jeu.ballon.porteur.nEquipe, 1)

    @unittest.mock.patch('projet.jeu.resolution', unittest.mock.MagicMock(side_effect=[1]))
    def test_placage9(self):
        j1 = self.jeu.equipe1.equipe[0]
        j2 = self.jeu.equipe2.equipe[0]
        j1.porteur = True
        j1.deplace((1, 7))
        j2.deplace((2, 7))
        self.jeu.ballon.porteur = j1
        self.jeu.ballon.deplacement()
        j2.placage(j1)
        self.assertTrue(j1.ko)
        self.assertFalse(j2.porteur)
        self.assertFalse(j1.porteur)
        self.assertEqual(self.jeu.ballon.position, (1, 6))
        self.assertEqual(self.jeu.ballon.porteur.nEquipe, 3)

    @unittest.mock.patch('projet.jeu.resolution', unittest.mock.MagicMock(side_effect=[1]))
    def test_passageForce(self):
        j1 = self.jeu.equipe1.equipe[0]
        j2 = self.jeu.equipe2.equipe[0]
        j1.porteur = True
        j1.deplace((1, 0))
        j2.deplace((2, 0))
        self.jeu.ballon.porteur = j1
        self.jeu.ballon.deplacement()
        j1.placage(j2,False)
        self.assertTrue(j2.ko)
        self.assertFalse(j2.porteur)
        self.assertTrue(j1.porteur)
        self.assertEqual(self.jeu.ballon.position, (2,0))
        self.assertEqual(self.jeu.ballon.porteur.nEquipe, 1)
        self.assertEqual(j1.pos,(2,0))

    def test_passe1(self):
        self.jeu.equipe1.equipe[0].pos = (5, 1)
        self.jeu.equipe1.equipe[1].pos = (3, 3)
        self.jeu.equipe1.equipe[0].porteur = True
        self.jeu.ballon.position = (5, 1)
        self.jeu.ballon.joueur = self.jeu.equipe1.equipe[0]
        self.jeu.equipe1.equipe[0].passe(self.jeu.equipe1.equipe[1])
        self.assertEqual(self.jeu.ballon.position, (3, 3))

    def test_passe2(self):
        self.jeu.equipe1.equipe[0].pos = (5, 1)
        self.jeu.equipe1.equipe[1].pos = (3, 3)
        self.jeu.equipe1.equipe[0].porteur = True
        self.jeu.ballon.position = (5, 1)
        self.jeu.ballon.joueur = self.jeu.equipe1.equipe[0]
        self.jeu.equipe1.equipe[1].passe(self.jeu.equipe1.equipe[0])
        self.assertEqual(self.jeu.ballon.position, (5, 1))

    def test_passe3(self):
        self.jeu.equipe1.equipe[0].pos = (5, 1)
        self.jeu.equipe1.equipe[1].pos = (3, 3)
        self.jeu.equipe1.equipe[2].pos = (4, 2)
        self.jeu.equipe1.equipe[0].porteur = True
        self.jeu.ballon.position = (5, 1)
        self.jeu.ballon.joueur = self.jeu.equipe1.equipe[0]
        self.jeu.equipe1.equipe[0].passe(self.jeu.equipe1.equipe[1])
        self.assertEqual(self.jeu.ballon.position, (3, 3))

    @unittest.mock.patch('builtins.input', lambda x: '1')
    @unittest.mock.patch('projet.jeu.resolution', unittest.mock.MagicMock(side_effect=[-1]))
    def test_passe4(self):
        self.jeu.equipe1.equipe[0].pos = (5, 1)
        self.jeu.equipe1.equipe[1].pos = (3, 3)
        self.jeu.equipe2.equipe[2].pos = (4, 3)
        self.jeu.equipe1.equipe[0].porteur = True
        self.jeu.ballon.position = (5, 1)
        self.jeu.ballon.joueur = self.jeu.equipe1.equipe[0]
        self.jeu.equipe1.equipe[0].passe(self.jeu.equipe1.equipe[1])
        self.assertEqual(self.jeu.ballon.position, (3, 3))

    @unittest.mock.patch('builtins.input', lambda x: '1')
    @unittest.mock.patch('projet.jeu.resolution', unittest.mock.MagicMock(side_effect=[1]))
    def test_passe6(self):
        self.jeu.equipe1.equipe[0].pos = (5, 1)
        self.jeu.equipe1.equipe[1].pos = (3, 3)
        self.jeu.equipe2.equipe[2].pos = (4, 3)
        self.jeu.equipe1.equipe[0].porteur = True
        self.jeu.ballon.position = (5, 1)
        self.jeu.ballon.joueur = self.jeu.equipe1.equipe[0]
        self.jeu.equipe1.equipe[0].passe(self.jeu.equipe1.equipe[1])
        self.assertEqual(self.jeu.ballon.position, (3, 3))

    def test_passe7(self):
        self.jeu.equipe1.equipe[0].pos = (5, 1)
        self.jeu.equipe1.equipe[1].pos = (3, 3)
        self.jeu.equipe2.equipe[2].pos = (4, 1)
        self.jeu.equipe1.equipe[0].porteur = True
        self.jeu.ballon.position = (5, 1)
        self.jeu.ballon.joueur = self.jeu.equipe1.equipe[0]
        self.jeu.equipe1.equipe[0].passe(self.jeu.equipe1.equipe[1])
        self.assertEqual(self.jeu.ballon.position, (3, 3))

    def test_passe8(self):
        self.jeu.equipe1.equipe[0].pos = (5, 1)
        self.jeu.equipe1.equipe[1].pos = (3, 3)
        self.jeu.equipe2.equipe[2].pos = (4, 2)
        self.jeu.equipe1.equipe[0].porteur = True
        self.jeu.ballon.position = (5, 1)
        self.jeu.ballon.joueur = self.jeu.equipe1.equipe[0]
        self.jeu.equipe1.equipe[1].passe(self.jeu.equipe1.equipe[0])
        self.assertEqual(self.jeu.ballon.position, (5, 1))

    def test_deplace1(self):
        pos = self.jeu.equipe1.equipe[0].pos
        self.assertEqual(self.jeu.equipe1.equipe[0].depRestant, 3)
        self.jeu.equipe1.equipe[0].deplace((4, 4))
        self.assertEqual(self.jeu.matrice[4][4][0].pos, (4, 4))
        self.assertEqual(self.jeu.equipe1.equipe[0].pos, (4, 4))
        self.assertEqual(self.jeu.matrice[pos[0]][pos[1]][0].nEquipe, 3)
        self.assertEqual(self.jeu.equipe1.equipe[0].depRestant, 2)

    def test_deplace2(self):
        pos = self.jeu.equipe1.equipe[1].pos
        self.jeu.equipe1.equipe[0].ko = True
        self.jeu.equipe1.equipe[1].deplace(self.jeu.equipe1.equipe[0].pos)
        self.assertEqual(self.jeu.matrice[self.jeu.equipe1.equipe[0].pos[0]][self.jeu.equipe1.equipe[0].pos[1]],
                         [self.jeu.equipe1.equipe[0], self.jeu.equipe1.equipe[1]])
        self.assertEqual(self.jeu.equipe1.equipe[
                         1].pos, self.jeu.equipe1.equipe[0].pos)
        self.assertEqual(self.jeu.matrice[pos[0]][pos[1]][0].nEquipe, 3)

    def test_deplace3(self):
        self.jeu.equipe1.equipe[0].ko = True
        self.jeu.equipe1.equipe[1].deplace(self.jeu.equipe1.equipe[0].pos)
        pos = self.jeu.equipe1.equipe[1].pos
        self.jeu.equipe1.equipe[1].deplace((pos[0] + 1, pos[1]))
        self.assertEqual(self.jeu.equipe1.equipe[
                         1].pos, projet.add(pos, (1, 0)))
        self.assertEqual(self.jeu.matrice[pos[0]][pos[1]][
                         0], self.jeu.equipe1.equipe[0])

    def test_deplacementBallon(self):
        self.jeu.ballon.position = (5, 5)
        self.jeu.ballon.porteur = self.jeu.equipe1.equipe[2]
        self.jeu.ballon.deplacement()
        self.assertEqual(self.jeu.ballon.position,
                         self.jeu.equipe1.equipe[2].pos)

    def test_deplacement4(self):
        self.jeu.ballon.position = (5, 1)
        (posx, posy) = self.jeu.equipe1.equipe[0].pos
        self.jeu.ballon.porteur = self.jeu.matrice[posx][posy][0]
        self.jeu.equipe1.equipe[0].pos = (5, 0)
        dep = self.jeu.equipe1.equipe[0].depRestant 
        self.jeu.equipe1.equipe[0].deplacement((5, 1))
        self.assertTrue(self.jeu.equipe1.equipe[0].porteur)
        self.assertEqual(self.jeu.ballon.porteur.numero, 0)
        self.assertEqual(self.jeu.equipe1.equipe[0].depRestant ,dep-1)
        self.jeu.equipe1.equipe[0].deplacement((5, 2))
        self.assertEqual(self.jeu.equipe1.equipe[0].nEquipe, 1)
        self.assertEqual(self.jeu.ballon.porteur.pos, (5, 2))
        self.assertEqual(self.jeu.ballon.position, (5, 2))

    def test_onGrid1(self):
        self.jeu.equipe1.equipe[0].pos = (1,0)
        self.assertFalse(self.jeu.equipe1.equipe[0].onGrid((0,0)))

    def test_onGrid2(self):
        self.jeu.equipe1.equipe[0].pos = (11,0)
        self.assertFalse(self.jeu.equipe1.equipe[0].onGrid((12,0)))

    def test_onGrid3(self):
        self.jeu.equipe1.equipe[0].pos = (11,0)
        self.jeu.equipe1.equipe[0].porteur = True
        self.assertTrue(self.jeu.equipe1.equipe[0].onGrid((12,0)))

    def test_onGrid3_bis(self):
        self.jeu.equipe1.equipe[0].pos = (1,0)
        self.jeu.equipe1.equipe[0].porteur = True
        self.assertFalse(self.jeu.equipe1.equipe[0].onGrid((0,0)))

    def test_onGrid4(self):
        self.jeu.equipe2.equipe[0].pos = (1,0)
        self.assertFalse(self.jeu.equipe2.equipe[0].onGrid((0,0)))

    def test_onGrid5(self):
        self.jeu.equipe2.equipe[0].pos = (11,0)
        self.assertFalse(self.jeu.equipe2.equipe[0].onGrid((12,0)))

    def test_onGrid6(self):
        self.jeu.equipe2.equipe[0].pos = (11,0)
        self.jeu.equipe2.equipe[0].porteur = True
        self.assertFalse(self.jeu.equipe2.equipe[0].onGrid((12,0)))

    def test_onGrid7(self):
        self.jeu.equipe2.equipe[0].pos = (1,0)
        self.jeu.equipe2.equipe[0].porteur = True
        self.assertTrue(self.jeu.equipe2.equipe[0].onGrid((0,0)))

unittest.main()
