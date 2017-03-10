import sys
import json
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from mainWindow import *
from saveAndWriteJSON import *

#This class manages all GUI functions created within the create menu.
class CreateMenuManagement(QHBoxLayout):

	#These variables help track and index the dynamically generated widgets in the create menu.
	listOfHboxes = []
	indentationList = ["Object"]
	listOfHboxTypes = []
	currentRow = 0
	indentionLength = 0
	nestedObjects = False
	nestedObjectLevel = 0
	tabCounter = 1

	#Init establishes the base buttons (create object/array/value, delete most recent row, save, generate)
	#Main function runs the updateHBoxWidgetsObjects function one time to generate the initial row.
	def __init__(self, textBox, mainWindow):

		super().__init__()
		self.initEditableVBox()
		self.x_button = QPushButton("")
		self.x_button.setIcon(QIcon("xImage.png"))
		self.x_button.setMaximumWidth(50)
		self.writableBox = textBox;
		self.parentWindow = mainWindow;

		horizontal_object_layout = QHBoxLayout()
		horizontal_object_layout.addWidget(self.x_button)
		horizontal_object_layout.setAlignment(Qt.AlignCenter)

		self.x_button.clicked.connect(lambda: self.x_button_hit(self.listOfHboxes[self.currentRow - 1]))

		self.wholeVbox.addLayout(horizontal_object_layout)

		self.value_button = QPushButton("Value")
		self.value_button.setMaximumWidth(50)
		self.object_button = QPushButton("Object")
		self.object_button.setMaximumWidth(50)
		self.array_button = QPushButton("Array")
		self.array_button.setMaximumWidth(50)

		horizontal_object_layout2 = QHBoxLayout()
		horizontal_object_layout2.addWidget(self.value_button)
		horizontal_object_layout2.addWidget(self.object_button)
		horizontal_object_layout2.addWidget(self.array_button)
		horizontal_object_layout2.setAlignment(Qt.AlignCenter)

		self.value_button.clicked.connect(self.updateHBoxWidgetsValue)
		self.object_button.clicked.connect(self.updateHBoxWidgetsObjects)
		self.array_button.clicked.connect(self.updateHBoxWidgetsArray)

		self.wholeVbox.addLayout(horizontal_object_layout2)

		self.generate_json_button = QPushButton("Generate JSON")
		self.save_button = QPushButton("Save Generated JSON")

		horizontal_object_layout3 = QHBoxLayout()
		horizontal_object_layout3.addWidget(self.generate_json_button)
		horizontal_object_layout3.addWidget(self.save_button)
		horizontal_object_layout3.setAlignment(Qt.AlignCenter)

		self.save_button.clicked.connect(self.saveJSON)
		self.generate_json_button.clicked.connect(self.printAllList)		
		self.wholeVbox.addLayout(horizontal_object_layout3)

	#Creates a scrollable vbox in case there are a lot of widgets created.
	def initEditableVBox(self):
		self.wholeVbox = QVBoxLayout()
		self.fillout_info_layout = QVBoxLayout()
		self.fillout_info_layout.setAlignment(Qt.AlignTop)
		self.scrollable_area = QScrollArea()
		self.scrollable_area.setWidgetResizable(True)
		self.frameBox = QFrame(self.scrollable_area)
		self.frameBox.setLayout(self.fillout_info_layout)
		self.scrollable_area.setWidget(self.frameBox)
		self.wholeVbox.addWidget(self.scrollable_area)

	#Returns the layout so that it can be added to the grid in the main function.
	def getFilloutInfoLayout(self):
		return self.wholeVbox

	#This function tracks indentation levels for widgets. Pretty sloppy and can be improved.
	#Add ability to collapse sections based on indentation if time.
	def trackIndentation(self, currentHBoxType):
		if self.indentationList[0] == "Object":
			self.indentationList.append(currentHBoxType)
			if self.currentRow != 0:
				self.indentionLength += 1

		elif self.indentationList[0] == "Value":
			self.indentationList.append(currentHBoxType)
			if self.indentationList[1] == "Value":
				pass
			elif self.indentationList[1] == "Object" and self.indentionLength > 0:
				self.indentionLength -= 1
			elif self.indentationList[1] == "Array":
				self.indentionLength += 1
			elif self.indentationList[1] == "ArrayObject":
				self.indentionLength -= 1

		elif self.indentationList[0] == "Array":
			self.indentationList.append(currentHBoxType)
			if self.indentationList[1] == "ArrayObject":
				self.indentionLength += 1
			elif self.indentationList[1] == "Object":
				self.indentionLength -= 1
			elif self.indentationList[1] == "Value":
				self.indentionLength += 1

		elif self.indentationList[0] == "ArrayObject":
			self.indentationList.append(currentHBoxType)
			self.indentionLength += 1

		self.indentationList.pop(0)

		return self.indentionLength

	#Generates an HBox with an object property. Objects can be followed by an ARRAY or a VALUE.
	def updateHBoxWidgetsObjects(self):
		if self.currentRow > 0 and self.listOfHboxTypes[self.currentRow - 1] == "Object":
			msgBox = QMessageBox(QMessageBox.Warning, "Whoops!", "You're trying to add an object to an object!\n To nest objects, use the 'Array' button.")
			msgBox.exec_()
		else:
			self.initial_object_label = QLabel("Object: ")
			self.initial_object_line_edit = QLineEdit() 

			horizontal_object_layout = QHBoxLayout()
			horizontal_object_layout.addStretch(self.trackIndentation("Object"))
			horizontal_object_layout.addWidget(self.initial_object_label)
			horizontal_object_layout.addWidget(self.initial_object_line_edit)
			horizontal_object_layout.addStretch(8)

			self.listOfHboxes.append(horizontal_object_layout)
			self.listOfHboxTypes.append("Object")

			self.fillout_info_layout.addLayout(self.listOfHboxes[self.currentRow])
			self.currentRow += 1

	#Generates an HBox with an array property. Arrays will be empty lists ([]) if left blank. Otherwise they can have an object or value array.
	def updateHBoxWidgetsArray(self):
		if self.listOfHboxTypes[self.currentRow - 1] == "Value" or self.listOfHboxTypes[self.currentRow - 1] == "Array":
			msgBox = QMessageBox(QMessageBox.Warning, "Whoops!", "You're trying to add an array to an existing array or a value!\n Nesting arrays is not supported.")
			msgBox.exec_()
		else:
			self.initial_array_label = QLabel("Array size: ")
			self.initial_array_line_edit = QLineEdit()
			self.array_radio_group = QGroupBox("Choose an array type:")
			self.array_radio_buttons = QButtonGroup()
			self.array_radio_button_list = []
			self.array_radio_button_list.append(QRadioButton("Object"))
			self.array_radio_button_list.append(QRadioButton("Value"))
			self.array_create_button = QPushButton("+")
			self.array_create_button.setMaximumWidth(50)


			horizontal_object_layout = QHBoxLayout()
			horizontal_object_layout.addStretch(self.trackIndentation("Array"))
			horizontal_object_layout.addWidget(self.initial_array_label)
			horizontal_object_layout.addWidget(self.initial_array_line_edit)

			self.array_radio_button_layout = QHBoxLayout()

			counter = 1
			for each in self.array_radio_button_list:
				self.array_radio_button_layout.addWidget(each)
				self.array_radio_buttons.addButton(each)
				self.array_radio_buttons.setId(each, counter)
				counter += 1

			self.array_radio_group.setLayout(self.array_radio_button_layout)
			horizontal_object_layout.addWidget(self.array_radio_group)

			horizontal_object_layout.addWidget(self.array_create_button)
			horizontal_object_layout.addStretch(8)

			self.array_create_button.clicked.connect(lambda: self.instantiate_chosen_array(self.array_radio_buttons.checkedId(), self.initial_array_line_edit.text()))

			self.listOfHboxes.append(horizontal_object_layout)
			self.listOfHboxTypes.append("Array")

			self.fillout_info_layout.addLayout(self.listOfHboxes[self.currentRow])
			self.currentRow += 1

	#Error catching in case the user enters a non-int value in an array box.
	def arrayBoxIsInt(self, stringToCheck):
		try: 
			int(stringToCheck)
			return True
		except ValueError:
			return False
			
	#Generate the chosen number of values or arrays. Error check in case a non-int is entered.
	def instantiate_chosen_array(self, chosenID, numberToSpawn):
		if chosenID == 1 and self.arrayBoxIsInt(numberToSpawn):
			for x in range(0, int(numberToSpawn)):
				self.createArrayOfObjects()
			self.indentionLength -= 2
		elif chosenID == 2 and self.arrayBoxIsInt(numberToSpawn):
			for x in range(0, int(numberToSpawn)):
				self.createArrayOfValues()
			self.indentionLength -= 1			
		elif not self.arrayBoxIsInt(numberToSpawn):
			msgBox = QMessageBox(QMessageBox.Warning, "Whoops!", "You entered a non integer value into an array!\n Make sure you only have whole numbers in arrays.")
			msgBox.exec_()

	#Sloppy workaround to create objects for arrays. Needs to be different because of indentation tracking wonkiness. Rework if time.
	def createArrayOfObjects(self):
		self.array_object_label = QLabel("Object: ")
		self.array_object_line_edit = QLineEdit()
		horizontal_object_layout = QHBoxLayout()
		horizontal_object_layout.addStretch(self.trackIndentation("ArrayObject"))
		horizontal_object_layout.addWidget(self.array_object_label)
		horizontal_object_layout.addWidget(self.array_object_line_edit)
		horizontal_object_layout.addStretch(8)

		self.listOfHboxes.append(horizontal_object_layout)
		self.listOfHboxTypes.append("Object")

		self.fillout_info_layout.addLayout(self.listOfHboxes[self.currentRow])
		self.currentRow += 1

		self.updateHBoxWidgetsValue()

	#Also a sloppy patch to create values for arrays. Fix if time.
	def createArrayOfValues(self):
		self.value_object_label = QLabel("Value: ")
		self.value_object_line_edit = QLineEdit()

		horizontal_object_layout = QHBoxLayout()
		horizontal_object_layout.addStretch(self.trackIndentation("Value"))
		horizontal_object_layout.addWidget(self.value_object_label)
		horizontal_object_layout.addWidget(self.value_object_line_edit)
		horizontal_object_layout.addStretch(8)
		self.listOfHboxes.append(horizontal_object_layout)
		self.listOfHboxTypes.append("Value")

		self.fillout_info_layout.addLayout(self.listOfHboxes[self.currentRow])
		self.currentRow += 1

	#Create an HBox with a value property. Values can only follow OBJECTS unless added with an Array (which doesn't call this function anyways).
	def updateHBoxWidgetsValue(self):
		if self.listOfHboxTypes[self.currentRow - 1] == "Array":
			msgBox = QMessageBox(QMessageBox.Warning, "Whoops!", "You're trying to add a value after an array!\n Type in the number of values you want in the array, check the value button, and then hit the '+' instead.")
			msgBox.exec_()
		elif self.listOfHboxTypes[self.currentRow - 1] == "Value":
			msgBox = QMessageBox(QMessageBox.Warning, "Whoops!", "You're trying to add a value after a value!\n Objects can only have one value. If you want an object to have more than one value, use an array.")
			msgBox.exec_()
		else:
			self.value_object_label = QLabel("Value: ")
			self.value_object_line_edit = QLineEdit()

			horizontal_object_layout = QHBoxLayout()
			horizontal_object_layout.addStretch(self.trackIndentation("Value"))
			horizontal_object_layout.addWidget(self.value_object_label)
			horizontal_object_layout.addWidget(self.value_object_line_edit)
			horizontal_object_layout.addStretch(8)
			self.listOfHboxes.append(horizontal_object_layout)
			self.listOfHboxTypes.append("Value")

			self.fillout_info_layout.addLayout(self.listOfHboxes[self.currentRow])
			self.currentRow += 1

	#This function deletes the most recently created HBox and cleans up the necessary lists / indention values.
	def x_button_hit(self, layoutToKill):
		if self.currentRow == 1:
			pass
		else:
			for n in reversed(range(layoutToKill.count())):
				widget = layoutToKill.takeAt(n).widget()
				if widget is not None:
					widget.deleteLater()
	
				for i in range(self.fillout_info_layout.count()):
					layout_item = self.fillout_info_layout.itemAt(i)
					if layout_item.layout() == layoutToKill:
						self.fillout_info_layout.removeItem(layout_item)

			self.currentRow -= 1
			if self.listOfHboxTypes[self.currentRow] == "Object" and self.indentionLength >= 1 and self.listOfHboxTypes[self.currentRow - 1] != "Value":
				self.indentionLength -= 1
			elif self.listOfHboxTypes[self.currentRow] == "Array" and self.indentionLength >= 1:
				self.indentionLength -= 1
			elif self.listOfHboxTypes[self.currentRow] == "Value" and self.listOfHboxTypes[self.currentRow - 1] == "Object" and self.indentionLength >= 1:
				self.indentionLength -= 1
			if self.listOfHboxTypes[self.currentRow] == "Object" and self.listOfHboxTypes[self.currentRow - 1] == "Value":
				self.indentionLength += 1
			self.indentationList.append(self.listOfHboxTypes[self.currentRow - 1])
			self.indentationList.pop(0)
			self.listOfHboxTypes.pop()
			self.listOfHboxes.pop()

	#Writes JSON to the text box. See saveAndWriteJSON + SaveAndWriteJSON class for more info.
	def printAllList(self):
		jsonMaker = SaveAndWriteJSON(self.writableBox, self.parentWindow)
		jsonMaker.writeJSON(self.listOfHboxes, self.listOfHboxTypes)

	#Saves JSON from the text box. See saveAndWriteJSON + SaveAndWriteJSON class for more info.
	def saveJSON(self):
		jsonMaker = SaveAndWriteJSON(self.writableBox, self.parentWindow)
		jsonMaker.makeJSON()