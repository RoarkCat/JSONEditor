import sys
import json
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from colorizeText import *

class SaveAndWriteJSON(QHBoxLayout):

	def __init__(self, writableBox, parentWindow):
		super().__init__()
		self.writableBox = writableBox
		self.parentWindow = parentWindow

	#Error catching in case the user enters a non-int value in an array box.
	def arrayBoxIsInt(self, stringToCheck):
		try: 
			int(stringToCheck)
			return True
		except ValueError:
			return False

	#Clear the writable box and then write JSON to it.
	#TLDR overview: listOfHboxes has every text box at item value 2. Compare listOfHboxes with listOfHboxTypes and then add to appropriate list or dictionary.
	#This is all added to the jsonToCreate dict which is then fed into the writable box using json.dumps
	def writeJSON(self, listOfHboxes, listOfHboxTypes):
		self.writableBox.clear()

		counter = 0
		arrayCounter = 0
		numberInArray = 0
		checkForArrayEndValues = False
		skipNext = False
		makingObjects = False
		jsonToCreate = {}
		trackArrayList = []
		arrayDict = {}
		placeholderCounter = 0
		
		for box in listOfHboxes:
			if listOfHboxTypes[counter] != "Array":
				if not checkForArrayEndValues:
					try:
						textWidget = box.itemAt(2).widget()
						if listOfHboxTypes[counter] == "Object" and listOfHboxTypes[counter + 1] != "Array":
							jsonToCreate[textWidget.text()] = listOfHboxes[counter + 1].itemAt(2).widget().text()
						elif listOfHboxTypes[counter] == "Object" and listOfHboxTypes[counter + 1] == "Array":
							placeholderCounter = counter

						elif listOfHboxTypes[counter] == "Value":
							pass
					except IndexError:
						msgBox = QMessageBox(QMessageBox.Warning, "Whoops!", "You have malformed JSON data!\n Check for an object missing a value.")
						msgBox.exec_()
				else:
					textWidget = box.itemAt(2).widget()
					if listOfHboxTypes[counter] == "Object" and not skipNext:
						arrayDict[textWidget.text()] = listOfHboxes[counter + 1].itemAt(2).widget().text()
						skipNext = True
						makingObjects = True
					elif listOfHboxTypes[counter] == "Value" and not skipNext:
						trackArrayList.append(textWidget.text())
					else:
						skipNext = False
			else:
				if self.arrayBoxIsInt(box.itemAt(2).widget().text()):
					numberInArray = int(box.itemAt(2).widget().text())
					checkForArrayEndValues = True
				else:
					jsonToCreate[listOfHboxes[counter - 1].itemAt(2).widget().text()] = []

			#If we're currently cycling through an array. (This bool flips whenever listOfHboxTypes[counter] == "Array")
			if checkForArrayEndValues:
				if listOfHboxTypes[counter] == "Value":
					arrayCounter += 1				
				if numberInArray - arrayCounter == 0:
					if makingObjects:
						trackArrayList.append(arrayDict)
						instanceOfArrayList = trackArrayList
						jsonToCreate[listOfHboxes[placeholderCounter].itemAt(2).widget().text()] = instanceOfArrayList
						trackArrayList = []
						arrayDict = {}
					else:
						instanceOfArrayList = trackArrayList
						jsonToCreate[listOfHboxes[placeholderCounter].itemAt(2).widget().text()] = instanceOfArrayList
						trackArrayList = []

					checkForArrayEndValues = False
					makingObjects = False
					arrayCounter = 0
					numberInArray = 0

			counter += 1

		#Just a sanity check to make sure the JSON is never malformed. I don't think it ever could be at this point, but... maybe?
		try:
			self.writableBox.append(json.dumps(jsonToCreate, sort_keys = True, indent = 8, separators = (',', ': ')))
			colorText = ColorizeText(self.writableBox)
			colorText.colorText()
		except ValueError:
			msgBox = QMessageBox(QMessageBox.Warning, "Whoops!", "You have malformed JSON data!\n Check for an object missing a value.")
			msgBox.exec_()

	#Save out a json file from the writable text box. Saving it out here as opposed to automatically during generation so that there is a chance to manually modify the generated JSON.
	def makeJSON(self):
		saveFileName = QFileDialog.getSaveFileName(self.parentWindow, "Save File")[0]
		try:
			if saveFileName.endswith(".json"):
				pass
			else:
				saveFileName += ".json"
			saveFile = open(saveFileName, "w")
			text = self.writableBox.toPlainText()
			saveFile.write(text)
			saveFile.close()
			print("success")
		except TypeError:
			print("error")
			pass
