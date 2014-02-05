#!/usr/bin/python

from Tkinter import Tk, BOTH, RIGHT,StringVar,Text
from ttk import Frame,Button,Style,Label,Entry
import os,sys
import subprocess
from munkres import Munkres

dir='/home/activatedgeek/Desktop'
matrix = []

#setup resulting matrix
def setupMatrix():
	for i in range(0,len(files)):
		temp = []
		j=0
		while j<len(files):
			temp.append(-1)
			j+=1
		matrix.append(temp)

#similarity calculation between pair of sentences
def simSubUtil(s,t):
	s = s.split(' ')
	t = t.split(' ')
	union = len(set(s).union(set(t)))
	intersection = len(set(s).intersection(set(t)))
	return float(intersection)/union

#similarity index for given pair of files
def simScore(fileapath,filebpath):
	astream = open(dir+'/'+fileapath,'r').read()
	bstream = open(dir+'/'+filebpath,'r').read()
	astream = astream.split('\n')
	bstream = bstream.split('\n')
	if len(astream)>len(bstream):
		astream, bstream = bstream, astream

	matScore = []
	for s in astream:
		temp = []
		for t in bstream:
			sWord = sWord.lower()
			tWord = tWord.lower()
			sim = simSubUtil(sWord,tWord)
			temp.append(sim)
		matScore.append(temp)

	m = Munkres()
	for i in range(len(matScore)):
		for j in range(len(matScore[i])):
			matScore[i][j] = 1 - matScore[i][j]

	results = m.compute(matScore)
	return float(len(results))/len(astream)

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


def populateMatrix(dir):
	files = getASCII(dir)
	n = len(files)
	global matrix

	for i in range(n):
		temp = []
		for j in range(i,n):
			if j==i:
				temp.append(1)
			else:
				score = simScore(file[i],file[j])

		matrix.append(temp)

class Window(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent)
		self.parent = parent
		self.initUI()

	def initUI(self):
		self.style = Style()
		self.style.theme_use("clam")
		self.pack(fill=BOTH,expand=5)
		self.parent.title("Document Similarity Checker")
		self.setButton()
		self.setupInputs()
		
	def setButton(self):
		self.quitButton = Button(self, text="Close",command=self.quit)
		self.quitButton.place(x=520, y=250)
		self.generate = Button(self, text="Generate",command=self.genButton)
		self.generate.place(x=400, y=250)

	def genButton(self):
		t = self.pathBox.get()
		if not os.path.isdir(t):
			self.generate.config(state='disabled')
		else:
			import webbrowser
			webbrowser.open('http://google.co.in/')

	def setupInputs(self):
		self.pathLabel = Label(self, text="Enter Full Directory Path", font=("Helvetica", 12))
		self.pathLabel.place(x=10, y=10)
		self.pathBox = Entry()
		self.pathBox.place(x=200,y=10,width=400,height=30)

		self.aLabel = Label(self, text="Alpha", font=("Helvetica", 12))
		self.aLabel.place(x=10, y=50)
		self.aEntry = Entry()
		self.aEntry.place(x=200,y=50,width=400,height=30)

		self.bLabel = Label(self, text="Beta", font=("Helvetica", 12))
		self.bLabel.place(x=10, y=100)
		self.bEntry = Entry()
		self.bEntry.place(x=200,y=100,width=400,height=30)

		
def main():
	root = Tk()
	root.geometry("650x300+200+200")
	app = Window(root)
	root.resizable(0,0)
	root.mainloop()

if __name__=='__main__':
	main()
