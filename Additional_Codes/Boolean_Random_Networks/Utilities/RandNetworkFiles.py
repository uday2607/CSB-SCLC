def GenRandNetworks(num,network):

	import sys

	R = [] #List which contains all the target, source and interaction values
	with open(network + '.topo', 'r') as f:
		count = 0
		for line in f:
			if count == 0:
				count += 1    #To omit the first line
				continue
			l = line.strip().split('\t')
			R.append([l[0].strip(), l[1].strip(), l[2].strip()]) #Storing all the details from .topo file

	from math import floor
	from math import log
	import random
	import os
	random.seed(os.urandom(10)) #Wonderful Random seed. The best in business

	try:
		os.mkdir('inputfiles') #If folder doesn't exist then create it
	except:
		pass

	for i in range(0,num+1): #Generating 100 Random Networks
		R_new = [] #For each new network SToring the nodes in R_new
		for j in range(len(R)):
			R_new.append([R[j][0], R[j][1], R[j][2]]) #Storing the old one for modification
		N = int(floor(log(1e7)*len(R_new) / 2)) #I don't why this. BUt seems a good value
		for j in range(N):
			edge1 = int(floor(random.randint(0, len(R_new) - 1))) #Random edge
			edge2 = edge1
			while edge2 == edge1:
				edge2 = int(floor(random.randint(0, len(R_new) - 1))) #Making sure Edge 1 and Edge 2 are not same
			target1 = R_new[edge1][1]
			target2 = R_new[edge2][1]
			R_new[edge1][1] = target2 #Shifting the target nodes of the edges
			R_new[edge2][1] = target1

		if i == 0: #For i = 0, we are writing the wild type to the file
			with open('inputfiles/' + network + '.topo', 'w') as f:
				f.write('Source\tTarget\tType\n')
				for j in range(len(R)):
					f.write(R[j][0] + '\t' + R[j][1] + '\t' + R[j][2] + '\n')
		else:
			with open('inputfiles/' + network + '_' + str(i) +'.topo', 'w') as f:
				f.write('Source\tTarget\tType\n')
				for j in range(len(R_new)):
					f.write(R_new[j][0] + '\t' + R_new[j][1] + '\t' + R_new[j][2] + '\n')

		if i == 0:
			with open(network + '.ids', 'r') as f, open('inputfiles/' + network + '.ids', 'w') as g:
				for line in f:
					g.write(line.strip() + '\n') #Generating ids for all the random network files.
			with open(network + '.phs', 'r') as f, open('inputfiles/' + network + '.phs', 'w') as g:
				for line in f:
					g.write(line.strip() + '\n')
		else:
			with open(network + '.ids', 'r') as f, open('inputfiles/' + network + '_' + str(i) + '.ids', 'w') as g:
				for line in f:
					g.write(line.strip() + '\n') #Generating ids for all the random network files.
			with open(network + '.phs', 'r') as f, open('inputfiles/' + network + '_' + str(i) + '.phs', 'w') as g:
				for line in f:
					g.write(line.strip() + '\n')
