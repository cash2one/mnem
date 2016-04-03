#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Created on 2 Apr 2016

Nose wrapper for running tests

@author: John Beard
'''

import nose
import sys

argv = sys.argv[:]
nose.main(argv=argv)