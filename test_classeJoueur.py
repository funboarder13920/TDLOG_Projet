import projet
import unittest
import unittest.mock

projet.log.propagate = False

positionsStr = ['1','0','1','1','2','2','2','3','1','4','1','5','10','1','10','2',
        '11','3','11','7','10','5','10','6']

positions = [1,0,1,1,2,2,2,3,1,4,1,5,10,1,10,2,11,3,11,7,10,5,10,6]

class test_joueur(unittest.TestCase):
	def __init__(self,*args, **kwargs):
		super(test_joueur, self).__init__(*args, **kwargs)
		self.patcher = unittest.mock.patch('builtins.input',unittest.mock.MagicMock(side_effect=positionsStr))
		self.patcher.start()
		self.jeu = projet.jeu()
		self.patcher.stop()

	def test_enArriere(self):
		self.assertFalse(self.jeu.equipe1.equipe[0].enArriere(self.jeu.equipe1.equipe[1]))
		self.assertFalse(self.jeu.equipe1.equipe[1].enArriere(self.jeu.equipe1.equipe[1]))
		self.assertTrue(self.jeu.equipe1.equipe[2].enArriere(self.jeu.equipe1.equipe[1]))
		self.assertTrue(self.jeu.equipe1.equipe[-3].enArriere(self.jeu.equipe1.equipe[-1]))
		self.assertFalse(self.jeu.equipe1.equipe[-1].enArriere(self.jeu.equipe1.equipe[-3]))
		self.jeu.equipe1.equipe[2].pos=(10,10)
		self.assertFalse(self.jeu.equipe1.equipe[2].enArriere(self.jeu.equipe1.equipe[1]))

	def test_nobodyFront(self):
		self.jeu.equipe1.equipe[2].pos=(10,10)
		self.assertFalse(self.jeu.equipe1.equipe[2].nobodyFront())
		self.assertFalse(self.jeu.equipe1.equipe[0].nobodyFront())
		self.jeu.equipe2.equipe[2].pos=(2,2)
		self.assertTrue(self.jeu.equipe2.equipe[2].nobodyFront())
		self.assertFalse(self.jeu.equipe2.equipe[0].nobodyFront())

	def test_front(self):
		pass

	def test_tirAvant(self):
		pass

	def test_placage(self):
		pass

	def test_passe(self):
		pass

"""
	def test_deplace1(self):
		pos = self.jeu.equipe1.equipe[0].pos
		self.assertEqual(self.jeu.equipe1.equipe[0].depRestant,3)
		self.jeu.equipe1.equipe[0].deplace((4,4))
		self.assertEqual(self.jeu.matrice[4][4][0].pos,(4,4))
		self.assertEqual(self.jeu.equipe1.equipe[0].pos,(4,4))
		self.assertEqual(self.jeu.matrice[pos[0]][pos[1]][0].nEquipe,3)
		self.assertEqual(self.jeu.equipe1.equipe[0].depRestant,2)

	def test_deplace2(self):
		pos = self.jeu.equipe1.equipe[1].pos
		self.jeu.equipe1.equipe[0].ko = True
		self.jeu.equipe1.equipe[1].deplace(self.jeu.equipe1.equipe[0].pos)
		self.assertEqual(self.jeu.matrice[self.jeu.equipe1.equipe[0].pos[0]][self.jeu.equipe1.equipe[0].pos[1]],
    		[self.jeu.equipe1.equipe[0],self.jeu.equipe1.equipe[1]])
		self.assertEqual(self.jeu.equipe1.equipe[1].pos,self.jeu.equipe1.equipe[0].pos)
		self.assertEqual(self.jeu.matrice[pos[0]][pos[1]][0].nEquipe,3)

	def test_deplace3(self):
		self.jeu.equipe1.equipe[0].ko = True
		self.jeu.equipe1.equipe[1].deplace(self.jeu.equipe1.equipe[0].pos)
		pos = self.jeu.equipe1.equipe[1].pos
		self.jeu.equipe1.equipe[1].deplace((pos[0]+1,pos[1]))
		self.assertEqual(self.jeu.equipe1.equipe[1].pos,pos)
		self.assertEqual(self.jeu.matrice[pos[0]][pos[1]][0],self.jeu.equipe1.equipe[0])
		
	def test_deplacement1(self):
		pass
"""

