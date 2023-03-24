from systemVariables import systemVariables
from queryProcessor import dynamicIndex, termPartitionedIndex

from os import listdir
from os.path import basename, dirname, realpath
from re import match
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
        
        self.noQueryIcon = QPushButton()
        self.queryStackedWidget = QStackedWidget()
    
    
    
    
    
    
    def getFileName(self, directory):
        return basename(directory)
    
    
    
    
    
    
    def eventFilter(self, object, event):
        
        if object == self.noQueryIcon and event.type() == QEvent.Type.HoverEnter:
            self.noQueryIcon.setIcon(QIcon(self.currentDirectory + '\\Images\\Search icon hover'))
            self.noQueryIcon.setIconSize(QSize(100, 100))
        elif object == self.noQueryIcon and event.type() == QEvent.Type.HoverLeave:
            self.noQueryIcon.setIcon(QIcon(self.currentDirectory + '\\Images\\Search icon'))
            self.noQueryIcon.setIconSize(QSize(100, 100))
        
        return super().eventFilter(object, event)
    
    
    
    
    
    
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
            return
        elif not self.filesPresent:
            self.showErrorMessage('Please select the files you would like to search from')
            return
        
        try:
            self.mainStackedWidget.removeWidget(self.queryStackedWidget)
        except:
            pass

        self.documentContent = []
        for index, documentLocation in enumerate(self.listOfFiles):
            with open(documentLocation, 'r', encoding = 'utf--8', errors = 'ignore') as document:
                documentBundle = []
                documentBundle.append(index)
                documentContent = document.read()
                documentBundle.append(documentContent)
                self.documentContent.append(documentBundle)
        
        if self.tPIndex.isChecked():
            index = termPartitionedIndex(len(self.documentContent))
            for document in self.documentContent:
                termPartitionedIndex.addDocument(index, document)
        
        else:
            index = dynamicIndex()
            for document in self.documentContent:
                dynamicIndex.addDocument(index, document)
        
        for query in self.queryList:
            results = index.search(query)
            queryWidget = QWidget(self.mainStackedWidget)
            queryWidget.setObjectName('mainCOntainerWidget')
            queryWidget.setFixedSize(self.mainStackedWidget.width(), self.mainStackedWidget.height())
            currentQuery = QLabel(queryWidget)
            currentQuery.setObjectName('subContainerLabel')
            currentQuery.setFixedWidth(queryWidget.width() - 50)
            currentQuery.setText(f"Showing results for \"{query}\"")
            currentQuery.setWordWrap(True)
            currentQuery.move(25, 20)
            self.queryStackedWidget = QStackedWidget(self.mainStackedWidget)
            self.queryStackedWidget.setObjectName('mainContainerWidget')
            self.queryStackedWidget.setFixedSize(self.mainStackedWidget.width(), self.mainStackedWidget.height())
            if results:
                resultScrollableArea = QScrollArea(queryWidget)
                resultScrollableArea.setObjectName('scrollableWidget')
                resultScrollableArea.setFixedHeight(queryWidget.height() - (20 + 20 + 20))
                resultScrollableArea.setFixedWidth(queryWidget.width() - 40)
                resultScrollableArea.move(20, currentQuery.height() + 20 + 20)
                resultScrollableWidget = QWidget(queryWidget)
                resultScrollableWidget.setObjectName('scrollableWidget')
                resultScrollableWidget.setFixedHeight(resultScrollableArea.height())
                resultLayout = QVBoxLayout()
                resultLayout.setContentsMargins(5, 0, 5, 10)
                
                for result in results:
                    resultWidget = QWidget(resultScrollableArea)
                    resultWidget.setObjectName('resultWidget')
                    resultWidget.setFixedSize(30, resultScrollableWidget.width() - 10)
                    resultRelevanceScore = QLabel(resultWidget)
                    resultRelevanceScore.setObjectName('relevanceScore')
                    resultRelevanceScore.setStyleSheet('padding-left: none;')
                    resultRelevanceScore.setFixedSize(30, 20)
                    resultRelevanceScore.setText(str(result[1]))
                    resultRelevanceScore.setToolTip(f"Relevance score: {result[1]}")
                    resultRelevanceScore.move(5, 5)
                    resultRelevanceScore.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    resultFileName = self.getFileName(self.listOfFiles[result[0][0]])
                    resultFileLabel = QLabel(resultWidget)
                    resultFileLabel.setObjectName('alternateContainerWidget')
                    resultFileLabel.setText(resultFileName)
                    resultFileLabel.move(5 + 10 + resultRelevanceScore.width(), 5)
                    resultFileLabel.setToolTip(resultFileName)
                    resultLayout.addWidget(resultWidget)
                resultScrollableWidget.setLayout(resultLayout)
                resultScrollableArea.setWidget(resultScrollableWidget)
                resultScrollableArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
                resultScrollableArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            else:
                ...
            self.queryStackedWidget.addWidget(queryWidget)
        self.queryStackedWidget.setCurrentIndex(0)
        self.mainStackedWidget.addWidget(self.queryStackedWidget)
        self.mainStackedWidget.setCurrentWidget(self.queryStackedWidget)
    
    
    
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
        errorLabelWidth = self.errorLabel.width()
        self.errorLabel.move((((systemVariables.appDimension[0] - 240) - errorLabelWidth) // 2) + 240, 20)
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
                self.noQueryIcon.clicked.disconnect()
            except:
                pass
            self.adaptiveQueryButton.clicked.connect(self.clickSearchButton)
            self.noQueryIcon.clicked.connect(self.clickSearchButton)
        else:
            self.adaptiveQueryButton.setText('ADD TO QUERY')
            self.adaptiveQueryButton.setFixedWidth(100)
            self.adaptiveQueryButton.move(self.queryWidgetSize[0] - (self.adaptiveQueryButton.width() + 5), 5)
            self.queryField.setFixedSize(self.queryWidgetSize[0] - self.adaptiveQueryButton.width() - 20, 30)
            try:
                self.adaptiveQueryButton.clicked.disconnect()
                self.noQueryIcon.clicked.disconnect()
            except:
                pass
            self.adaptiveQueryButton.clicked.connect(self.clickAddToQueryButton)
            self.noQueryIcon.clicked.connect(self.clickAddToQueryButton)
    
    
    
    def queryIndexChangeEvent(self):
        
        if not match('^[0-9]+$', self.currentQuery.text()):
            self.currentQuery.setText('⫗')
    
    
    
    
    
    
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
        # self.errorLabel.setFixedHeight(20)
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
        
        self.mainStackedWidget = QStackedWidget(self)
        self.mainStackedWidget.setObjectName('scrollableWidget')
        # self.mainStackedWidget.setStyleSheet('background-color: #999999;')
        self.mainStackedWidget.setFixedWidth((systemVariables.appDimension[0] - (200 + 40 + 100)))
        self.mainStackedWidget.setFixedHeight((systemVariables.appDimension[1]) - (20 + 80 + 80 + 40))
        self.mainStackedWidget.move((((systemVariables.appDimension[0] - (200 + 40)) - (systemVariables.appDimension[0] - (200 + 40 + 100))) // 2) + 200 + 40, 80 + 50)
        self.noQueryWidget = QWidget(self.mainStackedWidget)
        self.noQueryWidget.setObjectName('mainContainerWidget')
        self.noQueryWidget.setFixedSize(self.mainStackedWidget.width(), self.mainStackedWidget.height())
        # self.noQueryWidget.setStyleSheet('background-color: rgba(255, 255, 255, 0.5);')
        opacity = QGraphicsOpacityEffect()
        opacity.setOpacity(0.5)
        # self.noQueryWidget.setGraphicsEffect(opacity)
        # self.noQueryEmptyLabel = QLabel(self.noQueryWidget)
        # self.noQueryEmptyLabel.setObjectName('subContainerLabel')
        # self.noQueryEmptyLabel.setStyleSheet('background-color: rgba(0, 0, 0, 0); color: #333333;')
        # self.noQueryEmptyLabel.setText('Wow, such empty!')
        # # self.noQueryEmptyLabel.move((self.mainStackedWidget.width() - self.noQueryEmptyLabel.width()) // 2, (self.noQueryWidget.height() - self.noQueryEmptyLabel.height()) // 2 - 15)
        # self.noQueryEmptyLabel.move((self.mainStackedWidget.width() - self.noQueryEmptyLabel.width()) // 2, (self.noQueryWidget.height() - self.noQueryEmptyLabel.height()) // 2 - 15)
        # self.noQuerySearchLabel = QLabel(self.noQueryWidget)
        # self.noQuerySearchLabel.setObjectName('defaultButton')
        # self.noQueryEmptyLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.noQuerySearchLabel.setText('Surf a query to get started!')
        # self.noQuerySearchLabel.move((self.mainStackedWidget.width() - self.noQuerySearchLabel.width()) // 2 - 5, (self.noQueryWidget.height() - self.noQuerySearchLabel.height()) // 2 + 20)
        self.noQueryIcon = QPushButton(self.noQueryWidget)
        self.noQueryIcon.setFixedSize(100, 100)
        self.noQueryIcon.setObjectName('scrollableWidget')
        self.noQueryIcon.setIcon(QIcon(self.currentDirectory + '\\Images\\Search icon.png'))
        self.noQueryIcon.setIconSize(QSize(100, 100))
        self.noQueryIcon.move((self.mainStackedWidget.width() - 100) // 2, ((self.mainStackedWidget.height() - 100) // 2) - 30)
        self.noQueryIcon.clicked.connect(self.clickSearchButton)
        self.noQueryIcon.installEventFilter(self)
        self.mainStackedWidget.addWidget(self.noQueryWidget)
        self.mainStackedWidget.setCurrentWidget(self.noQueryWidget)
        
        self.previousQueryButton = QPushButton(self)
        self.previousQueryButton.setObjectName('defaultButton')
        self.previousQueryButton.setFixedSize(30, 20)
        self.previousQueryButton.setText('◀')
        self.previousQueryButton.move((((systemVariables.appDimension[0] - (200 + 40)) - (systemVariables.appDimension[0] - (200 + 40 + 100))) // 2) + 200 + 40, self.mainStackedWidget.height() + 80 + 60)
        self.previousQueryButton.setDisabled(True)
        self.nextQueryButton = QPushButton(self)
        self.nextQueryButton.setObjectName('defaultButton')
        self.nextQueryButton.setFixedSize(30, 20)
        self.nextQueryButton.setText('▶')
        self.nextQueryButton.move((systemVariables.appDimension[0] - (80)), self.mainStackedWidget.height() + 80 + 60)
        self.nextQueryButton.setDisabled(True)
        self.currentQuery = QLineEdit(self)
        self.currentQuery.setObjectName('alternateContainerWidget')
        self.currentQuery.setPlaceholderText('⫗')
        self.currentQuery.setToolTip('Search for a few queries to view the index')
        self.currentQuery.setFixedSize(50, 20)
        self.currentQuery.move((((systemVariables.appDimension[0] - 240) - self.currentQuery.width()) // 2) + 240, self.mainStackedWidget.height() + 80 + 60)
        self.currentQuery.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.currentQuery.setDisabled(True)
        
    
    
    
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
                currentQuery.setToolTip(query)
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
