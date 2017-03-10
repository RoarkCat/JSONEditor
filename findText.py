from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class FindText():

	def __init__(self, writableBox, wordToSearchFor, singleWordToSearchFor, positionTracker, indexTracker, replaceAllWord, replaceSingleWord):
		super().__init__()
		self.counter = 0
		self.writableBox = writableBox
		self.wordToSearchFor = wordToSearchFor
		self.singleWordToSearchFor = singleWordToSearchFor
		self.doReplace = False
		self.singlePositionTracker = positionTracker
		self.singleIndexTracker = indexTracker
		self.replaceAllWord = replaceAllWord
		self.replaceSingleWord = replaceSingleWord

	#Finds every instance of the word in the wordToSearchFor box.
	def findAll(self):
		if self.wordToSearchFor is not "":
			cursor = self.writableBox.textCursor()
			format = QTextCharFormat()
			format.setBackground(QBrush(QColor(255,255,255,255)))
			cursor.setPosition(0)
			cursor.movePosition(QTextCursor.End, 1)
			cursor.mergeCharFormat(format)
			format.setBackground(QBrush(QColor(255,0,180,150)))
			regexp = QRegExp(self.wordToSearchFor)
			pos = 0
			index = regexp.indexIn(self.writableBox.toPlainText(), pos)
			while (index != -1):
				cursor.setPosition(index)
				cursor.movePosition(QTextCursor.NextCharacter, QTextCursor.KeepAnchor, len(self.wordToSearchFor))
				if self.doReplace:
					cursor.removeSelectedText()
					cursor.insertText(self.replaceAllWord)
				else:
					cursor.mergeCharFormat(format)
				pos = index + regexp.matchedLength()
				index = regexp.indexIn(self.writableBox.toPlainText(), pos)
				self.counter += 1
		else:
			msgBox = QMessageBox(QMessageBox.Warning, "Oops!", "You didn't enter anything to search for!")
			msgBox.exec_()

	#Finds only the next instance of the word in the singleWordToSearchFor box.
	def findNext(self):
		cursor = self.writableBox.textCursor()

		format = QTextCharFormat()
		format.setBackground(QBrush(QColor(255,255,255,255)))
		cursor.setPosition(0)
		cursor.movePosition(QTextCursor.End, 1)
		cursor.mergeCharFormat(format)
		format.setBackground(QBrush(QColor(255,0,180,150)))

		regexp = QRegExp(self.singleWordToSearchFor)

		self.singleIndexTracker = regexp.indexIn(self.writableBox.toPlainText(), self.singlePositionTracker)

		if self.singleIndexTracker != -1:
			cursor.setPosition(self.singleIndexTracker)
			cursor.movePosition(QTextCursor.NextCharacter, QTextCursor.KeepAnchor, len(self.singleWordToSearchFor))
			cursor.mergeCharFormat(format)
			self.singlePositionTracker = self.singleIndexTracker + regexp.matchedLength()
			self.counter += 1
		else:
			msgBox = QMessageBox(QMessageBox.Warning, "Found 'em all!", "Reached the end of the document!")
			msgBox.exec_()
			self.singleIndexTracker = 0
			self.singlePositionTracker = 0

	#Replaces all selected words with the word in the replaceAllWord box.
	def replaceAll(self):
		if self.wordToSearchFor is not "":
			self.doReplace = True
			self.findAll()
			self.doReplace = False
		else:
			msgBox = QMessageBox(QMessageBox.Warning, "Oops!", "Nothing is selected to replace!")
			msgBox.exec_()

	#Replaces the selected word with the word in the replaceSingleWord box.
	def replaceSingle(self):
		if self.singleIndexTracker > 0:
			cursor = self.writableBox.textCursor()
			cursor.setPosition(self.singleIndexTracker)
			cursor.movePosition(QTextCursor.NextCharacter, QTextCursor.KeepAnchor, len(self.singleWordToSearchFor))
			cursor.removeSelectedText()
			cursor.insertText(self.replaceSingleWord)
		else:
			msgBox = QMessageBox(QMessageBox.Warning, "Oops!", "Nothing is selected to replace!")
			msgBox.exec_()

	#Track and return values for use in the editMenuManagement class.
	def getCounter(self):
		return self.counter

	def getPosition(self):
		return self.singlePositionTracker

	def getIndex(self):
		return self.singleIndexTracker