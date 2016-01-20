import projet
import unittest
import unittest.mock
#import coverage


projet.log.propagate = False

positionsStr = ['1', '0', '1', '1', '2', '2', '2', '3', '1', '4', '1', '5', '10', '1', '10', '2',
                '11', '3', '11', '7', '10', '5', '10', '6']

positions = [1, 0, 1, 1, 2, 2, 2, 3, 1, 4, 1,
             5, 10, 1, 10, 2, 11, 3, 11, 7, 10, 5, 10, 6]


class test_jeu(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(test_jeu, self).__init__(*args, **kwargs)
        self.patcher = unittest.mock.patch(
            'builtins.input', unittest.mock.MagicMock(side_effect=positionsStr))
        self.patcher.start()
        self.jeu = projet.jeu()
        self.patcher.stop()

    def test_positionsEquipe1(self):
        for i in range(6):
            self.assertEqual(self.jeu.equipe1.equipe[i].pos,
                             (positions[2 * i], positions[2 * i + 1]))

    def test_positionsEquipe2(self):
        for i in range(6):
            self.assertEqual(self.jeu.equipe2.equipe[i].pos,
                             (positions[2 * i + 12], positions[12 + 2 * i + 1]))

    def test_forme(self):
        self.jeu.equipe1.carte = [True, True, False, False, False, False]
        self.jeu.equipe1.forme()
        self.assertNotEqual(self.jeu.equipe1.carte, [
                            True, True, False, False, False, False])
        self.jeu.equipe1.forme()
        self.assertEqual(self.jeu.equipe1.carte, [
                         False, False, False, False, False, False])
        self.jeu.equipe1.forme()
        self.assertEqual(self.jeu.equipe1.carte.count(False), 1)
        self.jeu.equipe1.carte = [True, True, True, True, True, True]

    @unittest.mock.patch('projet.equipe.forme', unittest.mock.MagicMock(side_effect=[2, 0]))
    def test_resolution1(self):
        self.assertGreater(self.jeu.resolution(
            self.jeu.equipe1.equipe[0], self.jeu.equipe1.equipe[0]), 0)

    @unittest.mock.patch('projet.equipe.forme', unittest.mock.MagicMock(side_effect=[1, 1, 2, 0]))
    def test_resolution2(self):
        self.assertGreater(self.jeu.resolution(
            self.jeu.equipe1.equipe[0], self.jeu.equipe1.equipe[0]), 0)

    @unittest.mock.patch('projet.equipe.forme', unittest.mock.MagicMock(side_effect=[1, 1, 2, 2]))
    def test_resolution3(self):
        self.assertLessEqual(self.jeu.resolution(
            self.jeu.equipe1.equipe[0], self.jeu.equipe1.equipe[0]), 0)

    def test_resolution4(self):
        nbTrue = 0
        nbFalse = 0
        for i in range(1000):
            if self.jeu.resolution(self.jeu.equipe1.equipe[0], self.jeu.equipe2.equipe[0]) > 0:
                nbTrue += 1
            else:
                nbFalse += 1
        self.assertLess(nbTrue / 1000, 0.5)

    def test_resolution5(self):
        nbTrue = 0
        nbFalse = 0
        for i in range(1000):
            if self.jeu.resolution(self.jeu.equipe1.equipe[0], self.jeu.equipe2.equipe[5]) > 0:
                nbTrue += 1
            else:
                nbFalse += 1
        self.assertGreater(nbTrue / 1000, 0.63)

    def test_resolution6(self):
        nbTrue = 0
        nbFalse = 0
        for i in range(1000):
            if self.jeu.resolution(self.jeu.equipe1.equipe[0], self.jeu.equipe2.equipe[4]) > 0:
                nbTrue += 1
            else:
                nbFalse += 1
        self.assertLess(nbTrue / 1000, 0.36)

    def test_resolution7(self):
        nbTrue = 0
        nbFalse = 0
        for i in range(1000):
            if self.jeu.resolution(self.jeu.equipe1.equipe[3], self.jeu.equipe2.equipe[0]) >= 0:
                nbTrue += 1
            else:
                nbFalse += 1
        self.assertGreater(nbTrue / 1000, 0.78)

    def test_libre1(self):
        self.assertFalse(self.jeu.libre((1, 1)))
        self.assertTrue(self.jeu.libre((3, 2)))
        self.assertFalse(self.jeu.libre((2, 3)))

    def test_libre2(self):
        self.jeu.equipe1.equipe[0].ko = True
        self.assertFalse(self.jeu.libre(self.jeu.equipe1.equipe[0].pos, 1))
        self.assertFalse(self.jeu.libre(self.jeu.equipe1.equipe[0].pos))
        self.assertTrue(self.jeu.libre(self.jeu.equipe1.equipe[0].pos, 2))
        self.jeu.equipe1.equipe[0].ko = False

    # Tests interception à partir de l'exemple des règles
    def test_interception1(self):
        self.jeu.equipe1.equipe[0].pos = (1, 0)
        self.jeu.equipe1.equipe[1].pos = (5, 0)
        self.jeu.equipe2.equipe[1].pos = (2, 0)
        self.assertEqual(len(self.jeu.interception(self.jeu.equipe1.equipe[0],
                                                   self.jeu.equipe1.equipe[1])), 1)

    def test_interception2(self):
        self.jeu.equipe1.equipe[0].pos = (6, 4)
        self.jeu.equipe1.equipe[1].pos = (8, 4)
        self.jeu.equipe1.equipe[2].pos = (8, 5)
        self.jeu.equipe1.equipe[3].pos = (7, 6)
        self.jeu.equipe1.equipe[4].pos = (7, 7)
        self.jeu.equipe1.equipe[5].pos = (7, 3)
        self.jeu.equipe2.equipe[0].pos = (7, 5)
        self.assertEqual(len(self.jeu.interception(self.jeu.equipe1.equipe[0],
                                                   self.jeu.equipe1.equipe[1])), 0)
        self.assertEqual(len(self.jeu.interception(self.jeu.equipe1.equipe[0],
                                                   self.jeu.equipe1.equipe[2])), 1)
        self.assertEqual(len(self.jeu.interception(self.jeu.equipe1.equipe[0],
                                                   self.jeu.equipe1.equipe[3])), 1)
        self.assertEqual(len(self.jeu.interception(self.jeu.equipe1.equipe[0],
                                                   self.jeu.equipe1.equipe[4])), 0)
        self.assertEqual(len(self.jeu.interception(self.jeu.equipe1.equipe[0],
                                                   self.jeu.equipe1.equipe[5])), 0)

    def test_interception3(self):
        self.jeu.equipe1.equipe[0].pos = (5, 1)
        self.jeu.equipe1.equipe[1].pos = (3, 3)
        self.jeu.equipe2.equipe[2].pos = (4, 1)
        self.assertEqual(len(self.jeu.interception(self.jeu.equipe1.equipe[0],
                                                   self.jeu.equipe1.equipe[1])), 0)

unittest.main()
