import globals

def dumpData(data,filename):
	import json
	path = 'data/'+filename
	with open(path,'w') as file:
		json.dump(data,file)

def genDummyData():
	globals.dir = "dummy"
	globals.matrix = [[1.0,0.34,0.45],[0.09,1.0,0.23],[0.17,0.43,1.0]]
	globals.files = ['file1.txt','file2.cpp','file3.py']

	globals.jsonData = {"dir": globals.dir , "files" : globals.files}
	jlist = []
	n = len(globals.matrix)
	for i in range(n):
		for j in range(n):
			if globals.matrix[i][j]>globals.beta:
				temp = {}
				temp['src'] = globals.files[i]
				temp['dst'] = globals.files[j]
				temp['weight'] = globals.matrix[i][j]
				jlist.append(temp)

	globals.jsonData['fileLinks'] = jlist

def generateData():
	genDummyData()
	dumpData(globals.jsonData,'data.json')

def main():
	generateData()

if __name__=='__main__':
	main()