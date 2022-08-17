from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Settings import settings_dialog
from Help import help_dialog

import os
import sys

#ProxyStyle to remove tooltip delay
class MyStyle(QProxyStyle):     
    def styleHint(self, hint, option, widget, returnData):         
        if hint == QStyle.SH_ToolTip_WakeUpDelay:
            return 0
        return QProxyStyle.styleHint(self, hint, option, widget,
returnData)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.path = ''

        #App Settings
        self.getSettingsValues()

        self.setMinimumSize(QSize(800, 600))
        container = QWidget()
        layout = QVBoxLayout()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.theme = self.selected_theme.value('Theme')
        self.trans = self.translucency.value('Checked')

        if self.trans == 'On':
            self.setWindowOpacity(0.97)
        else:
            self.setWindowOpacity(1)

        #Toolbar
        app_toolbar = QToolBar()
        self.addToolBar(app_toolbar)
        app_toolbar.setMovable(False)

        self.spacer = QWidget()
        self.spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.spacer.setObjectName('spacer')

        self.spacer2 = QWidget()
        self.spacer2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.spacer2.setObjectName('spacer')

        #Settings
        self.settings = QAction(QIcon("Icons/Settings.png"), "Settings", self)
        self.settings.triggered.connect(self.show_settings_menu)
        app_toolbar.addAction(self.settings)
        
        #Settings Menu
        self.settings_menu = settings_dialog()
        self.settings_menu.closeEvent = self.settings_closed

        #Preview Button
        self.preview = QAction(QIcon("Icons/Preview_Close.png"), "Show Preview", self)
        self.preview.triggered.connect(self.preview_panel)
        app_toolbar.addAction(self.preview)
        self.preview_hidden = False

        app_toolbar.addWidget(self.spacer)

        #Filename
        self.filename = QLabel('Untitled.md')
        self.filename.setObjectName('doc')
        app_toolbar.addWidget(self.filename)

        app_toolbar.addWidget(self.spacer2)

        #Save Button
        self.save = QAction(QIcon("Icons/Save2.png"), "Save", self)
        self.save.triggered.connect(self.file_save)
        app_toolbar.addAction(self.save)
        self.save.setObjectName('right')

        #Help
        self.help = QAction(QIcon("Icons/Help.png"), "Help", self)
        self.help.triggered.connect(self.show_help_menu)
        app_toolbar.addAction(self.help)

        #Help Menu
        self.help_menu = help_dialog()

        #Editor
        mainlayout = QHBoxLayout()
        layout.addLayout(mainlayout)

        #Input Editor
        self.input_editor = QTextEdit(self,
                        placeholderText = "Type something here",
                        lineWrapColumnOrWidth = 100,
                        readOnly = False,
                        acceptRichText = False)
        self.input_editor.setContextMenuPolicy(Qt.NoContextMenu)
        mainlayout.addWidget(self.input_editor)

        #Output Editor
        self.output_editor = QTextEdit(self,
                        lineWrapColumnOrWidth = 100,
                        readOnly = True,
                        acceptRichText = False
        )
        self.output_editor.setContextMenuPolicy(Qt.NoContextMenu)
        mainlayout.addWidget(self.output_editor)
        self.output_editor.setObjectName('Output')

        #Live Preview
        self.input_editor.textChanged.connect(self.on_input_change)

    #Get User Settings
    def getSettingsValues(self):
        self.selected_theme = QSettings('noted', 'Selected Theme')
        self.translucency = QSettings('noted', 'Translucency')

    def show_settings_menu(self):
        self.settings_menu.setWindowModality(Qt.ApplicationModal)
        self.settings_menu.show()

    def show_help_menu(self):
        self.settings_menu.setWindowModality(Qt.ApplicationModal)
        self.help_menu.show()

    def settings_closed(self, event):
        self.getSettingsValues()
        self.theme = self.selected_theme.value('Theme')
        self.trans = self.translucency.value('Checked')

        if self.trans == 'On':
            self.setWindowOpacity(0.97)
        else:
            self.setWindowOpacity(1)
        
        #Updating theme after settings 
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

    #Live Preview
    def on_input_change(self):
        self.output_editor.setMarkdown(self.input_editor.toPlainText())

    #Error Message Box
    def error_dialog(self, error):
        dialog = QMessageBox(self)
        if error == 'string index out of range':
            dialog.setText("You didn't save :(")
        else:
            dialog.setText(error)
        dialog.setIcon(QMessageBox.Critical)
        dialog.show()

    #Save File
    def file_save(self):
        path = QFileDialog.getSaveFileName(self, "Save File", "", filter="Markdown Documents (*.md);;Text Documents (*.txt);;All Files (*.*)")
        text = self.input_editor.toPlainText()

        try:
            if path[0]:
                with open(path[0], 'w') as file:
                    file.write(text)
        except Exception as error:
            self.error_dialog(str(error))

        self.path = str(path[0])
        self.update_doc_title()

    #Preview 
    def preview_panel(self):
        if not self.preview_hidden:
            self.output_editor.hide()
            self.preview_hidden = True
            self.preview.setToolTip("Show Preview")
            self.preview.setIcon(QIcon('Icons/Preview_Open.png'))
        else:
            self.output_editor.show()
            self.preview_hidden = False
            self.preview.setToolTip("Close Preview")
            self.preview.setIcon(QIcon('Icons/Preview_Close.png'))

    #Update Document Name/Title
    def update_doc_title(self):
            self.setWindowTitle("%s - noted" %(os.path.basename(self.path) if self.path != '' else "Untitled.md"))
            self.filename.setText("%s" %(os.path.basename(self.path) if self.path != '' else "Untitled.md"))



if __name__ == '__main__':

#Initialize the App
    app = QApplication(sys.argv)
    app.setApplicationName("noted")
    app.setStyle(MyStyle())
    app_icon = QIcon("Icons/small_Logo.ico")
    app.setWindowIcon(app_icon)


    window = MainWindow()
    
    if window.theme == None or window.theme == 'Light Mode':
        file = QFile("Themes/light.qss")
        file.open(QFile.ReadOnly)
        stream = QTextStream(file)
        app.setStyleSheet(str(stream.readAll()))
    elif window.theme == 'Dark Mode':
        file = QFile("Themes/dark.qss")
        file.open(QFile.ReadOnly)
        stream = QTextStream(file)
        app.setStyleSheet(str(stream.readAll()))

    window.show()
    app.exec_()