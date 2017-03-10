import sys
import json
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from mainWindow import *
from loadJSON import *
from findText import *
from saveAndWriteJSON import *

#This class manages all GUI functions created within the create menu.
class EditMenuManagement(QHBoxLayout):


	#Init has the main text box generated in mainWindow and a reference to the parent window.
	#positionTracker and indexTracker get passed into the findText program to track single calls for the findNext function.
	def __init__(self, textBox, mainWindow):

		super().__init__()
		self.initEditableVBox()
		self.writableBox = textBox
		self.parentWindow = mainWindow
		self.positionTracker = 0
		self.indexTracker = 0

#------------------------WINDOW SETUP---------------------------------------
	#Create the buttons and assign functions for the edit window.
	def initEditableVBox(self):
		self.wholeVbox = QVBoxLayout()
		self.load_json = QPushButton("Load a JSON file")
		self.load_json.setMaximumWidth(150)
		self.find_all_button = QPushButton("Find all:")
		self.find_all_button.setMaximumWidth(150)
		self.find_all_text_field = QLineEdit()
		self.find_all_text_field.setMaximumWidth(300)
		self.replace_all_with_button = QPushButton("Replace all with:")
		self.replace_all_with_button.setMaximumWidth(150)
		self.replace_all_with_text_field = QLineEdit()
		self.replace_all_with_text_field.setMaximumWidth(300)
		self.instances_found_label = QLabel("")
		self.find_next_index_of_button = QPushButton("Find next index of:")
		self.find_next_index_of_button.setMaximumWidth(150)
		self.find_next_index_of_text_field = QLineEdit()
		self.find_next_index_of_text_field.setMaximumWidth(300)
		self.replace_selected_with_button = QPushButton("Replace selected with:")
		self.replace_selected_with_button.setMaximumWidth(150)
		self.replace_selected_with_text_field = QLineEdit()
		self.replace_selected_with_text_field.setMaximumWidth(300)
		self.save_json = QPushButton("Save current JSON")
		self.save_json.setMaximumWidth(150)

		horizontal_layout = QHBoxLayout()
		horizontal_layout.addWidget(self.load_json)
		horizontal_layout.addWidget(self.save_json)

		horizontal_layout2 = QHBoxLayout()
		horizontal_layout2.addWidget(self.find_all_button)
		horizontal_layout2.addWidget(self.instances_found_label)

		self.wholeVbox.addStretch(1)
		self.wholeVbox.addLayout(horizontal_layout2)
		self.wholeVbox.addWidget(self.find_all_text_field)
		self.wholeVbox.addSpacing(50)
		self.wholeVbox.addWidget(self.replace_all_with_button)
		self.wholeVbox.addWidget(self.replace_all_with_text_field)
		self.wholeVbox.addSpacing(200)
		self.wholeVbox.addWidget(self.find_next_index_of_button)
		self.wholeVbox.addWidget(self.find_next_index_of_text_field)
		self.wholeVbox.addSpacing(50)
		self.wholeVbox.addWidget(self.replace_selected_with_button)
		self.wholeVbox.addWidget(self.replace_selected_with_text_field)
		self.wholeVbox.addStretch(1)
		self.wholeVbox.addLayout(horizontal_layout)
		self.wholeVbox.setAlignment(Qt.AlignCenter)

		buttonFunctionsInstance = LoadJSON()

		self.load_json.clicked.connect(lambda: buttonFunctionsInstance.getFile(self.writableBox))
		self.find_all_button.clicked.connect(self.findAll)
		self.replace_all_with_button.clicked.connect(self.replaceAll)
		self.find_next_index_of_button.clicked.connect(self.findNext)
		self.replace_selected_with_button.clicked.connect(self.replaceNext)
		self.save_json.clicked.connect(self.saveJSON)

#------------------------BUTTON SETUP---------------------------------------
	def findAll(self):
		findText = FindText(self.writableBox, self.find_all_text_field.text(), self.find_next_index_of_text_field.text(), self.positionTracker, self.indexTracker, self.replace_all_with_text_field.text(), self.replace_selected_with_text_field.text())
		findText.findAll()
		counter = findText.getCounter()
		self.instances_found_label.setText("Found " + str(counter) + " instance(s)!")

	def replaceAll(self):
		findText = FindText(self.writableBox, self.find_all_text_field.text(), self.find_next_index_of_text_field.text(), self.positionTracker, self.indexTracker, self.replace_all_with_text_field.text(), self.replace_selected_with_text_field.text())
		findText.replaceAll()

	def findNext(self):
		findText = FindText(self.writableBox, self.find_all_text_field.text(), self.find_next_index_of_text_field.text(), self.positionTracker, self.indexTracker, self.replace_all_with_text_field.text(), self.replace_selected_with_text_field.text())
		findText.findNext()
		self.positionTracker = findText.getPosition() #Track position
		self.indexTracker = findText.getIndex() #Track index

	def replaceNext(self):
		findText = FindText(self.writableBox, self.find_all_text_field.text(), self.find_next_index_of_text_field.text(), self.positionTracker, self.indexTracker, self.replace_all_with_text_field.text(), self.replace_selected_with_text_field.text())
		findText.replaceSingle()

	def saveJSON(self):
		saver = SaveAndWriteJSON(self.writableBox, self.parentWindow)
		saver.makeJSON()

#------------------------MISC SETUP---------------------------------------
	def getFilloutInfoLayout(self):
		return self.wholeVbox