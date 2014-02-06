#!/usr/bin/python

from Tkinter import Tk, BOTH, RIGHT,StringVar,Text,DISABLED,NORMAL
from ttk import Frame,Button,Style,Label,Entry
import os,tkFileDialog,globals

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

		self.browserButton = Button(self, text="Open Browser",command=self.browser)
		self.browserButton.place(x=400, y=250)
		self.browserButton.config(state=NORMAL)

		self.generate = Button(self, text="Generate Data",command=self.genData)
		self.generate.place(x=10, y=250)

	def browser(self):
		import webbrowser
		webbrowser.get('firefox').open('/home/activatedgeek/Desktop/fileSim/data/index.html')
		self.browserButton.config(state=DISABLED)

	def getDir(self):
		globals.dir = tkFileDialog.askdirectory(parent=self.parent,initialdir="/",title='Select a directory')
		self.selpath['text'] = globals.dir
		#print globals.dir

	#validate and process data
	def genData(self):
		valid = True
		try:
			globals.alpha = float(self.aEntry.get())
		except ValueError:
			globals.alpha = 0.0
			valid = False
		try:
			globals.beta = float(self.bEntry.get())
		except ValueError:
			globals.beta = 0.0
			valid = False

		if not os.path.isdir(globals.dir) or globals.alpha>=1.0 or globals.beta>=1.0:
			valid = False

		if valid:
			self.generate.config(state=DISABLED)
			#from compute import main as computeMain
			from jsonutil import main as jsonMain
			jsonMain()
			self.browserButton.config(state=NORMAL)
			self.generate.config(state=NORMAL)
		
def main():
	root = Tk()
	root.geometry("650x300+200+200")
	app = Window(root)
	root.resizable(0,0)
	root.mainloop()

if __name__=='__main__':
	main()