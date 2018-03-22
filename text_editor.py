import sys,os,time,re
from PyQt4 import QtGui as qt
from PyQt4 import QtCore,Qsci
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.Qsci import *
from PyQt4.QtWebKit import QWebView
from PyQt4.QtCore import QUrl


class sau_edit(qt.QMainWindow):
    def __init__(self):
        super(sau_edit, self).__init__()
        self.screen = qt.QDesktopWidget().screenGeometry()
        self.ht=(self.screen.height())
        self.wd=(self.screen.width())
        self.setGeometry(0,0,self.wd,self.ht)
        self.setMinimumSize(self.wd/2,self.ht/2)
        #self.setGeometry((self.screen.width()-self.wd)/2,0,self.wd,self.ht-50)
        #self.setFixedSize(self.wd,self.ht-50)
        #self.showMaximized()
        #self.showFullScreen()
        #self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowTitle("SAU-editor")
        self.setWindowIcon(qt.QIcon("notepad.png"))

        #---------------------------------status label-------------------------------------
        """self.status=qt.QLabel(self)
        self.status.move(750,500)#self.wd-200,self.ht-200)
        self.status.setStyleSheet("QTextEdit {color:red;background-color:white}")"""
        #---------------------------------all menu bar entry--------------------------------
        new_file_key = qt.QAction("&New file", self)
        new_file_key.setShortcut("Ctrl+n")
        new_file_key.setStatusTip('New file')
        new_file_key.triggered.connect(self.new_file)

        new_window_file_key = qt.QAction("&New window", self)
        new_window_file_key.setShortcut("Ctrl+Shift+n")
        new_window_file_key.setStatusTip('New window')
        new_window_file_key.triggered.connect(self.new_window_file)

        open_file_key = qt.QAction("&Open file", self)
        open_file_key.setShortcut("Ctrl+o")
        open_file_key.setStatusTip('Open file')
        open_file_key.triggered.connect(self.open_file)

        save_key = qt.QAction("&Save", self)
        save_key.setShortcut("Ctrl+s")
        save_key.setStatusTip('Save file')
        save_key.triggered.connect(self.save_file)

        quit_key = qt.QAction("&Quit application !", self)
        quit_key.setShortcut("Ctrl+Q")
        quit_key.setStatusTip('Leave The App')
        quit_key.triggered.connect(self.close_application)

        copy_key = qt.QAction("&Copy", self)
        copy_key.setShortcut("Ctrl+c")
        copy_key.setStatusTip('copy')
        copy_key.triggered.connect(self.save_file)

        cut_key = qt.QAction("&Cut", self)
        cut_key.setShortcut("Ctrl+x")
        cut_key.setStatusTip('cut')
        cut_key.triggered.connect(self.save_file)

        paste_key = qt.QAction("&Paste", self)
        paste_key.setShortcut("Ctrl+v")
        paste_key.setStatusTip('paste')
        paste_key.triggered.connect(self.save_file)

        about_key = qt.QAction("&About", self)
        about_key.setStatusTip('About editor')
        about_key.triggered.connect(self.about_info)

        terminal_key = qt.QAction("&Terminal", self)
        terminal_key.setStatusTip('Open terminal')
        terminal_key.triggered.connect(self.show_terminal)

        refresh_key = qt.QAction("&Refresh", self)
        refresh_key.setStatusTip('Refresh html page')
        refresh_key.triggered.connect(self.refresh_fun)        

        self.statusBar()
        self.terminal()
        #self.terminal1()
        #-------------------------------------all menu-s-------------------------------------
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(new_file_key)
        fileMenu.addAction(new_window_file_key)
        fileMenu.addAction(open_file_key)
        fileMenu.addAction(save_key)
        fileMenu.addAction(quit_key)

        edit_menu=mainMenu.addMenu('&Edit')
        edit_menu.addAction(copy_key)
        edit_menu.addAction(cut_key)
        edit_menu.addAction(paste_key)

        tool_menu=mainMenu.addMenu('&Tool')
        tool_menu.addAction(terminal_key)
        tool_menu.addAction(refresh_key)

        help_menu=mainMenu.addMenu('&Help')
        help_menu.addAction(about_key)
        #-------------------------------------textEdit-----------------------------------------
        self.text_edit_field=QsciScintilla(self)
        self.text_edit_field.setLexer(Qsci.QsciLexerCPP(self))
        self.text_edit_field.setMarginType(10, QsciScintilla.NumberMargin)
        self.text_edit_field.setMarginWidth(0, "0000")
        self.text_edit_field.setStyleSheet("QsciScintilla {background-color:red}")
        self.text_edit_field.setIndentationGuides(True)
        self.text_edit_field.setAutoIndent(True)
        self.text_edit_field.setAutoCompletionThreshold(1)
        self.text_edit_field.setAutoCompletionSource(QsciScintilla.AcsDocument)
        self.text_edit_field.setCallTipsStyle(QsciScintilla.CallTipsNoAutoCompletionContext)
        #self.text_edit_field.setCaretLineVisible(True)
        self.text_edit_field.setFolding(QsciScintilla.BoxedTreeFoldStyle)
        self.text_edit_field.setMarginsBackgroundColor(QColor("#333333"))
        #self.text_edit_field.setCaretLineBackgroundColor(QColor("#A9A9A9"))
        #self.text_edit_field.setFixedSize(self.wd-500,self.ht-80)
        self.text_edit_field.setMaximumWidth(300)
        try:
            self.text_edit_field.setMinimumSize(self.wd/2,self.ht/2)
        except:
            pass
        #self.text_edit_field.showMaximized()
        self.text_edit_field.move(0,30)
        self.font = qt.QFont()
        self.font.setFamily('Courier')
        self.font.setPointSize(10)
        self.text_edit_field.setFont(self.font)
        #self.text_edit_field.setFontItalic(True)
        self.text_edit_field.setStyleSheet("QsciScintilla {color:green;background-color:black}")
        #highlight = syntax.PythonHighlighter(self.text_edit_field.document())
        self.text_edit_field.show()
        self.file_datail()
        """try:
            with open("last_opened.file","r") as lo:
                self.open_file(lo.read())
                print( str(lo.read()))
        except:
            pass"""
        self.load_previous_file()
        self.show()
    #-------------------------------------functions-----------------------------------
    def load_previous_file(self):
        with open("last_opened.file","r") as lof:
            f= lof.read()
            print( lof.read().strip())
        if "." in f:
            with open(f) as data:
                cont=data.read()
                self.text_edit_field.setText(cont)
                self.file_name=f
    def file_datail(self):
        self.file_name_title=qt.QLabel("name:\t",self)
        self.file_name_title.move(710,350)
        self.file_name_title.setFixedSize(250,30)

        self.file_size=qt.QLabel("size:\t",self)
        self.file_size.move(710,370)
        self.file_size.setFixedSize(250,30)
    def new_window_file(self):
        os.system("python text_editor.py")

    def show_terminal(self):
        path=os.getcwd()
        os.system("xterm")

    def terminal(self):
        self.process  = QProcess(self)
        self.terminal = QWidget(self)
        #layout = QVBoxLayout(self)
        #layout.addWidget(self.terminal)
        self.process.start(
            'xterm',
            ['-into', str(self.terminal.winId())]
        )
        self.terminal.move(self.get_window_size()[0]*0.66,30)
        self.terminal.setFixedSize(490,600)

    def terminal1(self):
        self.process  = QProcess(self)
        self.terminal = QWidget(self)
        #layout = QVBoxLayout(self)
        #layout.addWidget(self.terminal)
        self.process.start(
            'xterm',
            ['-into', str(self.terminal.winId())]
        )
        self.terminal.move(700,350)
        self.terminal.setFixedSize(490,600)

    def syn(self):
        data=open(self.file_name,"r").read()
        data=data.replace("int","<font color='red'>int</font>")
        return data

    def resizeEvent(self, event):
        #print(("resize"))
        self.x_y=self.get_window_size()
        print( self.x_y)
        self.set_type()
        if self.x_y[0]<=self.wd/2:
            self.terminal.setHidden(True)
            self.browser.move(self.x_y[0],30)
            self.browser.setFixedSize(self.x_y[0]*0.66,30)
            self.file_name_title.setHidden(True)
            self.file_size.setHidden(True)
            self.text_edit_field.setFixedSize(self.x_y[0],self.x_y[1])
        elif self.x_y[0]>=self.wd/2:
            self.terminal.show()
            self.text_edit_field.setFixedSize(self.x_y[0]*.666,self.x_y[1]-20)
            self.file_name_title.move((self.x_y[0]*0.66)+10,350)
            self.file_size.move((self.x_y[0]*0.66)+10,370)
            self.terminal.move(self.x_y[0]*0.66,30)
            self.terminal.setFixedSize(self.x_y[0]*0.33,600)

    def get_window_size(self):
        data=str(self.size()).split("PyQt4.QtCore.QSize")[1].split(",")
        data1=[]
        data1.append(int(data[0][1:]))
        data1.append(int(data[1][1:-1]))
        return data1

    def about_info(self):
        self.o=about()
        self.o.show()

    def close_application(self):
        try:
            with open("last_opened.file","w") as lo:
                self.write(self.file_name)
                print( "name stored")
        except:
            pass
        choice = qt.QMessageBox.question(self,"Confirm Exit...",
                      "Are you sure you want to exit ?",
                      qt.QMessageBox.Yes| qt.QMessageBox.No)
        if choice == qt.QMessageBox.Yes:
            sys.exit()
        else:
            pass

    def new_file(self):
        print( "new file")
        self.save_file()
        self.file_name=None
        self.text_edit_field.setText("")
        self.browser.setHidden(True)
        self.terminal.setHidden(False)

    def open_file(self):
        self.fileDialog = qt.QFileDialog(self)
        self.file_name=self.fileDialog.getOpenFileName()
        self.setWindowTitle("sau-edit: "+self.file_name)
        try:
            with open(self.file_name) as f:
                self.text_edit_field.setText(f.read())
        except:
            pass
            #print( self.text_edit_field.text())
            #self.text_edit_field.appendHtml(f.read())
        #self.text_edit_field.appendHtml(self.syn())
        self.file_name_title.setText("<font color='red'>name:</font>"+self.file_name.split("/")[-1])
        self.file_size.setText("<font color='red'>size:</font>"+str(os.path.getsize(self.file_name))+" bytes")
        self.set_type()

    """def open_file(self,last_file_name):
        #self.setWindowTitle("sau-edit: "+last_file_name)
        if last_file_name==None:
            print( "none")
        with open(last_file_name) as f:
            self.text_edit_field.setText(f.read())
            #print( self.text_edit_field.text())
            #self.text_edit_field.appendHtml(f.read())
        #self.text_edit_field.appendHtml(self.syn())
        self.file_name_title.setText("<font color='red'>name:</font>"+self.file_name.split("/")[-1])
        self.file_size.setText("<font color='red'>size:</font>"+str(os.path.getsize(self.file_name))+" bytes")"""

    def save_file(self):
        print( "saved")
        self.set_type()
        self.hide_web()
        try:
            with open(self.file_name,"w") as f:
                f.write(self.text_edit_field.text())
            print( "successful")
            self.file_name_title.setText("<font color='red'>name:</font>"+self.file_name.split("/")[-1])
            self.file_size.setText("<font color='red'>size:</font>"+str(os.path.getsize(self.file_name))+" bytes")
            self.setWindowTitle("Sau's Editor:  "+str(self.file_name))
        except:
            try:
                name = qt.QFileDialog.getSaveFileName(self, 'Save File')
                file = open(name,'w')
                text = self.text_edit_field.text()
                file.write(text)
                file.close()
                self.file_name=name
                self.file_name_title.setText("<font color='red'>name:</font>"+self.file_name.split("/")[-1])
                self.file_size.setText("<font color='red'>size:</font>"+str(os.path.getsize(self.file_name))+" bytes")
            except:
                pass
        #self.status.setText("saved")

    def closeEvent(self,event):
        print( event)
        result = qt.QMessageBox.question(self,
                      "Confirm Exit...",
                      "Are you sure you want to exit ?",
                      qt.QMessageBox.Yes| qt.QMessageBox.No)
        event.ignore()

        if result == qt.QMessageBox.Yes:
            try:
                with open("last_opened.file","w") as lo:
                    lo.write(self.file_name)
                print( "name stored")
            except:
                pass
            print( "close event")
            event.accept()
            #sys.exit()
    def refresh_fun(self):
        try:
            self.browser.load(QUrl(self.file_name))
        except:
            pass
    def set_type(self):
        try:
            ext=self.file_name.split(".")[-1]
            print( ext)
        except:
            ext=""
            self.text_edit_field.setLexer(Qsci.QsciLexerCPP(self))
            pass
        if ext=="py":
            self.text_edit_field.setLexer(Qsci.QsciLexerPython(self))
            self.hide_web()
            print( "type python")
        elif ext=="cpp" or ext=="c":
            self.text_edit_field.setLexer(Qsci.QsciLexerCPP(self))
            self.hide_web()
            print( "type cpp")
        elif ext=="html":
            self.text_edit_field.setLexer(Qsci.QsciLexerHTML(self))
            self.terminal.setHidden(True)
            self.browser = QWebView(self)
            self.browser.load(QUrl(self.file_name))
            self.browser.move(self.x_y[0]*66,30)
            self.browser.setFixedSize(self.x_y[0]*0.33,self.x_y[1]-20)
            self.browser.show()
            #self.browser.move(500,0)
            #self.setGeometry((self.screen.width()-self.wd+200)/2,0,self.wd,self.ht-50)
            #self.setFixedSize(self.wd+200,self.ht-50)
            print( "type html")
    def hide_web(self):
        #try:
        print( "hide html")
        self.terminal.setHidden(False)
        try:
            self.browser.close()
            self.browser.setHidden(True)
        except:
            pass
#        except:
#           pass
def run():
    app = qt.QApplication(sys.argv)
    GUI = sau_edit()
    sys.exit(app.exec_())
run()
