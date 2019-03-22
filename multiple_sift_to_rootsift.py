#!/usr/bin/env python
import sys
import subprocess
import os

cmd = "python single_sift_to_rootsift.py"

if len(sys.argv)<3:
	print("Usage: " + sys.argv[0] + " image_number_start image_number_end")
	print("\tfor INRIA_Holydays dataset")
	print("\twith image_number from 100000 to 149902")
	exit()

image_number_start = int(sys.argv[1])
image_number_end = int(sys.argv[2])
if(image_number_start < 100000 or image_number_start > 149902 or image_number_end < 100000 or image_number_end > 149902):
	print("ERROR: image_number needs to be from 100000 to 149902")
	exit()
if(image_number_start > image_number_end):
	print("ERROR: image_number_start needs to be less or equal than image_number_end")

for image_number in range(image_number_start, image_number_end+1):
	image_file = "%s.jpg.hesaff.sift"%(image_number)
	dataset_base = "/home/lbarrios/datasets/images/"
	dataset = "INRIA_Holydays/jpg"
	dataset_path = dataset_base + dataset + "/"
	image_path = dataset_path + image_file
	if not os.path.isfile(image_path):
		continue
	subprocess.run([cmd, image_path])
	print("Image number %s converted from sift to rootsift."%image_number)