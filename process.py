#!/usr/bin/python

from Tkinter import Tk, BOTH, RIGHT,StringVar,Text
from ttk import Frame,Button,Style,Label,Entry
import os,tkFileDialog

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
		self.dir = "Choose a directory"
		self.setupInputs()
		self.setButton()
	
	def setupInputs(self):
		self.chooseDir = Button(self, text="Choose",command=self.getDir)
		self.chooseDir.place(x=10, y=10)
		self.selpath = Label(self, text=self.dir, font=("Helvetica", 12))
		self.selpath.place(x=150, y=10)

		self.aLabel = Label(self, text="Alpha", font=("Helvetica", 12))
		self.aLabel.place(x=10, y=50)
		self.aEntry = Entry()
		self.aEntry.place(x=200,y=50,width=400,height=30)

		self.bLabel = Label(self, text="Beta", font=("Helvetica", 12))
		self.bLabel.place(x=10, y=100)
		self.bEntry = Entry()
		self.bEntry.place(x=200,y=100,width=400,height=30)

	def setButton(self):
		self.quitButton = Button(self, text="Close",command=self.quit)
		self.quitButton.place(x=520, y=250)
		self.generate = Button(self, text="Generate",command=self.genButton)
		self.generate.place(x=400, y=250)

	def genButton(self):
		import webbrowser
		#print "Opening browser..."
		webbrowser.open('http://www.iith.ac.in/')

	def getDir(self):
		self.dir = tkFileDialog.askdirectory(parent=self.parent,initialdir="/",title='Select a directory')
		self.selpath['text'] = self.dir

		
def main():
	root = Tk()
	root.geometry("650x300+200+200")
	app = Window(root)
	root.resizable(0,0)
	root.mainloop()

if __name__=='__main__':
	main()