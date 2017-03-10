from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class ColorizeText():

	def __init__(self, textBox):
		super().__init__()
		self.textBox = textBox

	def colorText(self):
		allText = self.textBox.toPlainText()
		allText = list(allText)
		count = 0
		format = QTextCharFormat()
		cursor = self.textBox.textCursor()
		trackColons = True

		for character in allText:
			if character == "{" or character == "}":
				format.setForeground(QBrush(QColor(30,55,235,255)))
				cursor.setPosition(count)
				cursor.setPosition(count + 1, QTextCursor.KeepAnchor)
				cursor.mergeCharFormat(format)
			elif character == "[" or character == "]":
				format.setForeground(QBrush(QColor(30,55,235,255)))
				cursor.setPosition(count)
				cursor.setPosition(count + 1, QTextCursor.KeepAnchor)
				cursor.mergeCharFormat(format)
			elif character == ",":
				format.setForeground(QBrush(QColor(30,55,235,255)))
				cursor.setPosition(count)
				cursor.setPosition(count + 1, QTextCursor.KeepAnchor)
				cursor.mergeCharFormat(format)
			elif character == '"':
				format.setForeground(QBrush(QColor(220,40,50,255)))
				cursor.setPosition(count)
				cursor.setPosition(count + 1, QTextCursor.KeepAnchor)
				cursor.mergeCharFormat(format)
			elif character == ":":
				format.setForeground(QBrush(QColor(30,55,235,255)))
				cursor.setPosition(count)
				cursor.setPosition(count + 1, QTextCursor.KeepAnchor)
				cursor.mergeCharFormat(format)
				trackColons = not trackColons
			elif trackColons:
				format.setForeground(QBrush(QColor(108,18,245,255)))
				cursor.setPosition(count)
				cursor.setPosition(count + 1, QTextCursor.KeepAnchor)
				cursor.mergeCharFormat(format)
			else:
				format.setForeground(QBrush(QColor(245,18,108,255)))
				cursor.setPosition(count)
				cursor.setPosition(count + 1, QTextCursor.KeepAnchor)
				cursor.mergeCharFormat(format)

			count += 1

