from PyQt5.QtWidgets import QDialog, QHBoxLayout, QVBoxLayout, QPushButton, QComboBox, QLabel
from PyQt5.QtCore import QSize, QSettings, QFile, QTextStream, Qt
from PyQt5.QtGui import QIcon, QPixmap
from Help import help_dialog

import webbrowser

class settings_dialog(QDialog):
        def __init__(self):
                super().__init__()
                layout = QHBoxLayout()
                self.setLayout(layout)
                self.setMinimumSize(QSize(500, 300))
                self.getSettingsValues()
                self.setWindowTitle('noted Settings')
                
                #Check and Change dialog theme
                self.theme = self.selected_theme.value('Theme')
                self.trans = self.translucency.value('Checked')

                if self.trans == 'On':
                    self.setWindowOpacity(0.97)
                else:
                    self.setWindowOpacity(1)

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


                #Options
                self.options_layout = QVBoxLayout()
                self.options_layout.setAlignment(Qt.AlignTop)
                
                self.appearance_btn = QPushButton("Appearance")
                self.appearance_btn.setObjectName('settings')
                self.appearance_btn.setCheckable(True)
                self.appearance_btn.setChecked(True)
                self.appearance_btn.clicked.connect(self.apperance_settings)
                
                self.about_btn = QPushButton("About")
                self.about_btn.setObjectName('settings')
                self.about_btn.setCheckable(True)
                self.about_btn.clicked.connect(self.about_settings)
                

                self.options_layout.addWidget(self.appearance_btn)
                self.options_layout.addWidget(self.about_btn)
                layout.addLayout(self.options_layout)

                #Options Settings
                self.ap_settings = QVBoxLayout()
                self.ap_settings.setAlignment(Qt.AlignTop)
                
                #Appearance Options
                self.select_theme = QComboBox()
                self.theme_lbl = QLabel("Choose noted's default theme:")
                self.select_theme.addItem('Light Mode')
                self.select_theme.addItem('Dark Mode')
                self.select_theme.currentIndexChanged.connect(self.set_theme)

                #Updating Theme's ComboBox
                if self.theme == 'Light Mode':
                    self.select_theme.setCurrentIndex(0) 
                elif self.theme == 'Dark Mode': 
                    self.select_theme.setCurrentIndex(1)

                self.ap_settings.addWidget(self.theme_lbl)#Adding theme widgets to appearance layout
                self.ap_settings.addWidget(self.select_theme)

                self.trans_window = QComboBox()
                self.trans_lbl = QLabel("Transluscency effect:")
                self.trans_window.addItem('Off')
                self.trans_window.addItem('On')
                self.trans_window.currentIndexChanged.connect(self.set_translucency)

                #Updating Translucency's ComboBox
                if self.trans == 'Off':
                    self.trans_window.setCurrentIndex(0)  
                elif self.trans == 'On': 
                    self.trans_window.setCurrentIndex(1)


                self.ap_settings.addWidget(self.trans_lbl)
                self.ap_settings.addWidget(self.trans_window)
                
                #About Options
                self.logo = QLabel()
                pixmap = QPixmap('Icons/noted-1.png')
                self.logo.setPixmap(pixmap)
                self.logo.resize(pixmap.width(), pixmap.height())
                self.about_noted = QLabel('noted is a very simple Markdown editor \ncreated using Python and PyQT5.')
                self.about_creator = QPushButton(QIcon('Icons\GitHub.png'), 'Check out my Github')
                self.about_creator.clicked.connect(lambda: webbrowser.open('https://github.com/tanthehack'))
                self.about_help_lbl = QLabel('Need Help?')
                self.about_help = QPushButton(QIcon('Icons\Help.png'), 'Help')
                self.about_help.clicked.connect(self.show_help_menu)

                self.ap_settings.addWidget(self.logo)
                self.ap_settings.addWidget(self.about_noted)
                self.ap_settings.addWidget(self.about_creator)
                self.ap_settings.addStretch(1)
                self.ap_settings.addWidget(self.about_help_lbl)
                self.ap_settings.addWidget(self.about_help)

                self.help_menu = help_dialog()

                self.about_noted.hide()
                self.about_creator.hide()
                self.about_help_lbl.hide()
                self.about_help.hide()
                self.logo.hide()

                
                layout.addLayout(self.ap_settings)

                
        def apperance_settings(self):
            if self.about_btn.isChecked:
                self.about_btn.setChecked(False)
                self.theme_lbl.show()
                self.select_theme.show()
                self.trans_window.show()
                self.trans_lbl.show()

                self.about_noted.hide()
                self.about_creator.hide()
                self.about_help_lbl.hide()
                self.about_help.hide()
                self.logo.hide()
                
            
        def about_settings(self):
            if self.appearance_btn.isChecked:
                self.appearance_btn.setChecked(False)
                self.about_noted.show()
                self.about_creator.show()
                self.about_help_lbl.show()
                self.about_help.show()
                self.logo.show()

                self.theme_lbl.hide()
                self.select_theme.hide()
                self.trans_window.hide()
                self.trans_lbl.hide()

        def set_translucency(self):
            trans = self.trans_window.currentText()
            self.translucency.setValue('Checked', trans)

            if trans == 'On':
                self.setWindowOpacity(0.97)
            else:
                self.setWindowOpacity(1)

        def set_theme(self):
                theme = self.select_theme.currentText()
                self.selected_theme.setValue('Theme', theme)

                if theme == 'Light Mode':
                    file = QFile("Themes/light.qss")
                    file.open(QFile.ReadOnly)
                    stream = QTextStream(file)
                    self.setStyleSheet(str(stream.readAll()))
                elif theme == 'Dark Mode':
                    file = QFile("Themes/dark.qss")
                    file.open(QFile.ReadOnly)
                    stream = QTextStream(file)
                    self.setStyleSheet(str(stream.readAll()))

        def show_help_menu(self):
            self.help_menu.show()

        def getSettingsValues(self):
            #Settings Keys
                self.selected_theme = QSettings('noted', 'Selected Theme')
                self.translucency = QSettings('noted', 'Translucency')

                self.hide()