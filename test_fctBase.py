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
		self.assertEqual(projet.intInput(),-1)
