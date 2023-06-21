from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtPrintSupport import *
import sys,sqlite3,time

import os

class InsertDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(InsertDialog, self).__init__(*args, **kwargs)

        self.setWindowTitle("Add Item")
        self.setFixedWidth(300)
        self.setFixedHeight(250)

        self.QBtn = QPushButton()
        self.QBtn.setText("Add")

        self.QBtn.clicked.connect(self.insertItem)

        layout = QVBoxLayout()

        self.typeinput = QComboBox()
        self.typeinput.addItem("Income")
        self.typeinput.addItem("Expend")
        layout.addWidget(self.typeinput)

        self.amountinput = QLineEdit()
        self.amountinput.setInputMask('999999.9') #规定按此格式输入，9代表允许数字[0,9]
        layout.addWidget(self.amountinput)

        self.categoryinput = QComboBox()
        self.categoryinput.addItem("吃饭")
        self.categoryinput.addItem("购物")
        self.categoryinput.addItem("学费")
        self.categoryinput.addItem("生活费")
        self.categoryinput.addItem("工资")
        self.categoryinput.addItem("奖学金")
        self.categoryinput.addItem("其他")
        layout.addWidget(self.categoryinput)

        self.commentinput = QLineEdit()
        self.commentinput.setPlaceholderText("Comment")
        layout.addWidget(self.commentinput)

        date = QDate.currentDate()
        self.dateinput = QLineEdit()
        self.dateinput.setText(date.toString(Qt.ISODate)) #以本地时间显示
        layout.addWidget(self.dateinput)
        
        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def insertItem(self):
        type = ""
        amount = -1
        category = ""
        comment = ""
        date = ""

        type = self.typeinput.itemText(self.typeinput.currentIndex())
        amount = self.amountinput.text()
        category = self.categoryinput.itemText(self.categoryinput.currentIndex())
        comment = self.commentinput.text()
        date = self.dateinput.text()
        try:
            self.conn = sqlite3.connect("database.db")
            self.c = self.conn.cursor()
            self.c.execute("INSERT INTO account(type,amount,category,comment,date) VALUES (?,?,?,?,?)",(type,amount,category,comment,date))
            self.conn.commit()
            self.c.close()
            self.conn.close()
            QMessageBox.information(QMessageBox(),'Successful','Item is added successfully to the database.')
            self.close()
        except Exception:
            QMessageBox.warning(QMessageBox(), 'Error', 'Fail to add item to the database.')

class SearchDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(SearchDialog, self).__init__(*args, **kwargs)

        self.setWindowTitle("Search Item")
        self.setFixedWidth(300)
        self.setFixedHeight(300)
        
        layout = QVBoxLayout()
        
        title = QLabel("Search condition:")
        layout.addWidget(title)
        
        type = QLabel("Income/Expend Type:")
        layout.addWidget(type)
        
        self.searchbytype = QComboBox()
        self.searchbytype.setPlaceholderText("Type")
        self.searchbytype.addItem("Income")
        self.searchbytype.addItem("Expend")
        layout.addWidget(self.searchbytype)
        
        datebegin = QLabel("Begin Date:")
        layout.addWidget(datebegin)
        
        self.searchbydatebegin = QLineEdit()
        self.searchbydatebegin.setPlaceholderText("year-month-date")
        self.searchbydatebegin.setInputMask('9999-99-99')
        layout.addWidget(self.searchbydatebegin)
        
        dateend = QLabel("End Date:")
        layout.addWidget(dateend)
        
        self.searchbydateend = QLineEdit()
        self.searchbydateend.setPlaceholderText("year-month-date")
        self.searchbydateend.setInputMask('9999-99-99')
        layout.addWidget(self.searchbydateend)

        self.QBtn = QPushButton()
        self.QBtn.setText("Search")
        self.QBtn.clicked.connect(self.searchItem)
        layout.addWidget(self.QBtn)
        
        self.setLayout(layout)

    def searchItem(self):

        type = ""
        datebegin = ""
        dateend = ""
        
        type = self.searchbytype.itemText(self.searchbytype.currentIndex())
        datebegin = self.searchbydatebegin.text()
        dateend = self.searchbydateend.text()
        
        print(type)
        print(datebegin)
        print(dateend)
        
        try:
            self.conn = sqlite3.connect("database.db")
            self.c = self.conn.cursor()
            #result = self.c.execute("SELECT * from account WHERE type=%s AND date >= %s AND date <= %s", (type, datebegin, dateend))
            #result = self.c.execute("SELECT * from account WHERE type="+type+" AND date >= "+datebegin+" AND date <= "+dateend)
            #result = self.c.execute("SELECT * from account WHERE date >= '2020-01-01' AND date <= '2025-01-01'")
            self.c.execute("SELECT * from account WHERE type = ? AND date >= ? AND date <= ?", ([(type), (datebegin), (dateend)]))
            #print(self.c.fetchall()) #debug
            
            result = self.c.fetchall()
            if(result):
                QMessageBox.information(QMessageBox(), 'Successful', str(result))
            else:
                QMessageBox.information(QMessageBox(), 'Fail', 'No result fetched')
            
            # row = result.fetchone()
            # if(row):
            #     serachresult = "Roll No. : "+str(row[0])+'\n'+"Type : "+str(row[1])+'\n'+"Amount : "+str(row[2])+'\n'+"Category : "+str(row[3])+'\n'+"Comment : "+str(row[4])+'\n'+"DateTime : "+str(row[5])
            #     QMessageBox.information(QMessageBox(), 'Successful', serachresult)
            # else:
            #     QMessageBox.information(QMessageBox(), 'Fail', 'No result fetched')
            self.conn.commit()
            self.c.close()
            self.conn.close()
        except Exception:
            QMessageBox.warning(QMessageBox(), 'Error', 'Fail to find item from the database.')

class DeleteDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(DeleteDialog, self).__init__(*args, **kwargs)

        self.QBtn = QPushButton()
        self.QBtn.setText("Delete")

        self.setWindowTitle("Delete Item")
        self.setFixedWidth(300)
        self.setFixedHeight(100)
        self.QBtn.clicked.connect(self.deleteItem)
        layout = QVBoxLayout()

        self.deleteinput = QLineEdit()
        self.onlyInt = QIntValidator()
        self.deleteinput.setValidator(self.onlyInt)
        self.deleteinput.setPlaceholderText("Roll No.")
        layout.addWidget(self.deleteinput)
        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def deleteItem(self):

        delrol = ""
        delrol = self.deleteinput.text()
        try:
            self.conn = sqlite3.connect("database.db")
            self.c = self.conn.cursor()
            self.c.execute("DELETE from account WHERE roll="+str(delrol))
            self.conn.commit()
            self.c.close()
            self.conn.close()
            QMessageBox.information(QMessageBox(),'Successful','Deleted item from table Successful')
            self.close()
        except Exception:
            QMessageBox.warning(QMessageBox(), 'Error', 'Fail to delete item from the database.')

class LoginDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(LoginDialog, self).__init__(*args, **kwargs)

        self.setFixedWidth(300)
        self.setFixedHeight(200)

        layout = QVBoxLayout()

        self.usernameinput = QLineEdit()
        self.usernameinput.setEchoMode(QLineEdit.Normal)
        self.usernameinput.setPlaceholderText("Enter Username.")
        
        self.passwordinput = QLineEdit()
        self.passwordinput.setEchoMode(QLineEdit.Password) #按密码形式显示，隐藏密码
        self.passwordinput.setPlaceholderText("Enter Password.")
        
        self.QBtnLogin = QPushButton()
        self.QBtnLogin.setText("Login")
        self.QBtnLogin.clicked.connect(self.login) #设置Push button的响应函数
        
        self.QBtnRegister = QPushButton()
        self.QBtnRegister.setText("Register")
        self.QBtnRegister.clicked.connect(self.register)

        #设置窗口标题
        self.setWindowTitle('简易记账工具V0.1')
        title = QLabel("Please login or register:")
        title.setFont(QFont('Times', 16))

        #窗口布局
        layout.addWidget(title)
        layout.addWidget(self.usernameinput)
        layout.addWidget(self.passwordinput)
        layout.addWidget(self.QBtnLogin)
        layout.addWidget(self.QBtnRegister)
        self.setLayout(layout)

        self.conn = sqlite3.connect("user.db")
        self.c = self.conn.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS usertable(roll INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)")
        self.c.close()
        

    def login(self):
        self.conn = sqlite3.connect("user.db")
        self.c = self.conn.cursor()
        username = self.usernameinput.text()
        password = self.passwordinput.text()
        self.c.execute("SELECT * FROM usertable WHERE username = ? AND password = ?", ([(username), (password)]))
        result = self.c.fetchall() #获取该查询(SELECT * FROM)的结果，如果非空表示有预期的结果
        if(result):
            self.accept() #设置状态 QDialog.Accepted
        else:
            QMessageBox.warning(self, 'Error', 'Wrong UserName or Password')

    def register(self):
        username = self.usernameinput.text()
        password = self.passwordinput.text()
        try:
            self.conn = sqlite3.connect("user.db")
            self.c = self.conn.cursor()
        
            self.c.execute("INSERT INTO usertable(username,password) VALUES (?,?)", (username,password))
            self.conn.commit()
            
            self.c.close()
            self.conn.close()
            
            QMessageBox.information(QMessageBox(),'Successful','Register Successful')
            self.close()
        except Exception:
            QMessageBox.warning(QMessageBox(), 'Error', 'Register Fail.')


class AboutDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(AboutDialog, self).__init__(*args, **kwargs)

        self.setFixedWidth(300)
        self.setFixedHeight(250)

        QBtn = QDialogButtonBox.Ok  # No cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()

        title = QLabel("STDMGMT")
        font = title.font()
        font.setPointSize(20)
        title.setFont(font)

        labelpic = QLabel()
        pixmap = QPixmap('icon/logo.png')
        pixmap = pixmap.scaledToWidth(275)
        labelpic.setPixmap(pixmap)
        labelpic.setFixedHeight(150)

        layout.addWidget(title)

        layout.addWidget(QLabel("Version 5.3.2"))
        layout.addWidget(QLabel("Copyright 2018 CYB Inc."))
        layout.addWidget(labelpic)

        layout.addWidget(self.buttonBox)

        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.conn = sqlite3.connect("database.db")
        self.c = self.conn.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS account(roll INTEGER PRIMARY KEY AUTOINCREMENT,type TEXT,amount TEXT,category TEXT,comment TEXT,date TEXT)")
        self.c.close()

        file_menu = self.menuBar().addMenu("&File")

        help_menu = self.menuBar().addMenu("&About")
        self.setWindowTitle("Simple Accounting Management")

        self.setMinimumSize(800, 600)

        self.tableWidget = QTableWidget()
        self.setCentralWidget(self.tableWidget)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setColumnCount(6)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.tableWidget.setHorizontalHeaderLabels(("Roll No.", "Type", "Amount", "Category", "Comment", "DateTime"))

        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        statusbar = QStatusBar()
        self.setStatusBar(statusbar)

        btn_ac_adduser = QAction(QIcon("icon/add.png"), "Add Account", self)
        btn_ac_adduser.triggered.connect(self.insert)
        btn_ac_adduser.setStatusTip("Add Account")
        toolbar.addAction(btn_ac_adduser)

        btn_ac_refresh = QAction(QIcon("icon/refresh.png"),"Refresh",self)
        btn_ac_refresh.triggered.connect(self.loaddata)
        btn_ac_refresh.setStatusTip("Refresh Table")
        toolbar.addAction(btn_ac_refresh)

        btn_ac_search = QAction(QIcon("icon/search.png"), "Search", self)
        btn_ac_search.triggered.connect(self.search)
        btn_ac_search.setStatusTip("Search Account")
        toolbar.addAction(btn_ac_search)

        btn_ac_delete = QAction(QIcon("icon/trash.png"), "Delete", self)
        btn_ac_delete.triggered.connect(self.delete)
        btn_ac_delete.setStatusTip("Delete Account")
        toolbar.addAction(btn_ac_delete)

        adduser_action = QAction(QIcon("icon/add.png"),"Insert Account", self)
        adduser_action.triggered.connect(self.insert)
        file_menu.addAction(adduser_action)

        searchuser_action = QAction(QIcon("icon/search.png"), "Search Account", self)
        searchuser_action.triggered.connect(self.search)
        file_menu.addAction(searchuser_action)

        deluser_action = QAction(QIcon("icon/trash.png"), "Delete", self)
        deluser_action.triggered.connect(self.delete)
        file_menu.addAction(deluser_action)

        about_action = QAction(QIcon("icon/info.png"),"Developer", self)
        about_action.triggered.connect(self.about)
        help_menu.addAction(about_action)

    def loaddata(self):
        self.connection = sqlite3.connect("database.db")
        query = "SELECT * FROM account"
        result = self.connection.execute(query)
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number,QTableWidgetItem(str(data)))
        self.connection.close()

    # def handlePaintRequest(self, printer):
    #     document = QTextDocument()
    #     cursor = QTextCursor(document)
    #     model = self.table.model()
    #     table = cursor.insertTable(
    #         model.rowCount(), model.columnCount())
    #     for row in range(table.rows()):
    #         for column in range(table.columns()):
    #             cursor.insertText(model.item(row, column).text())
    #             cursor.movePosition(QTextCursor.NextCell)
    #     document.print_(printer)

    def insert(self):
        dlg = InsertDialog()
        dlg.exec_()

    def delete(self):
        dlg = DeleteDialog()
        dlg.exec_()

    def search(self):
        dlg = SearchDialog()
        dlg.exec_()

    def about(self):
        dlg = AboutDialog()
        dlg.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    #Login设计比较简单：只要注册过的用户都可以访问同一个database，没有对不同用户区分不同database
    passdlg = LoginDialog()
    if(passdlg.exec_() == QDialog.Accepted): 
        window = MainWindow()
        window.show()
        window.loaddata()
    sys.exit(app.exec_())