import projet
import unittest
import unittest.mock


class test_absol(unittest.TestCase):
	def test1(self):
		self.assertEqual(projet.absol((-1,1)),(1,1))
	def test2(self):
		self.assertEqual(projet.absol((-1,-1)),(1,1))
	def test3(self):
		self.assertEqual(projet.absol((2,1)),(2,1))

class test_droite(unittest.TestCase):
	def test1(self):
		self.assertEqual(projet.droite((0,0),(0,1)),(1,0,0))

	def test2(self):
		self.assertEqual(projet.droite((0,0),(1,0)),(0,1,0))

	def test3(self):
		self.assertEqual(projet.droite((0,0),(1,1)),(-1,1,0))

	def test4(self):
		self.assertEqual(projet.droite((1,2),(2,3)),(-1,1,-1))

class test_intInput(unittest.TestCase):
	@unittest.mock.patch('builtins.input',lambda x:'10')
	def test1(self):
		self.assertEqual(projet.intInput("test"),10)

	@unittest.mock.patch('builtins.input',lambda x:'-1')
	def test2(self):
		print('1\n2')
		self.assertEqual(projet.intInput(),-1)

	@unittest.mock.patch('builtins.input',unittest.mock.MagicMock(side_effect = ['+','5']))
	def test3(self):
		self.assertEqual(projet.intInput(),5)

class test_choixPos(unittest.TestCase):
	@unittest.mock.patch('projet.equipe', nbEquipe = 1)
	@unittest.mock.patch('builtins.input',unittest.mock.MagicMock(side_effect=['-1', '1','1','2','1','0','1','2',
		'1','7','1','12','1','-1','1','8','2','0','2','3','2','4','11','0','11','8']))
	# mettre une liste pour input
	# mock patch une équipe?
	def test1(self,equipe):
		self.assertEqual(projet.choixPos(equipe.nbEquipe),[(1,2),(1,0),(1,7),(2,0),(2,3),(2,4)])