def GenEdgePertNetworkFiles(network):

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

    try:
		os.mkdir('inputfiles') #If folder doesn't exist then create it
	except:
		pass

    for i in range(len(R)):
        R_ = R.copy()
        edge = R[i]
        del R_[i]

        with open('inputfiles/' + edge[0] +"_"+ edge[1] +"_"+ "del" +'.topo', 'w') as f:
            f.write('Source\tTarget\tType\n')
            for j in range(len(R_new)):
                f.write(R_new[j][0] + '\t' + R_new[j][1] + '\t' + R_new[j][2] + '\n')

        with open(network + '.ids', 'r') as f, open('inputfiles/' + edge[0] +"_"+ edge[1] +"_"+ "del" + '.ids', 'w') as g:
            for line in f:
                g.write(line.strip() + '\n') #Generating ids for all the random network files.

        R_ = R.copy()
        if R_[i][2] == '1':
            R_[i][2] = '2'
        elif R_[i][2] == '2':
            R_[i][2] = '1'

        with open('inputfiles/' + edge[0] +"_"+ edge[1] +"_"+ "change" +'.topo', 'w') as f:
            f.write('Source\tTarget\tType\n')
            for j in range(len(R_new)):
                f.write(R_new[j][0] + '\t' + R_new[j][1] + '\t' + R_new[j][2] + '\n')

        with open(network + '.ids', 'r') as f, open('inputfiles/' + edge[0] +"_"+ edge[1] +"_"+ "change" + '.ids', 'w') as g:
            for line in f:
                g.write(line.strip() + '\n') #Generating ids for all the random network files.
