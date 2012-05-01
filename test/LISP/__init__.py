from Eval import evall
from Enviroment import Enviroment
from Printer import printLisp
from Reader import readLisp

import unittest

suite = unittest.TestLoader().loadTestsFromTestCase(unittest.TestCase)
unittest.TextTestRunner(verbosity=2).run(suite)