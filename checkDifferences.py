from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import difflib

class FindText():

	def __init__(self, leftWritableBox, rightWritableBox):
		super().__init__()
		self.diffCounter = 0
		self.leftWritableBox = leftWritableBox
		self.rightWritableBox = rightWritableBox

	#Find diffs. Could be expanded and done better with unified_diff over context_diff, but this works for
	#a simple, quick comparison of two files with minimal detail.
	def getDifferences(self, appendableDiffs):
		leftText = self.leftWritableBox.toPlainText()
		rightText = self.rightWritableBox.toPlainText()
		diffs_found_label = QLabel("Diffs found: ")
		diffs_found_label.setStyleSheet("QLabel { color : red; }")
		appendableDiffs.addWidget(diffs_found_label)

		cursor = self.rightWritableBox.textCursor()
		format = QTextCharFormat()
		format.setBackground(QBrush(QColor(255,255,255,255)))
		cursor.setPosition(0)
		cursor.movePosition(QTextCursor.End, 1)
		cursor.mergeCharFormat(format)

		
		lines = difflib.context_diff(leftText, rightText)
		for line in lines:
			if line.startswith("---"):
				try:
					#Get values for cursor position to highlight diff.
					firstCommaIndex = line.index(",")
					secondDashIndex = line[4:].index(" -")
					secondDashIndex += 4

					format.setBackground(QBrush(QColor(255,0,0,150)))
					cursor.setPosition(int(line[4:firstCommaIndex]) + 1)
					cursor.setPosition(int(line[firstCommaIndex + 1:secondDashIndex]) - 1, QTextCursor.KeepAnchor)
					cursor.mergeCharFormat(format)

					#Create a label to append to the list.
					current_diff_label = QLabel("Change from position " + line[4:firstCommaIndex] + " to position " + line[firstCommaIndex + 1:secondDashIndex])
					current_diff_label.setStyleSheet("QLabel { color : magenta }")
					appendableDiffs.addWidget(current_diff_label)

					self.diffCounter += 1
				except ValueError:
					pass

		diffs_found_label.setText(str(self.diffCounter) + " difference(s) found.")
		return appendableDiffs