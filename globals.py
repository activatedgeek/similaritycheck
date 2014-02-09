#files list in dir
dir = ''
files = None

#matrix containing scores
matrix = []
matrixLinks = []
alpha = 0.0
beta = 0.0

jsonData = None

def resetGlobals():
	global dir,files,matrix,matrixLinks,alpha,beta,jsonData
	dir = ''
	files = None

	matrix = []
	matrixLinks = []
	alpha = 0.0
	beta = 0.0

	jsonData = None