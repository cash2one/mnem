'''
Created on 1 Apr 2016

@author: John Beard
'''

import unittest

from mnem.tests.plugin_tests import google

def main():
    suite = unittest.TestLoader().loadTestsFromTestCase(google.GoogleTest)

    unittest.TextTestRunner().run(suite)

if __name__ == '__main__':
    main()
