import globals
import random

def dumpData(data,filename):
	import json
	path = 'data/'+filename
	with open(path,'w') as file:
		json.dump(data,file)

def genDummyData():
	globals.dir = "dummy"
	globals.matrix = [[1.0,0.34,0.45,0.11],[0.09,1.0,0.23,0.57],[0.17,0.43,1.0,0.18],[0.17,0.43,0.09,1.0]]
	globals.files = ['file1.txt','file2.cpp','file3.py','file4.mpg']

	globals.jsonData = {"dir": globals.dir}
	fileList = []
	for file in globals.files:
		temp = {};
		temp['name'] = file
		temp['category'] = random.randint(0,len(globals.files))%20;
		fileList.append(temp)

	globals.jsonData['files'] = fileList

	jlist = []
	n = len(globals.matrix)
	for i in range(n):
		for j in range(i+1,n):
			if globals.matrix[i][j]>globals.beta:
				temp = {}
				temp['source'] = i
				temp['target'] = j
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