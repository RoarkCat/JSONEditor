import sys
import json
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from mainWindow import *
from loadJSON import *
from checkDifferences import *

#This class manages all GUI functions created within the create menu.
class CompareMenuManagement(QHBoxLayout):


	#Init has the main text box generated in mainWindow and a reference to the parent window.
	#positionTracker and indexTracker get passed into the findText program to track single calls for the findNext function.
	def __init__(self, mainWindow):

		super().__init__()
		self.initEditableVBox()
		self.parentWindow = mainWindow
		self.appendableDiffs = QVBoxLayout()

#------------------------WINDOW SETUP---------------------------------------
	#Create the buttons and assign functions for the comparison window.
	def initEditableVBox(self):
		self.leftVbox = QVBoxLayout()
		self.rightVbox = QVBoxLayout()
		self.left_writable_box = QTextEdit()
		self.right_writable_box = QTextEdit()
		self.load_left_json = QPushButton("Load base file")
		self.load_left_json.setMaximumWidth(150)
		self.load_right_json = QPushButton("Load file to compare")
		self.load_right_json.setMinimumWidth(150)
		self.load_right_json.setMaximumWidth(150)
		self.compare_json_button = QPushButton("Compare JSON files")
		self.compare_json_button.setMinimumWidth(150)
		self.compare_json_button.setMaximumWidth(150)

		self.leftVbox.addWidget(self.left_writable_box)
		self.leftVbox.addWidget(self.load_left_json)
		compareButtonHBox = QHBoxLayout()
		
		compareButtonHBox.setAlignment(Qt.AlignRight)
		self.leftVbox.addLayout(compareButtonHBox)
		self.leftVbox.addSpacing(150)

		self.rightVbox.addWidget(self.right_writable_box)
		compareButtonHBox2 = QHBoxLayout()
		compareButtonHBox2.addWidget(self.load_right_json)
		compareButtonHBox2.setAlignment(Qt.AlignRight)
		self.rightVbox.addLayout(compareButtonHBox2)
		self.rightVbox.addSpacing(150)

		buttonFunctionsInstance = LoadJSON()

		self.load_left_json.clicked.connect(lambda: buttonFunctionsInstance.getFile(self.left_writable_box))
		self.load_right_json.clicked.connect(lambda: buttonFunctionsInstance.getFile(self.right_writable_box))
		self.compare_json_button.clicked.connect(self.compareJSON)

		#Create a small scrollable window that will expand in case tons of diffs are found.
		self.comparisonVbox = QVBoxLayout()
		self.comparisonVbox.addStretch(1)
		self.fillout_info_layout = QVBoxLayout()
		self.fillout_info_layout.setAlignment(Qt.AlignCenter)
		self.scrollable_area = QScrollArea()
		self.scrollable_area.setWidgetResizable(True)
		self.frameBox = QFrame(self.scrollable_area)
		self.frameBox.setLayout(self.fillout_info_layout)
		self.scrollable_area.setWidget(self.frameBox)
		quickAddVbox = QVBoxLayout()
		quickAddVbox.addWidget(self.compare_json_button)
		quickAddVbox.setAlignment(Qt.AlignCenter)
		self.comparisonVbox.addLayout(quickAddVbox)
		self.comparisonVbox.addWidget(self.scrollable_area)


#------------------------BUTTON SETUP---------------------------------------
	def compareJSON(self):
		diffChecker = FindText(self.left_writable_box, self.right_writable_box)
		
		for n in reversed(range(self.appendableDiffs.count())):
			widget = self.appendableDiffs.takeAt(n).widget()
			if widget is not None:
				widget.deleteLater()

			for i in range(self.fillout_info_layout.count()):
				layout_item = self.fillout_info_layout.itemAt(i)
				self.fillout_info_layout.removeItem(layout_item)

		addableDiffLayout = diffChecker.getDifferences(self.appendableDiffs)

		self.fillout_info_layout.addLayout(addableDiffLayout)

#------------------------MISC SETUP---------------------------------------
	def getLeftVbox(self):
		return self.leftVbox

	def getRightVbox(self):
		return self.rightVbox

	def getLowerRightVbox(self):
		return self.comparisonVbox