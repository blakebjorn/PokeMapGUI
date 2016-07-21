from PySide import QtCore, QtGui
import sys
import subprocess
import os
import json
import time
import webbrowser
from ast import literal_eval

if getattr(sys, 'frozen', True):
    sys.stderr = open('Errors.txt', 'a')

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowIcon(QtGui.QIcon("pokeball.png"))
        self.mainWindowWidget = QtGui.QWidget()
        self.container = QtGui.QVBoxLayout()
        self.formLayout = QtGui.QFormLayout()
        self.container.addLayout(self.formLayout)
        self.mainWindowWidget.setLayout(self.container)

        self.userNameTextBox = QtGui.QLineEdit()
        self.passwordTextBox = QtGui.QLineEdit()
        self.locationTextBox = QtGui.QLineEdit()
        self.stepsTextBox = QtGui.QLineEdit()
        self.otherCommandsTextBox = QtGui.QLineEdit()
        self.otherCommandsTextBox.setPlaceholderText("{\"flag\":\"value\", \"flag2\":\"value2\"}, optional")
        self.stepsTextBox.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)

        self.formLayout.addRow("Username:", self.userNameTextBox)
        self.formLayout.addRow("Password:", self.passwordTextBox)
        self.formLayout.addRow("Address:", self.locationTextBox)
        self.formLayout.addRow("Steps:", self.stepsTextBox)
        self.formLayout.addRow("Other Args:", self.otherCommandsTextBox)

        self.goButton = QtGui.QPushButton("GO!")
        self.goButton.setEnabled(False)
        self.goButton.clicked.connect(self.start_server)
        self.saveButton = QtGui.QPushButton("Save")
        self.saveButton.clicked.connect(self.save_settings)
        self.container.addWidget(self.saveButton)
        self.container.addWidget(self.goButton)

        self.userNameTextBox.textChanged.connect(self.text_changed)
        self.passwordTextBox.textChanged.connect(self.text_changed)
        self.locationTextBox.textChanged.connect(self.text_changed)
        self.stepsTextBox.textChanged.connect(self.text_changed)

        self.setGeometry(300,300,500,300)
        self.setWindowTitle("Pokemon GO GUI")

        self.menu = self.menuBar()
        self.statusBar()
        self.setCentralWidget(self.mainWindowWidget)

        self.threadRunning = False

        if os.path.isfile('GuiConfig.json'):
            args = json.load(open('GuiConfig.json','r'))
            if 'username' in args.keys():
                self.userNameTextBox.setText(str(args['username']))
            if 'password' in args.keys():
                self.passwordTextBox.setText(str(args['password']))
            if 'steps' in args.keys():
                self.stepsTextBox.setText(str(args['steps']))
            if 'optionalArgs' in args.keys():
                self.otherCommandsTextBox.setText(str(args['optionalArgs']))
            if 'location' in args.keys():
                self.locationTextBox.setText(str(args['location']))
            if 'sourceDirectory' in args.keys():
                self.sourceFolder = args['sourceDirectory']
            else:
                self.sourceFolder = "PokemonGo-Map-develop"
            if 'sourceScript' in args.keys():
                self.sourceScript = args['sourceScript']
            else:
                self.sourceScript = "runserver.py"
        else:
            self.sourceFolder = "PokemonGo-Map-develop"
            self.sourceScript = "runserver.py"

        try:
            os.chdir(self.sourceFolder)
        except:
            QtGui.QMessageBox.warning(self,"Error","No source folder found, place source folder in working directory and restart the application.")

        self.show()

    def save_settings(self):
        argDict = {}
        argDict["username"] = self.userNameTextBox.text()
        argDict["password"] = self.passwordTextBox.text()
        argDict["steps"] = self.stepsTextBox.text()
        location = self.locationTextBox.text()
        argDict["location"] = location
        if self.otherCommandsTextBox.text() != "":
            argDict["optionalArgs"] = self.otherCommandsTextBox.text()

        argDict["sourceDirectory"] = self.sourceFolder
        argDict["sourceScript"] = self.sourceScript

        with open(os.path.join(os.path.dirname(sys.argv[0]),'GuiConfig.json'), 'w') as fp:
            json.dump(argDict, fp)

    def text_changed(self):
        if self.stepsTextBox.text()!="" and self.userNameTextBox.text()!="" and \
            self.passwordTextBox.text()!="" and self.locationTextBox.text()!="":
            self.goButton.setEnabled(True)
        else:
            self.goButton.setEnabled(False)

    def start_server(self):
        if not self.threadRunning:
            optionalArgsText = self.otherCommandsTextBox.text()
            if not os.path.isfile('credentials.json') and "-k" not in optionalArgsText:
                QtGui.QMessageBox.information(self,"Error","credentials.json not found in source directory.\nCreate file manually or include an optional flag for your GMAPS API key:\n{\"-k\":\"API KEY IN QUOTES HERE\"}")
                return
            argsDict = {}
            argsDict['-P'] = "5000"
            argsDict['-H'] = "127.0.0.1"

            if optionalArgsText != "":
                try:
                    evalDict = literal_eval(optionalArgsText)
                    for key in evalDict.keys():
                        argsDict[key]=evalDict[key]
                except Exception as E:
                    QtGui.QMessageBox.warning(self,"Error","Couldn't parse optional arguments.\nException:\n\n"+str(E))
                    return

            argsDict['-u'] = self.userNameTextBox.text()
            argsDict['-p'] = self.passwordTextBox.text()
            argsDict['-st'] = self.stepsTextBox.text()
            argsDict['-l'] = self.locationTextBox.text()

            argsList = []
            if getattr(sys, 'frozen', True):
                argsList.append(os.path.join(os.path.dirname(sys.executable),"Python","python.exe"))
            else:
                argsList.append(sys.executable)

            argsList.append(self.sourceScript)
            for key in argsDict.keys():
                argsList.append(key)
                argsList.append(argsDict[key])

            print argsList
            self.goButton.setText("STOP!")
            self.threadRunning = True
            self.subProcess = subprocess.Popen(argsList)
            time.sleep(3)

            if not "http://" in argsDict['-H']:
                argsDict['-H']="http://"+argsDict['-H']
            webbrowser.open(str(argsDict['-H'])+":"+str(argsDict['-P']))
        else:
            self.subProcess.terminate()
            self.goButton.setText("GO!")
            self.threadRunning = False

    def closeEvent(self, event):
        try:
            self.subProcess.terminate()
        except AttributeError:
            pass
        event.accept()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    QtCore.QLocale.setDefault(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
    app.setStyle("Plastique")
    mainWin = MainWindow()
    mainWin.show()
    mainWin.setFocus()
    app.exec_()
    if getattr(sys, 'frozen', True):
        sys.stderr.close()
        sys.stderr = sys.__stderr__
