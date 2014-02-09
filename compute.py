import os,subprocess
from munkres import Munkres
import globals

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
	astream = open(globals.dir+'/'+fileapath,'r').read()
	bstream = open(globals.dir+'/'+filebpath,'r').read()
	astream = astream.split('\n')
	bstream = bstream.split('\n')

	if len(astream)>len(bstream):
		astream, bstream = bstream, astream

	matScore = []
	for s in astream:
		temp = []
		for t in bstream:
			if s=='' or t=='':
				temp.append(1.0)
				continue
			s = s.lower()
			t = t.lower()
			sim = lineSimUtil(s,t,alpha)
			temp.append(1.0 - sim)
		matScore.append(temp)

	m = Munkres()

	results = m.compute(matScore)
	fres = []

	#remove all 0 weight connections (here inverted connections)
	for row,col in results:
		if matScore[row][col]!=1.0:
			fres.append([row,col])

	score =  float(len(fres))/len(astream)
	if score<beta:
		score=0.0
	return score,fres

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
	globals.files.sort()
	n = len(globals.files)

	for i in range(n):
		temp = []
		links = []
		for j in range(n):
			if j<=i:
				temp.append(-1)
				links.append([])
			else:
				score,combines = fileSimScore(globals.files[i],globals.files[j],alpha,beta)
				temp.append(score)
				links.append(combines)

		globals.matrix.append(temp)
		globals.matrixLinks.append(links)

	return True

def main():
	result = populateMatrix(globals.dir,globals.alpha,globals.beta)

if __name__=='__main__':
	main()