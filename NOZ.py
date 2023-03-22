from systemVariables import systemVariables

from os import listdir
from os.path import dirname, realpath
from sys import exit, argv
from time import sleep
from tkinter import Tk, filedialog

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *





class mainApplication(QMainWindow):
    
    def __init__(self):
        
        super().__init__()
        
        self.createCommonVariables()
        
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        
        self.setFixedSize(systemVariables.appDimension[0], systemVariables.appDimension[1])
        
        self.styleSheet = systemVariables.stylesheet
        self.setStyleSheet(self.styleSheet)
        
        backgroundImage = QLabel(self)
        # backgroundImage.setObjectName('backgroundImage')
        backgroundImagePixmap = QPixmap(f'{self.currentDirectory}\\Images\\Wallpaper.png')
        backgroundImage.setPixmap(backgroundImagePixmap)
        backgroundImage.resize(backgroundImagePixmap.width(), backgroundImagePixmap.height())
        backgroundImage.move(0, 0)
        
        self.createMainWidgets()
    
    
    
    
    
    
    def createCommonVariables(self):
        
        self.currentDirectory = dirname(realpath(__file__))
        
        self.listOfFiles = []
        self.queryList = []
        self.filesPresent = False
        
        self.holdTimer = QTimer()
        self.holdTimer.setInterval(2500)
    
    
    
    
    
    
    def clickSelectFromDirectoryButton(self):
        
        directory = filedialog.askdirectory()
        if directory:
            directory = listdir(directory)
        for file in directory:
            if file.endswith('.txt'):
                self.listOfFiles.append(file)
            print(file)
        if len(self.listOfFiles) == 0:
            self.showErrorMessage("No files were found in the given directory")
            self.filesPresent = False
            self.fromDirectory.setChecked(False)
        else:
            self.filesPresent = True
            self.fromDirectory.setChecked(True)
            self.fromFiles.setChecked(False)
    
    
    
    def clickSelectFromFilesButton(self):
        
        directory = filedialog.askopenfilenames()
        for file in directory:
            if file.endswith('.txt'):
                self.listOfFiles.append(file)
            print(file)
        if len(self.listOfFiles) == 0:
            self.showErrorMessage("None of the files had the supportd file type")
            self.filesPresent = False
            self.fromFiles.setChecked(False)
        else:
            self.filesPresent = True
            self.fromFiles.setChecked(True)
            self.fromDirectory.setChecked(False)
    
    
    
    def clickSearchButton(self):
        
        if len(self.queryList) == 0:
            self.showErrorMessage('Please enter a query to search for')
        elif not self.filesPresent:
            self.showErrorMessage('Please select the files you would like to search from')
    
    
    
    def clickAddToQueryButton(self):
        
        self.queryList.append(self.queryField.text())
        self.queryField.setText('')
        self.createQueryList()
        self.queryField.setFocus()
        
        
    
    def clickSelectDynamicIndexButton(self):
        self.dynamicIndex.setChecked(True)
        self.tPIndex.setChecked(False)
    
    
    
    def clickSelectTPIndexButton(self):
        self.tPIndex.setChecked(True)
        self.dynamicIndex.setChecked(False)
    
    
    
    def clickDeleteQueryButton(self, index):
        self.queryList.pop(index)
        self.createQueryList()

    
    
    
    
    
    def showErrorMessage(self, message, color = '#FF4010'):    
        
        self.errorLabel.setText(message)
        self.errorLabel.setStyleSheet(f'background-color: {color};')
        self.errorLabel.setVisible(True)
        self.holdTimer.timeout.connect(lambda: self.errorLabel.setHidden(True))
        self.holdTimer.timeout.connect(self.holdTimer.stop)
        self.holdTimer.start()
    
    
    
    
    
    
    def queryFieldChangeEvent(self):
        
        if self.queryField.text() == '':
            self.adaptiveQueryButton.setText('SEARCH')
            self.adaptiveQueryButton.setFixedWidth(70)
            self.adaptiveQueryButton.move(self.queryWidgetSize[0] - (self.adaptiveQueryButton.width() + 5), 5)
            self.queryField.setFixedSize(self.queryWidgetSize[0] - self.adaptiveQueryButton.width() - 20, 30)
            try:
                self.adaptiveQueryButton.clicked.disconnect()
            except:
                pass
            self.adaptiveQueryButton.clicked.connect(self.clickSearchButton)
        else:
            self.adaptiveQueryButton.setText('ADD TO QUERY')
            self.adaptiveQueryButton.setFixedWidth(100)
            self.adaptiveQueryButton.move(self.queryWidgetSize[0] - (self.adaptiveQueryButton.width() + 5), 5)
            self.queryField.setFixedSize(self.queryWidgetSize[0] - self.adaptiveQueryButton.width() - 20, 30)
            try:
                self.adaptiveQueryButton.clicked.disconnect()
            except:
                pass
            self.adaptiveQueryButton.clicked.connect(self.clickAddToQueryButton)
    
    
    
    
    
    
    def createMainWidgets(self):
        
        self.menuBar = QWidget(self)
        self.menuBar.setObjectName('mainContainerWidget')
        self.menuBar.setFixedSize(200, systemVariables.appDimension[1] - 40)
        self.menuBar.move(20, 20)
        menuBarLogo = QLabel(self.menuBar)
        menuBarLogoPixmap = QPixmap(f'{self.currentDirectory}\\Images\\Logo.png').scaledToWidth(150)
        menuBarLogo.setPixmap(menuBarLogoPixmap)
        menuBarLogo.resize(menuBarLogoPixmap.width(), menuBarLogoPixmap.height())
        menuBarLogo.move(200 // 2 - (menuBarLogoPixmap.width() // 2), 30)
        
        menuBarSearchFromWidget = QWidget(self.menuBar)
        menuBarSearchFromWidget.setObjectName('subContainerWidget')
        menuBarSearchFromWidget.setFixedSize(180, 65)
        menuBarSearchFromWidget.move(10, 130)
        menuBarSearchFromLabel = QLabel(menuBarSearchFromWidget)
        menuBarSearchFromLabel.setObjectName('subContainerLabel')
        menuBarSearchFromLabel.setText("Search from")
        menuBarSearchFromLabel.move(10, 5)
        self.fromDirectory = QPushButton(menuBarSearchFromWidget)
        self.fromDirectory.setObjectName('defaultButton')
        self.fromDirectory.setFixedHeight(20)
        self.fromDirectory.move(10, 35)
        self.fromDirectory.setText('DIRECTORY')
        self.fromDirectory.setCheckable(True)
        self.fromDirectory.clicked.connect(self.clickSelectFromDirectoryButton)
        self.fromFiles = QPushButton(menuBarSearchFromWidget)
        self.fromFiles.setObjectName('defaultButton')
        self.fromFiles.setFixedHeight(20)
        self.fromFiles.setMaximumWidth(180)
        self.fromFiles.move(89, 35)
        self.fromFiles.setText('FILES')
        self.fromFiles.setCheckable(True)
        self.fromFiles.clicked.connect(self.clickSelectFromFilesButton)
        
        menuBarIndexingWidget = QWidget(self.menuBar)
        menuBarIndexingWidget.setObjectName('subContainerWidget')
        menuBarIndexingWidget.setFixedSize(180, 65)
        menuBarIndexingWidget.move(10, 205)
        menuBarIndexingLabel = QLabel(menuBarIndexingWidget)
        menuBarIndexingLabel.setObjectName('subContainerLabel')
        menuBarIndexingLabel.setText("Indexing type")
        menuBarIndexingLabel.move(10, 5)
        self.dynamicIndex = QPushButton(menuBarIndexingWidget)
        self.dynamicIndex.setObjectName('defaultButton')
        self.dynamicIndex.setFixedHeight(20)
        self.dynamicIndex.move(10, 35)
        self.dynamicIndex.setText('DYNAMIC')
        self.dynamicIndex.setCheckable(True)
        self.dynamicIndex.setChecked(True)
        self.dynamicIndex.clicked.connect(self.clickSelectDynamicIndexButton)
        self.tPIndex = QPushButton(menuBarIndexingWidget)
        self.tPIndex.setObjectName('defaultButton')
        self.tPIndex.setFixedHeight(20)
        self.tPIndex.setMaximumWidth(180)
        self.tPIndex.move(80, 35)
        self.tPIndex.setText('T-PARTITIONED')
        self.tPIndex.setCheckable(True)
        self.tPIndex.clicked.connect(self.clickSelectTPIndexButton)
        
        self.menuBarQueryListWidget = QWidget(self.menuBar)
        self.menuBarQueryListWidget.setObjectName('subContainerWidget')
        self.menuBarQueryListWidget.setFixedWidth(180)
        self.menuBarQueryListWidget.setMaximumHeight(170)
        self.menuBarQueryListWidget.move(10, 275)
        menuBarQueryListLabel = QLabel(self.menuBarQueryListWidget)
        menuBarQueryListLabel.setObjectName('subContainerLabel')
        menuBarQueryListLabel.setText("Your queries")
        menuBarQueryListLabel.move(10, 5)
        self.menuBarQueryListScrollableArea = QScrollArea(self.menuBarQueryListWidget)
        self.menuBarQueryListScrollableArea.setObjectName('scrollableWidget')
        self.menuBarQueryListScrollableArea.setFixedWidth(180)
        self.menuBarQueryListScrollableArea.setMaximumHeight(180)
        self.menuBarQueryListScrollableArea.move(0, 35)
        self.createQueryList()
        
        self.errorLabel = QLabel(self)
        self.errorLabel.setObjectName('errorMessage')
        self.errorLabel.setFixedSize(300, 20)
        self.errorLabel.move((((systemVariables.appDimension[0] - (200 + 40)) - 300) // 2) + 200 + 40, 10)
        self.errorLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.errorLabel.setHidden(True)
        
        self.queryWidgetSize = [(systemVariables.appDimension[0] - (200 + 40 + 100)), 30]
        queryWidget = QWidget(self)
        queryWidget.setObjectName('mainContainerWidget')
        queryWidget.setFixedSize((systemVariables.appDimension[0] - (200 + 40 + 100)), 30)
        queryWidget.move((((systemVariables.appDimension[0] - (200 + 40)) - (systemVariables.appDimension[0] - (200 + 40 + 100))) // 2) + 200 + 40, 50)
        self.adaptiveQueryButton = QPushButton(queryWidget)
        self.adaptiveQueryButton.setObjectName('defaultAlterButton')
        self.adaptiveQueryButton.setFixedHeight(20)
        self.adaptiveQueryButton.setText('SEARCH')
        self.adaptiveQueryButton.setFixedWidth(70)
        self.adaptiveQueryButton.move(self.queryWidgetSize[0] - (self.adaptiveQueryButton.width() + 5), 5)
        self.adaptiveQueryButton.clicked.connect(self.clickSearchButton)
        self.queryField = QLineEdit(queryWidget)
        self.queryField.setObjectName('mainContainerWidget')
        self.queryField.setFixedSize(self.queryWidgetSize[0] - self.adaptiveQueryButton.width() - 20, 30)
        self.queryField.move(5, 0)
        self.queryField.setPlaceholderText('Type your query here...')
        self.queryField.textChanged.connect(self.queryFieldChangeEvent)
        self.queryField.setFocus()
    
    
    
    def createQueryList(self):
        
        self.menuBarQueryListScrollableWidget = QWidget(self.menuBarQueryListWidget)
        self.menuBarQueryListScrollableWidget.setObjectName('scrollableWidget')
        self.menuBarQueryListScrollableArea.setFixedHeight(140)
        self.menuBarQueryListLayout = QVBoxLayout()
        self.menuBarQueryListLayout.setContentsMargins(10, 0, 10, 5)
        
        if len(self.queryList) > 0:
            for index, query in enumerate(self.queryList):
                currentQueryContainer = QWidget(self.menuBarQueryListScrollableArea)
                currentQueryContainer.setFixedSize(160, 20)
                currentQuery = QLabel(currentQueryContainer)
                currentQuery.setObjectName('queryContainer')
                currentQuery.setFixedHeight(20)
                currentQuery.setMaximumWidth(160)
                currentQuery.setText(query)
                currentQueryButton = QPushButton(currentQuery)
                currentQueryButton.setObjectName('defaultButton')
                currentQueryButton.setStyleSheet('padding-left: None; padding-right: None; padding: Npne; font-size: 6px; font-weight: 500; border-radius: 5px;')
                currentQueryButton.setFixedSize(10, 10)
                currentQueryButton.move(5, 5)
                currentQueryButton.setText('✕')
                currentQueryButton.clicked.connect(lambda checked, argument = index: self.clickDeleteQueryButton(argument))
                self.menuBarQueryListLayout.addWidget(currentQueryContainer)
            
        else:
            currentQuery = QLabel(self.menuBarQueryListScrollableArea)
            currentQuery.setObjectName('defaultButton')
            currentQuery.setFixedHeight(20)
            currentQuery.setMaximumWidth(180)
            currentQuery.setText('Add a query to begin...')
            self.menuBarQueryListLayout.addWidget(currentQuery)
            
        self.menuBarQueryListScrollableWidget.setLayout(self.menuBarQueryListLayout)
        self.menuBarQueryListScrollableArea.setWidget(self.menuBarQueryListScrollableWidget)
        self.menuBarQueryListScrollableArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.menuBarQueryListScrollableArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        




def startUp():
    
    application = QApplication(argv)
    applicationInitializer = mainApplication()
    applicationInitializer.show()
    exit(application.exec())
        
        
        


if __name__ == '__main__':
    
    try:
        startUp()
    
    except Exception as errorCode:
        print(f"An error has occured!\n{errorCode}")
        sleep(5)
        exit()
