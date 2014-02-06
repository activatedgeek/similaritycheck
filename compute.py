import os,subprocess
from munkres import Munkres
import globals

#setup resulting matrix
def setupMatrix(n):
	globals.matrix = []
	for i in range(n):
		temp = []
		j=0
		while j<n:
			temp.append(-1)
			j+=1
		globals.matrix.append(temp)

#similarity calculation between pair of sentences
def lineSimUtil(s,t,alpha):
	s = s.split(' ')
	t = t.split(' ')
	union = len(set(s).union(set(t)))
	intersection = len(set(s).intersection(set(t)))
	score =  float(intersection)/union
	if score<alpha:
		score=0.0
	return score

#similarity index for given pair of files
def fileSimScore(fileapath,filebpath,alpha,beta):
	astream = open(dir+'/'+fileapath,'r').read()
	bstream = open(dir+'/'+filebpath,'r').read()
	astream = astream.split('\n')
	bstream = bstream.split('\n')
	if len(astream)>len(bstream):
		astream, bstream = bstream, astream

	matScore = []
	for sWord in astream:
		temp = []
		for tWord in bstream:
			sWord = sWord.lower()
			tWord = tWord.lower()
			sim = lineSimUtil(sWord,tWord,alpha)
			temp.append(sim)
		matScore.append(temp)

	m = Munkres()
	for i in range(len(matScore)):
		for j in range(len(matScore[i])):
			matScore[i][j] = 1.0 - matScore[i][j]

	results = m.compute(matScore)
	fres = []

	#remove all 0 weight connections (here inverted connections)
	for row,col in results:
		if matScore[row][col]!=1.0:
			fres.append(1-matScore[row][col])

	score =  float(len(fres))/len(astream)
	if score<beta:
		score=0
	return score

#gets all the text readable files
def getASCII(dir):
	import mimetypes
	result = []
	files = os.listdir(dir)
	for file in files:
		if os.path.isfile(dir+'/'+file):
			try:
				output = subprocess.check_output('file "'+dir+'/'+file+'" | grep -o "ASCII text"', shell=True)
				output = output[:-1]
				if output == 'ASCII text':
					result.append(file)
			except subprocess.CalledProcessError:
				n=-1
	return result

def populateMatrix(dir,alpha,beta):
	globals.files = getASCII(dir)
	n = len(files)
	setupMatrix(n)

	for i in range(n):
		for j in range(i,n):
			if j==i:
				globals.matrix[i][j] = 1
			else:
				globals.matrix[i][j] = fileSimScore(file[i],file[j],alpha)

	return True

def main():
	populateMatrix(globals.dir,globals.alpha,globals.beta)

if __name__=='__main__':
	main()