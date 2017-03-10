import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from colorizeText import *

class LoadJSON(QMainWindow):

	def __init__(self):
		super().__init__()

	#Load json into the given textBox.
	def getFile(self, textBox):
		printableEdit = []
		theFile = QFileDialog.getOpenFileName(self, "Open file", "/home")[0]
		try:
			readFile = open(theFile).read()

			for line in readFile:
				printableEdit.append(line)

			printableEdit = "".join(printableEdit)

			textBox.setText(printableEdit)
			textColor = ColorizeText(textBox)
			textColor.colorText()

		except FileNotFoundError:
			pass
