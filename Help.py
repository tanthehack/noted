from PyQt5.QtWidgets import QDialog, QHBoxLayout, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import QSize, QSettings, QFile, QTextStream
from PyQt5.QtGui import QIcon

import webbrowser

class help_dialog(QDialog):
        def __init__(self):
                super().__init__()
                layout = QVBoxLayout()
                self.setLayout(layout)
                self.setMinimumSize(QSize(300, 150))
                self.getSettingsValues()
                self.setWindowTitle('noted Help')
                
                #Check and Change dialog theme
                self.theme = self.selected_theme.value('Theme')

                if self.theme == None or self.theme == 'Light Mode':
                    file = QFile("Themes/light.qss")
                    file.open(QFile.ReadOnly)
                    stream = QTextStream(file)
                    self.setStyleSheet(str(stream.readAll()))
                elif self.theme == 'Dark Mode':
                    file = QFile("Themes/dark.qss")
                    file.open(QFile.ReadOnly)
                    stream = QTextStream(file)
                    self.setStyleSheet(str(stream.readAll()))

                #Markdown Tutorial
                mk_layout = QHBoxLayout()
                self.mk_tut = QPushButton(QIcon('Icons/Markdown_doc.png'),"MarkDown Tutorial \nOpen official Github Markdown", self)
                self.mk_tut.clicked.connect(lambda: webbrowser.open('https://www.markdownguide.org'))
                self.mk_tut.setObjectName('mk')
                layout.addWidget(self.mk_tut)


        def getSettingsValues(self):
            #Settings Keys
                self.selected_theme = QSettings('noted', 'Selected Theme')

                self.hide()