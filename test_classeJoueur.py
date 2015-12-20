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