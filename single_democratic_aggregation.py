#!/usr/bin/env python
import numpy as np
import os
import sys
from sklearn.cluster import KMeans
from sklearn.preprocessing import normalize

# Links:
# https://davidstutz.de/triangulation-embedding-democratic-aggregation-image-search-jegou-zisserman/
# http://www.aprendemachinelearning.com/k-means-en-python-paso-a-paso

N_CLUSTERS = 16

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
image_arg = sys.argv[1]
if os.path.isfile(image_arg):
	# Full path
	rootsift_path = image_arg
else:
	image_number = int(image_arg)
	# Inria dataset
	if(image_number < 100000 or image_number > 149902):
		print("ERROR: image_number needs to be from 100000 to 149902")
		exit()
	image_file = "%s.jpg"%(image_number)
	rootsift_file = image_file + ".hesaff.sift.rootsift"
	rootsift_path = inria_dataset_path + rootsift_file

descs = np.loadtxt(rootsift_path)
print("loaded image %s rootsift descriptors (%s)"%(image_arg, len(descs)))

# compute C, the set of representative anchor points using kmeans
kmeans = KMeans(n_clusters=N_CLUSTERS).fit(descs)
C = kmeans.cluster_centers_

# compute the normalized residual vectors
R = [np.zeros((len(descs[0]),len(C))) for x in descs]
for i in range(len(C)):
	XCi = descs-C[i]
	Ri = normalize(XCi, axis=1)#, norm='l2')
	# for every image, complete the "i" residual vector
	for j in range(len(descs)):
		R[j][:,i] = Ri[i]

# # compute the normalized residual vectors
# R = [np.zeros((len(C), len(descs[0]))) for x in descs]
# for i in range(len(C)):
# 	XCi = descs-C[i]
# 	Ri = normalize(XCi, axis=1)#, norm='l2')
# 	# for every image, complete the "i" residual vector
# 	for j in range(len(descs)):
# 		R[j][i] = Ri[i]

tembedding=list()
i = 0
for Rj in R:
	i += 1
	mean = np.mean(Rj)
	cov = np.cov(Rj)
	tembedding.append(scipy.linalg.sqrtm(cov).dot((Rj-mean)))
	if i%50 == 0:
		print("%s/%s"%(i,len(R)))

print(tembedding)