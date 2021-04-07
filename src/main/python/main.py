from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import (QApplication, QDialog, QGridLayout, QGroupBox, QLabel, QLineEdit,
        QPushButton, QRadioButton, QStyleFactory, QFileDialog)
from functools import partial

import time
import sys, os
from play_sound import play
import load_models
import generate

class drumkitchen(QDialog):

    widgetDict = {}

    def __init__(self, parent=None):
        super(drumkitchen, self).__init__(parent)

        self.savedpath = ""
        self.originalPalette = QApplication.palette()

        self.setWindowTitle("drumkitchen")
        self.setFixedWidth(700)
        self.changeStyle('Fusion')
        self.setStyleSheet("background: #333333;" +
                           "color: #ffffff;")

        self.models = load_models.load()

        self.createInputGroupBox()
        self.createGenGroupBox()
        mainLayout = QGridLayout()
        mainLayout.addWidget(self.inputGroupBox)
        mainLayout.addWidget(self.generateGroupBox)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setRowStretch(2, 1)
        self.setLayout(mainLayout)


    def changeStyle(self, styleName):
        QApplication.setStyle(QStyleFactory.create(styleName))
        self.changePalette()

    def changePalette(self):
        QApplication.setPalette(QApplication.style().standardPalette())

    def upload_sound(self, pressed):
        filename = self.openFileNameDialog(self)
        if len(filename) > 0:
            self.widgetDict['uploadPathLineEdit'].setHidden(False)
            self.widgetDict['uploadPathLineEdit'].setText(filename)

    def playInputSound(self, pressed):
        filepath = self.widgetDict['uploadPathLineEdit'].text()
        if len(filepath) > 0 and filepath.endswith('.wav'):
            self.widgetDict['playInputButton'].setDisabled(True)
            play(filepath)
            self.widgetDict['playInputButton'].setDisabled(False)
        

    def record_toggled(self, toggle):
        self.widgetDict['uploadPushButton'].setEnabled(not toggle)

    def openFileNameDialog(self, arg):
        filenamep = ""
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Select a sound to upload", "","Wav Files (*.wav)", options=options)
        if fileName:
            filenamep = fileName
        return filenamep

    def createInputGroupBox(self):
        self.inputGroupBox = QGroupBox("Input sound")

        explLabel = QLabel("Select or record a sound to be transformed onto a drumkit. When selecting a file "
                            + "it should be a wav mono file, and it will be downsampled if needed to 16000 samples per second. "
                            + "Short sounds no longer than 5 seconds are recommended.")
        explLabel.setWordWrap(True)
        explLabel.setStyleSheet("color: #aaaaaa;")
        uploadRadioButton = QRadioButton("Upload a sound")
        uploadRadioButton.setChecked(True)
        uploadPathLineEdit = QLineEdit()
        uploadPathLineEdit.setHidden(True)
        uploadPathLineEdit.setDisabled(True)
        uploadPathLineEdit.setReadOnly(True)
        uploadPushButton = QPushButton("Select...")
        recordRadioButton = QRadioButton("Record a sound")
        playInputButton = QPushButton("Play input sound")

        uploadPushButton.clicked.connect(self.upload_sound)
        recordRadioButton.toggled.connect(self.record_toggled)
        playInputButton.clicked.connect(self.playInputSound)

        layout = QGridLayout()
        layout.addWidget(explLabel, 0, 0, 1, 3)
        layout.addWidget(uploadRadioButton, 1, 0)
        layout.addWidget(uploadPathLineEdit, 1, 1)
        layout.addWidget(uploadPushButton, 1, 2)
        layout.addWidget(recordRadioButton, 2, 0)
        layout.addWidget(playInputButton, 3, 0, 1, 3)
        
        self.widgetDict['uploadRadioButton'] = uploadRadioButton
        self.widgetDict['uploadPathLineEdit'] = uploadPathLineEdit
        self.widgetDict['uploadPushButton'] = uploadPushButton
        self.widgetDict['recordRadioButton'] = recordRadioButton
        self.widgetDict['playInputButton'] = playInputButton

        # layout.addStretch(1)
        self.inputGroupBox.setLayout(layout)

    def generateDrums(self, pressed):
        self.widgetDict['generateButton']
        dirpath = QFileDialog.getExistingDirectory(self, 'Select a folder to save the .wav files')
        self.savedpath = dirpath
        self.widgetDict['savePathLineEdit'].setHidden(False)
        self.widgetDict['savePathLineEdit'].setText(dirpath)
        generate.gendrumkit(self.widgetDict['uploadPathLineEdit'].text(), self.models, dirpath)

        self.widgetDict['generateButton'].setDisabled(False)
        self.widgetDict['savePathLineEdit'].setDisabled(False)
        self.widgetDict['clapPushButton'].setDisabled(False)
        self.widgetDict['closedHatPushButton'].setDisabled(False)
        self.widgetDict['cymbalPushButton'].setDisabled(False)
        self.widgetDict['kickPushButton'].setDisabled(False)
        self.widgetDict['openHatPushButton'].setDisabled(False)
        self.widgetDict['rimshotPushButton'].setDisabled(False)
        self.widgetDict['snarePushButton'].setDisabled(False)
        self.widgetDict['tomPushButton'].setDisabled(False)

    def play_gen(self, file, pressed):
        if len(self.savedpath) > 0:
            filepath = os.path.join(self.savedpath, file)
            play(filepath)

    def createGenGroupBox(self):
        self.generateGroupBox = QGroupBox("Generate drumkit")

        savePathLineEdit = QLineEdit()
        savePathLineEdit.setHidden(True)
        savePathLineEdit.setDisabled(True)
        savePathLineEdit.setReadOnly(True)
        generateButton = QPushButton("Generate")
        generateButton.clicked.connect(self.generateDrums)

        clapLabel = QLabel("Clap")
        closedHatLabel = QLabel("Closed hat")
        cymbalLabel = QLabel("Cymbal")
        kickLabel = QLabel("Kick")
        openHatLabel = QLabel("Open hat")
        rimshotLabel = QLabel("Rimshot")
        snareLabel = QLabel("Snare")
        tomLabel = QLabel("Tom")

        clapPushButton = QPushButton("Play")
        closedHatPushButton = QPushButton("Play")
        cymbalPushButton = QPushButton("Play")
        kickPushButton = QPushButton("Play")
        openHatPushButton = QPushButton("Play")
        rimshotPushButton = QPushButton("Play")
        snarePushButton = QPushButton("Play")
        tomPushButton = QPushButton("Play")

        clapPushButton.setDisabled(True)
        closedHatPushButton.setDisabled(True)
        cymbalPushButton.setDisabled(True)
        kickPushButton.setDisabled(True)
        openHatPushButton.setDisabled(True)
        rimshotPushButton.setDisabled(True)
        snarePushButton.setDisabled(True)
        tomPushButton.setDisabled(True)

        layout = QGridLayout()
        layout.addWidget(generateButton, 0, 0, 1, 2)
        layout.addWidget(savePathLineEdit, 0, 2, 1, 2)

        layout.addWidget(kickLabel, 1, 0)
        layout.addWidget(kickPushButton, 1, 1)
        layout.addWidget(snareLabel, 1, 2)
        layout.addWidget(snarePushButton, 1, 3)

        layout.addWidget(rimshotLabel, 2, 0)
        layout.addWidget(rimshotPushButton, 2, 1)
        layout.addWidget(clapLabel, 2, 2)
        layout.addWidget(clapPushButton, 2, 3)

        layout.addWidget(openHatLabel, 3, 0)
        layout.addWidget(openHatPushButton, 3, 1)
        layout.addWidget(closedHatLabel, 3, 2)
        layout.addWidget(closedHatPushButton, 3, 3)

        layout.addWidget(cymbalLabel, 4, 0)
        layout.addWidget(cymbalPushButton, 4, 1)
        layout.addWidget(tomLabel, 4, 2)
        layout.addWidget(tomPushButton, 4, 3)
        
        self.widgetDict['generateButton'] = generateButton
        self.widgetDict['savePathLineEdit'] = savePathLineEdit
        self.widgetDict['clapPushButton'] = clapPushButton
        self.widgetDict['closedHatPushButton'] = closedHatPushButton
        self.widgetDict['cymbalPushButton'] = cymbalPushButton
        self.widgetDict['kickPushButton'] = kickPushButton
        self.widgetDict['openHatPushButton'] = openHatPushButton
        self.widgetDict['rimshotPushButton'] = rimshotPushButton
        self.widgetDict['snarePushButton'] = snarePushButton
        self.widgetDict['tomPushButton'] = tomPushButton

        kickPushButton.clicked.connect(partial(self.play_gen, 'kick.wav'))
        clapPushButton.clicked.connect(partial(self.play_gen, 'clap.wav'))
        closedHatPushButton.clicked.connect(partial(self.play_gen, 'closedhat.wav'))
        cymbalPushButton.clicked.connect(partial(self.play_gen, 'cymbal.wav'))
        openHatPushButton.clicked.connect(partial(self.play_gen, 'openhat.wav'))
        rimshotPushButton.clicked.connect(partial(self.play_gen, 'rimshot.wav'))
        snarePushButton.clicked.connect(partial(self.play_gen, 'snare.wav'))
        tomPushButton.clicked.connect(partial(self.play_gen, 'tom.wav'))

        # layout.addStretch(1)
        self.generateGroupBox.setLayout(layout)


if __name__ == '__main__':
    appctxt = ApplicationContext()
    window = drumkitchen()
    window.show()
    sys.exit(appctxt.app.exec())
