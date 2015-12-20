import projet
import unittest
import unittest.mock

class test_jeu(unittest.Testcase):
	def __init__(self, *args, **kwargs):
		super(CasDeTest, self).__init__(*args, **kwargs)
		jeu = projet.jeu()