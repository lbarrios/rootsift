#!/usr/bin/env python
import numpy as np

def loadImage(number):
	return np.loadtxt("/home/lbarrios/datasets/images/INRIA_Holydays/jpg/%s.jpg.hesaff.sift.rootsift"%(number))