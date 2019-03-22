#!/usr/bin/env python
import cv2 as cv
import numpy as np
from sklearn import preprocessing
import sys
import os

# script global parameters
dataset_base = "%s/datasets/images/"%(os.getenv("HOME"))
inria_dataset_path = dataset_base + "INRIA_Holydays/jpg/"

# check argument count
if len(sys.argv)<2:
	print("Usage: " + sys.argv[0] + " full_path_to_image")
	print("OR usage: " + sys.argv[0] + " image_number")
	print("\tfor INRIA_Holydays dataset (https://lear.inrialpes.fr/~jegou/data.php)")
	print("\tsaved at path %s"%(inria_dataset_path))
	print("\twith image_number from 100000 to 149902")
	exit()

# parse arguments
image_number = int(sys.argv[1])
if os.path.isfile(image_number):
	# Full path
	sift_path = image_number
	rootsift_path = sift_path + ".rootsift"
else:
	# Inria dataset
	if(image_number < 100000 or image_number > 149902):
		print("ERROR: image_number needs to be from 100000 to 149902")
		exit()
	image_file = "%s.jpg"%(image_number)
	sift_file = image_file + ".hesaff.sift"
	rootsift_file = sift_file + ".rootsift"
	sift_path = inria_dataset_path + sift_file
	rootsift_path = inria_dataset_path + rootsift_file


eps=1e-7 #< what is this parameter for?
# read descriptors from file
with open(sift_path) as fp:
	descriptors_lenght = int(fp.readline())
	descriptors_count = int(fp.readline())
	descs_list = list()
	for i in range(descriptors_count):
		descs_line = fp.readline().split()
		descs_list.append(list(map(int,descs_line[5:])))

# convert from sift to rootsift
descs = np.asarray(descs_list, dtype=np.float)
descs /= (descs.sum(axis=1, keepdims=True) + eps)
descs = np.sqrt(descs)

np.save(rootsift_path, descs)