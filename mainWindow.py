import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from createMenuManagement import *
from editMenuManagement import *
from compareMenuManagement import *

class MainWindow(QMainWindow):

	currentRow = 0
	tabCounter = 1

	def __init__(self):
		super().__init__()
		self.first_pass_creation()


#------------------------WINDOW SETUP---------------------------------------
	def first_pass_creation(self):
		self.setWindowTitle("World's Coolest JSON Editor")
		self.create_main_selection_menu()
		self.setGeometry(600, 150, 600, 600)

		self.stacked_layout = QStackedLayout()
		self.stacked_layout.addWidget(self.button_selection_widget)
		self.create_create_menu()
		self.stacked_layout.addWidget(self.create_layout_widget)
		self.create_edit_menu()
		self.stacked_layout.addWidget(self.edit_layout_widget)
		self.create_compare_menu()
		self.stacked_layout.addWidget(self.compare_layout_widget)

		self.central_widget = QWidget()
		self.central_widget.setLayout(self.stacked_layout)
		self.setCentralWidget(self.central_widget)
		self.showMaximized()

	def create_main_selection_menu(self):
		createPix = QPixmap("newFileImage.png")
		editPix = QPixmap("editFileImage.png")
		comparePix = QPixmap("compareFileImage.png")

		self.create_button = QPushButton("Create JSON")
		self.create_button.setIcon(QIcon(createPix))
		self.create_button.setIconSize(createPix.rect().size())
		self.create_button.setMaximumWidth(300)
		self.create_button.setMinimumHeight(200)

		self.edit_button = QPushButton("Edit JSON")
		self.edit_button.setIcon(QIcon(editPix))
		self.edit_button.setIconSize(editPix.rect().size())
		self.edit_button.setMaximumWidth(300)
		self.edit_button.setMinimumHeight(200)

		self.compare_button = QPushButton("Compare / Diff JSON")
		self.compare_button.setIcon(QIcon(comparePix))
		self.compare_button.setIconSize(comparePix.rect().size())
		self.compare_button.setMaximumWidth(300)
		self.compare_button.setMinimumHeight(200)

		self.initial_layout = QVBoxLayout()
		self.initial_layout.addStretch(1)
		self.initial_layout.addWidget(self.create_button)
		self.initial_layout.addSpacing(100)
		self.initial_layout.addWidget(self.edit_button)
		self.initial_layout.addSpacing(100)
		self.initial_layout.addWidget(self.compare_button)
		self.initial_layout.addStretch(1)
		self.initial_layout.setAlignment(Qt.AlignCenter)

		self.button_selection_widget = QWidget()
		self.button_selection_widget.setLayout(self.initial_layout)

		self.create_button.clicked.connect(self.create_button_hit)
		self.edit_button.clicked.connect(self.edit_button_hit)
		self.compare_button.clicked.connect(self.compare_button_hit)

	def create_create_menu(self):
		self.back_button = QPushButton("Back to main menu")
		self.text_edit_create = QTextEdit()
		#self.text_edit_create.setTextColor(Qt.green)

		hboxClass = CreateMenuManagement(self.text_edit_create, self)
		hboxClass.updateHBoxWidgetsObjects()
		vboxForGrid = hboxClass.getFilloutInfoLayout()

		self.create_layout = QGridLayout()
		self.create_layout.setSpacing(10)
		self.create_layout.addWidget(self.back_button,1,0)
		self.create_layout.addWidget(self.text_edit_create,0,1)
		self.create_layout.addLayout(vboxForGrid,0,0)

		self.create_layout_widget = QWidget()
		self.create_layout_widget.setLayout(self.create_layout)
		self.back_button.clicked.connect(self.back_button_hit)

	def create_edit_menu(self):
		self.back_button = QPushButton("Back to main menu")
		self.text_edit_edit = QTextEdit()

		editMenuInstance = EditMenuManagement(self.text_edit_edit, self)
		vboxForGrid = editMenuInstance.getFilloutInfoLayout()

		self.edit_layout = QGridLayout()
		self.edit_layout.addWidget(self.back_button,1,0)
		self.edit_layout.addWidget(self.text_edit_edit,0,1)
		self.edit_layout.addLayout(vboxForGrid,0,0)

		self.edit_layout_widget = QWidget()
		self.edit_layout_widget.setLayout(self.edit_layout)

		self.back_button.clicked.connect(self.back_button_hit)

	def create_compare_menu(self):
		self.back_button = QPushButton("Back to main menu")

		compareMenuInstance = CompareMenuManagement(self)
		leftVbox = compareMenuInstance.getLeftVbox()
		rightVbox = compareMenuInstance.getRightVbox()
		infoLabel = compareMenuInstance.getLowerRightVbox()

		leftBoxWidget = QWidget()
		leftBoxWidget.setLayout(leftVbox)
		leftBoxWidget.resize(500,600)

		rightBoxWidget = QWidget()
		rightBoxWidget.setLayout(rightVbox)
		rightBoxWidget.resize(500,600)

		self.compare_layout = QHBoxLayout()
		self.compare_layout.addWidget(leftBoxWidget)
		self.compare_layout.addWidget(rightBoxWidget)

		self.compare_grid_layout = QGridLayout()
		self.compare_grid_layout.setSpacing(10)
		self.compare_grid_layout.addLayout(self.compare_layout,0,0,-1,-1)
		self.compare_grid_layout.addLayout(infoLabel,1,0)
		self.compare_grid_layout.addWidget(self.back_button,2,0)

		self.compare_layout_widget = QWidget()
		self.compare_layout_widget.setLayout(self.compare_grid_layout)

		self.back_button.clicked.connect(self.back_button_hit)


#---------------------BUTTON FUNCTIONS------------------------------------------------
	def create_button_hit(self):
		self.stacked_layout.setCurrentIndex(1)

	def edit_button_hit(self):
		self.stacked_layout.setCurrentIndex(2)
		#buttonFunctionsInstance = ButtonFunctions()
		#buttonFunctionsInstance.getFile(self.text_edit_edit)

	def compare_button_hit(self):
		self.stacked_layout.setCurrentIndex(3)

	def back_button_hit(self):
		self.stacked_layout.setCurrentIndex(0)

#------------------------MISC SETUP---------------------------------------
	def getVBoxLayout(self):
		return self.fillout_info_layout

	def getCreateLayout(self):
		return self.create_layout

#---------------------RUN PROGRAM-------------------------------------------------
if __name__ == "__main__":
	window_sim = QApplication(sys.argv)
	y = MainWindow()
	y.show()
	sys.exit(window_sim.exec_())