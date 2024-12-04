import sys
from Transactions import *
from PyQt6 import QtWidgets
from PyQt6 import uic
from PyQt6.QtWidgets import (QMainWindow , QApplication ,
QLabel , QCheckBox , QComboBox , QListWidget , QLineEdit ,
QLineEdit , QSpinBox , QDoubleSpinBox , QSlider, QTableWidgetItem)
from PyQt6.QtCore import Qt,QDate,QDateTime
import pyodbc



class login_screen(QtWidgets.QMainWindow):
    def __init__(self):
    # Call the inherited classes __init__ method
        super(login_screen, self).__init__()
        # Load the .ui file
        uic.loadUi('Screens\\login_screen.ui', self)
        # Show the GUI
        self.show()
        self.SignUp.clicked.connect(self.signUp)
        self.Login.clicked.connect(self.login)
    
    def signUp(self):
        self.hide()
        self.view = signup_screen(self)
        self.view.show()

    def button_clicked (self,s) :
        dlg = QtWidgets.QMessageBox(self)
        dlg.setWindowTitle ("Error")
        dlg.setText (s)
        dlg.setStandardButtons (QtWidgets.QMessageBox.StandardButton.Ok)
        dlg.setIcon (QtWidgets.QMessageBox.Icon.Question)
        dlg.exec()
    
    def login(self):
        HU_ID = self.Email.text()
        password = self.Password.text()
        user_data = fetchUserData(HU_ID)
        if not password or not HU_ID:
            self.button_clicked("One or more fields has been left empty")
            return

        if user_data:
            ID, FirstName, LastName, Email, StoredPassword, Balance, Role, DOB = user_data
        else:
            self.button_clicked("Incorrect ID")
            return
        
        if password != StoredPassword:
            self.button_clicked("Incorrect Password")
            return
        
        if password == StoredPassword:
            self.hide()
            if Role == 'S': 
                self.view = student_main_screen(ID, FirstName, LastName, Email, StoredPassword, Balance, Role, DOB)
            elif Role == 'A':  
                self.view = admin_main_screen(ID, FirstName, LastName, Email, StoredPassword, Balance, Role, DOB)
            else:
                self.button_clicked("You are either banned or your request was denied")
            self.view.show()
            
class signup_screen(QtWidgets.QMainWindow):
    def __init__(self, login_screen):
    # Call the inherited classes __init__ method
        super(signup_screen, self).__init__()
        # Load the .ui file
        self.login_screen = login_screen
        uic.loadUi('Screens\\signup_screen.ui', self)
        # Show the GUI
        self.show()
        self.Back.clicked.connect(self.back)
        self.SignUp.clicked.connect(self.signup)

    def back(self):
        self.close()
        self.login_screen.show()

    def button_clicked (self) :
        dlg = QtWidgets.QMessageBox(self)
        dlg.setWindowTitle ("Error")
        dlg.setText ("One or more fields has been left empty or is incorrect")
        dlg.setStandardButtons (QtWidgets.QMessageBox.StandardButton.Ok)
        dlg.setIcon (QtWidgets.QMessageBox.Icon.Question)
        dlg.exec()

    def successful(self,s):
        dlg = QtWidgets.QMessageBox(self)
        dlg.setWindowTitle ("Done")
        dlg.setText (s)
        dlg.setStandardButtons (QtWidgets.QMessageBox.StandardButton.Ok)
        dlg.setIcon (QtWidgets.QMessageBox.Icon.Question)
        dlg.exec()
    
    def signup(self):
        F_Name = self.FirstName.text()
        L_Name = self.LastName.text()
        ID = self.ID.text()
        Email = self.Email.text()
        Password = self.Password.text()
        DOB = self.DOB.date()
        Balance = 0
        Role = 'U'

        if 'habib.edu.pk' not in Email:
            Email = None
        
        fields = [F_Name,L_Name,ID,Email,Password,DOB]
        missing = any(not field for field in fields)


        if missing:
            self.button_clicked()
        else:
            insertUser(F_Name,L_Name,ID,Email,Password,DOB,Balance,Role)
            self.successful("SignUp successful, please wait for admin to approve")
        #needs function to insert these values into the database


class student_main_screen(QtWidgets.QMainWindow):
    def __init__(self,ID,FirstName,LastName,Email,Passowrd,Balance,Role,DOB):
    # Call the inherited classes __init__ method
        super(student_main_screen, self).__init__()
        # Load the .ui file
        uic.loadUi('Screens\\student_main_screen.ui', self)
        # Show the GUI
        self.ID = ID
        self.balance = Balance
        self.FName = FirstName
        self.LName = LastName
        self.Email = Email
        self.show()
        self.Balance.setText(str(Balance))
        self.Balance.setEnabled(False)
        self.update_balance_label()


        self.MakeBet.clicked.connect(self.makebet)
        self.MyBets.clicked.connect(self.mybets)
        self.TaskList.clicked.connect(self.tasklist)
        self.TaskProgress.clicked.connect(self.taskprogress)
        self.Shop.clicked.connect(self.shop)
        self.Close.clicked.connect(self.close)

    def update_balance_label(self):
        self.Balance.setText(str(self.balance))

    def update_balance(self, new_balance):
        self.balance = new_balance
        self.update_balance_label()

    def makebet(self):
        self.hide()
        self.view = make_bet(self,self.ID,self.balance)
        self.view.show()

    def mybets(self):
        self.hide()
        self.view = my_bets(self, self.ID)
        self.view.show()

    def tasklist(self):
        self.hide()
        self.view = tasks_screen(self, self.ID)
        self.view.show()

    def taskprogress(self):
        self.hide()
        self.view = task_progress(self, self.ID)
        self.view.show()

    def shop(self):
        self.hide()

        self.view = shop_screen(self, self.ID, self.balance)
        self.view.show()

class my_bets(QtWidgets.QMainWindow):
    def __init__(self,student_main_screen, ID):
    # Call the inherited classes __init__ method
        super(my_bets, self).__init__()
        self.ID = ID
        self.std_screen = student_main_screen
        # Load the .ui file
        uic.loadUi('Screens\\my_bets.ui', self)
        # Show the GUI
        self.show()
        self.populate()
        self.Back.clicked.connect(self.back)
        self.Search.clicked.connect(self.search)
    

    def back(self):
        self.close()
        self.std_screen.show()

    def populate(self):
        self.ViewBets.setRowCount(0)  # Clear all rows
        self.ViewBets.setColumnCount(0)  # Clear all columns
        rows = fetchUserBets(self.ID)
        self.rows = rows
        self.ViewBets.setRowCount(len(rows))
        self.ViewBets.setColumnCount(9)
        new_column_names = ['Event_ID', 'Name', 'Bet_ID', 'Total_Amount', 'For/Against', 'Odds', 'End_Date', 'Start_Date', 'Ended']
        self.ViewBets.setHorizontalHeaderLabels(new_column_names)

        for row_index, row_data in enumerate(rows):
                for col_index, value in enumerate(row_data):
                    self.ViewBets.setItem(row_index, col_index, QTableWidgetItem(str(value)))
        self.ViewBets.setEnabled(False)

    def button_clicked (self,s) :
        dlg = QtWidgets.QMessageBox(self)
        dlg.setWindowTitle ("Error")
        dlg.setText (s)
        dlg.setStandardButtons (QtWidgets.QMessageBox.StandardButton.Ok)
        dlg.setIcon (QtWidgets.QMessageBox.Icon.Question)
        dlg.exec()

    def search(self):
        Name = self.EventName.text()
        For = self.For.isChecked()
        Against = self.Agaisnt.isChecked()
        self.ViewBets.clearContents()
        self.ViewBets.setRowCount(0)

        #1 Column is Name and 4 column is For/Agaisnt
        if (Name and For and not Against):
            # If Name is provided and For is selected, show only rows where Name and For match
            count = 0
            for row_index in range(len(self.rows)):
                if Name in self.rows[row_index][1] and self.rows[row_index][4] == "For":
                    self.ViewBets.insertRow(count)
                    for col_index in range(len(self.rows[row_index])):
                        self.ViewBets.setItem(count, col_index, QTableWidgetItem(str(self.rows[row_index][col_index])))
                    count += 1
        elif (Name and Against and not For):
            # If Name is provided and Against is selected, show only rows where Name and Against match
            count = 0
            for row_index in range(len(self.rows)):
                if Name in self.rows[row_index][1] and self.rows[row_index][4] == "Against":
                    self.ViewBets.insertRow(count)
                    for col_index in range(len(self.rows[row_index])):
                        self.ViewBets.setItem(count, col_index, QTableWidgetItem(str(self.rows[row_index][col_index])))
                    count += 1
        elif (not Name and For and not Against):
            # If Name is provided and For is selected, show only rows where Name and For match
            count = 0
            for row_index in range(len(self.rows)):
                if self.rows[row_index][4] == "For":
                    self.ViewBets.insertRow(count)
                    for col_index in range(len(self.rows[row_index])):
                        self.ViewBets.setItem(count, col_index, QTableWidgetItem(str(self.rows[row_index][col_index])))
                    count += 1
        elif (not Name and Against and not For):
            # If Name is provided and Against is selected, show only rows where Name and Against match
            count = 0
            for row_index in range(len(self.rows)):
                if self.rows[row_index][4] == "Against":
                    self.ViewBets.insertRow(count)
                    for col_index in range(len(self.rows[row_index])):
                        self.ViewBets.setItem(count, col_index, QTableWidgetItem(str(self.rows[row_index][col_index])))
                    count += 1
        elif Name:
            # If only Name is provided, show rows where Name matches
            count = 0
            for row_index in range(len(self.rows)):
                if Name in self.rows[row_index][1]:
                    self.ViewBets.insertRow(count)
                    for col_index in range(len(self.rows[row_index])):
                        self.ViewBets.setItem(count, col_index, QTableWidgetItem(str(self.rows[row_index][col_index])))
                    count += 1
        else:
            for row_index, row_data in enumerate(self.rows):
                self.ViewBets.insertRow(row_index)
                for col_index, value in enumerate(row_data):
                    self.ViewBets.setItem(row_index, col_index, QTableWidgetItem(str(value)))



class make_bet(QtWidgets.QMainWindow):
    def __init__(self,student_main_screen,ID,Bal):
    # Call the inherited classes __init__ method
        super(make_bet, self).__init__()
        self.std_screen = student_main_screen
        self.ID = ID
        self.Bal = Bal
        # Load the .ui file
        uic.loadUi('Screens\\make_bet.ui', self)
        # Show the GUI

        #self.addBets()
        self.show()
        rows = fetchBetEvents()
        for row in rows:
                self.BetName.addItem(row[0])
        self.BetName.currentIndexChanged.connect(self.newBet)
        self.Back.clicked.connect(self.back)
        self.PlaceBet.clicked.connect(self.placeBet)

    def addBets(self):
        Events = fetchEvents()
        for i in range(len(Events)):
            self.PlaceBet.addItems([Events[i][0]])
    
    def newBet(self):
        Event = self.BetName.currentText()
        Odds = getBetOdds(Event)[0][0].split('-')
        self.ForOdds.setText(Odds[0])
        self.AgaisntOdds.setText(Odds[1])

    def button_clicked (self,s) :
        dlg = QtWidgets.QMessageBox(self)
        dlg.setWindowTitle ("Error")
        dlg.setText (s)
        dlg.setStandardButtons (QtWidgets.QMessageBox.StandardButton.Ok)
        dlg.setIcon (QtWidgets.QMessageBox.Icon.Question)
        dlg.exec()

    def successful(self,s):
        dlg = QtWidgets.QMessageBox(self)
        dlg.setWindowTitle ("Done")
        dlg.setText (s)
        dlg.setStandardButtons (QtWidgets.QMessageBox.StandardButton.Ok)
        dlg.setIcon (QtWidgets.QMessageBox.Icon.Question)
        dlg.exec()

        
    def placeBet(self) :
        ID = self.ID
        Bal = self.Bal
        betName = self.BetName.currentText()
        # EventDetails = fetchEventDetails(betName)
        EventID = getbeteventID(betName)[0][0]
        betAmt = self.Amount.text()
        try:
            betAmt = int(betAmt)
            if (self.For.isChecked() and self.Agaisnt.isChecked()):
                self.button_clicked("Choose Only One For or Agaisnt")
            elif(not self.For.isChecked() and not self.Agaisnt.isChecked()):
                self.button_clicked("Choose One For or Agaisnt")
            elif(self.For.isChecked()):
                if betAmt > Bal:
                    self.button_clicked("Tum Gareeb Ho")
                else:
                    # updateUserBal(ID,-betAmt)
                    # generateBetEntry(EventID,ID,betAmt,True)
                    # updateEventDetials(EventID,betAmt)
                    betPlaced(ID, betAmt,EventID, "For")
                    self.successful("Bet Placed")
                    self.Bal = self.Bal - int(betAmt)
            else:
                if betAmt > Bal:
                    self.button_clicked("Tum Gareeb Ho")
                else:
                    # updateUserBal(ID,-betAmt)
                    # generateBetEntry(EventID,ID,betAmt,False)
                    # updateEventDetials(EventID,betAmt)
                    betPlaced(ID, betAmt,EventID, "Against")
                    self.successful("Bet Placed")
                    self.Bal = self.Bal - int(betAmt)
        except ValueError:
            self.button_clicked("Ajeeb o gareeb amt enter na karo")
        

    def back(self):
        self.std_screen.update_balance(self.Bal)
        self.close()
        self.std_screen.show()

class tasks_screen(QtWidgets.QMainWindow):
    def __init__(self,student_main_screen, ID):
    # Call the inherited classes __init__ method
        super(tasks_screen, self).__init__()
        self.std_screen = student_main_screen
        # Load the .ui file
        self.ID = ID
        uic.loadUi('Screens\\tasks_screen.ui', self)
        # Show the GUI
        self.show()
        self.populate()
        self.Search.clicked.connect(self.search)
        self.Back.clicked.connect(self.back)
        self.SelectTask.clicked.connect(self.selectTask)

    def back(self):
        self.close()
        self.std_screen.show()
    
    def search(self):
        EventName = self.EventID.text()
        MinReward = self.MinReward.text()
        rows = fetchTasksearch(EventName, MinReward)
        self.ShowTasks.setRowCount(len(rows))
        self.ShowTasks.setColumnCount(4)
        for row_index, row_data in enumerate(rows):
                for col_index, value in enumerate(row_data):
                    self.ShowTasks.setItem(row_index, col_index, QTableWidgetItem(str(value)))


    def populate(self):
        rows = fetchTaskEvents()
        self.ShowTasks.setRowCount(len(rows))
        self.ShowTasks.setColumnCount(4)
        for row_index, row_data in enumerate(rows):
                for col_index, value in enumerate(row_data):
                    self.ShowTasks.setItem(row_index, col_index, QTableWidgetItem(str(value)))

        

    def selectTask(self):
        self.hide()
        selected_row = self.ShowTasks.currentRow()
        self.EventName = self.ShowTasks.item(selected_row, 0).text()
        self.view = upload_task(self, self.EventName, self.ID)
        self.view.show()

class upload_task(QtWidgets.QMainWindow):
    def __init__(self,tasks_screen, EventName, ID):
    # Call the inherited classes __init__ method
        super(upload_task, self).__init__()
        uic.loadUi('Screens\\upload_task.ui', self)
        # Load the .ui file
        self.ID = ID
        self.tasks_screen = tasks_screen
        self.EventName = EventName
        self.EventID = geteventID(EventName)
        self.TaskEventID.setText(self.EventID)
        self.TaskEventID.setDisabled(True)
        self.TaskName.setText(self.EventName)
        self.TaskName.setDisabled(True)
        # Show the GUI
        self.show()

        self.taskscreen = tasks_screen
        self.Close.clicked.connect(self.back)
        self.pushButton.clicked.connect(self.upload)

    def back(self):
        self.close()
        self.taskscreen.show()
    def upload(self):
        Task_ID = self.TaskEventID.text()
        Task_Name = self.TaskName.text()
        desc = self.Desc.toPlainText()
        CompletedOn = self.CompletedOn.date()
        UploadTask(Task_ID, Task_Name, desc, CompletedOn, self.ID)
        self.close()
        self.tasks_screen.show()

class shop_screen(QtWidgets.QMainWindow):
    def __init__(self,student_main_screen, ID, balance):
    # Call the inherited classes __init__ method
        super(shop_screen, self).__init__()
        self.std_screen = student_main_screen
        self.ID = ID
        self.balance = balance
        # Load the .ui file
        uic.loadUi('Screens\\shop_screen.ui', self)
        # Show the GUI
        self.show()
        self.populate()
        self.Back.clicked.connect(self.back)
        self.Buy.clicked.connect(self.buy)
        self.Search.clicked.connect(self.search)

    def back(self):
        print(self.balance)
        self.std_screen.update_balance(self.balance)
        self.close()
        self.std_screen.show()
    def buy(self):
        selected_row = self.tableWidget.currentRow()
        Item_ID = self.tableWidget.item(selected_row, 0).text()
        Total_Cost = self.tableWidget.item(selected_row, 1).text()
        Order_placed(self.ID, Item_ID, 1, int(Total_Cost), self.balance)
        self.balance = self.balance - int(Total_Cost)


    def populate(self):

        rows = fetchShopItems()

        self.tableWidget.setRowCount(len(rows))
        self.tableWidget.setColumnCount(3)
        for row_index, row_data in enumerate(rows):
            for col_index in range(1, len(row_data)):
                self.tableWidget.setItem(row_index, col_index - 1, QTableWidgetItem(str(row_data[col_index])))
    def search(self):
        Name = self.ItemName.text()
        Min = self.MinPrice.text()
        Max = self.MaxPrice.text()
        rows = fetchShopsearch(Name, Min, Max)
        self.tableWidget.setRowCount(len(rows))
        self.tableWidget.setColumnCount(3)
        for row_index, row_data in enumerate(rows):
                for col_index, value in enumerate(row_data):
                    self.tableWidget.setItem(row_index, col_index, QTableWidgetItem(str(value)))




class task_progress(QtWidgets.QMainWindow):
    def __init__(self,student_main_screen, ID):
    # Call the inherited classes __init__ method
        super(task_progress, self).__init__()
        self.ID = ID
        self.std_screen = student_main_screen
        # Load the .ui file
        uic.loadUi('Screens\\task_progress.ui', self)
        # Show the GUI
        self.show()
        self.populate()
        self.Back.clicked.connect(self.back)

    def back(self):
        self.close()
        self.std_screen.show()
    def populate(self):
        
        rows = fetchUserTasks(self.ID)

        self.tableWidget.setRowCount(len(rows))
        self.tableWidget.setColumnCount(3)
        for row_index, row_data in enumerate(rows):
                for col_index, value in enumerate(row_data):
                    self.tableWidget.setItem(row_index, col_index, QTableWidgetItem(str(value)))


class admin_main_screen(QtWidgets.QMainWindow):
    def __init__(self,ID,FirstName,LastName,Email,Passowrd,Balance,Role,DOB):
    # Call the inherited classes __init__ method
        super(admin_main_screen, self).__init__()
        # Load the .ui file
        uic.loadUi('Screens\\admin_main_screen.ui', self)
        # Show the GUI
        self.show()
        self.ApproveStd.clicked.connect(self.approveStd)
        self.ApprovedStd.clicked.connect(self.approvedStd)
        self.ApproveTask.clicked.connect(self.approveTask)
        self.TaskHistory.clicked.connect(self.taskHistory)
        self.AddBettingEvent.clicked.connect(self.addBettingEvent)
        self.ModifyShop.clicked.connect(self.modifyShop)
        self.AddTaskEvent.clicked.connect(self.addTaskEvent)
        self.EndBettingEvent.clicked.connect(self.endBetEvent)
        self.Close.clicked.connect(self.close)

    def approveStd(self):
        self.hide()
        self.view = approve_student(self)
        self.view.show()

    def approvedStd(self):
        self.hide()
        self.view = approved_students(self)
        self.view.show()

    def approveTask(self):
        self.hide()
        self.view = approve_task_list(self)
        self.view.show()

    def taskHistory(self):
        self.hide()
        self.view = task_history(self)
        self.view.show()

    def addBettingEvent(self):
        self.hide()
        self.view = add_betting_events(self)
        self.view.show()
    
    def modifyShop(self):
        self.hide()
        self.view = modify_shops(self)
        self.view.show()

    def addTaskEvent(self):
        self.hide()
        self.view = add_task_event(self)
        self.view.show()

    def endBetEvent(self):
        self.hide()
        self.view = end_betting_event(self)
        self.view.show()



class approve_student(QtWidgets.QMainWindow):
    def __init__(self,admin_main_screen):
    # Call the inherited classes __init__ method
        super(approve_student, self).__init__()
        self.adminScreen = admin_main_screen
        # Load the .ui file
        uic.loadUi('Screens\\approve_student.ui', self)
        # Show the GUI
        self.show()
        self.populate()
        self.Back.clicked.connect(self.back)

    def back(self):
        self.close()
        self.adminScreen.show()

    def populate(self):
        
        rows = fetchUnapprovedUsers()
        self.ShowStds.setRowCount(len(rows))
        self.ShowStds.setColumnCount(6)
        for row_index, row_data in enumerate(rows):
                for col_index, value in enumerate(row_data):
                    self.ShowStds.setItem(row_index, col_index, QTableWidgetItem(str(value)))

class approve_student(QtWidgets.QMainWindow):
    def __init__(self,admin_main_screen):
    # Call the inherited classes __init__ method
        super(approve_student, self).__init__()
        self.adminScreen = admin_main_screen
        # Load the .ui file
        uic.loadUi('Screens\\approve_student.ui', self)
        # Show the GUI
        self.show()
        self.populate()
        self.Back.clicked.connect(self.back)
        self.Search.clicked.connect(self.search)
        self.Approve.clicked.connect(self.MakeStd)
        self.MakeAdmin.clicked.connect(self.MakeAd)
        self.Deny.clicked.connect(self.MakeByeBye)

    def back(self):
        self.close()
        self.adminScreen.show()

    def populate(self):
        rows = fetchUnapprovedUsers()
        self.rows = rows
        self.ShowStds.setRowCount(len(rows))
        self.ShowStds.setColumnCount(6)
        for row_index, row_data in enumerate(rows):
                for col_index, value in enumerate(row_data):
                    self.ShowStds.setItem(row_index, col_index, QTableWidgetItem(str(value)))
        self.disableEdit()

    def disableEdit(self):
        for row in range(self.ShowStds.rowCount()):
            for col in range(self.ShowStds.columnCount()):
                item = self.ShowStds.item(row, col)
                if item:
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)

    def button_clicked (self,s) :
        dlg = QtWidgets.QMessageBox(self)
        dlg.setWindowTitle ("Error")
        dlg.setText (s)
        dlg.setStandardButtons (QtWidgets.QMessageBox.StandardButton.Ok)
        dlg.setIcon (QtWidgets.QMessageBox.Icon.Question)
        dlg.exec()

    def MakeStd(self):
        selected_row = self.ShowStds.currentRow()
        if selected_row != -1:
            data = self.getRowData(selected_row)
            ID = data[0]
            Role = 'S'
            updateUserRole(ID,Role)
        else:
            self.button_clicked("Please select an entry first")
    
    def MakeAd(self):
        selected_row = self.ShowStds.currentRow()
        if selected_row != -1:
            data = self.getRowData(selected_row)
            ID = data[0]
            Role = 'A'
            updateUserRole(ID,Role)
        else:
            self.button_clicked("Please select an entry first")

    def MakeByeBye(self):
        selected_row = self.ShowStds.currentRow()
        if selected_row != -1:
            data = self.getRowData(selected_row)
            ID = data[0]
            Role = 'D'
            updateUserRole(ID,Role)
        else:
            self.button_clicked("Please select an entry first")
    
    def getRowData(self,selected_row):
        row_data = []
        for col in range(self.ShowStds.columnCount()):
            item = self.ShowStds.item(selected_row, col)
            if item:
                row_data.append(item.text())  # Append the text from each cell in the row

        return row_data

    def search(self):
        Name = self.StdName.text()
        ID = self.StdID.text()
        Email = self.Email.text()

        self.ShowStds.clearContents()
        self.ShowStds.setRowCount(0)

        if (Name and ID and Email):
            count = 0
            for row_index in range(len(self.rows)):
                if Name in (self.rows[row_index][1] + " " + self.rows[row_index][2]) and self.rows[row_index][0] == ID and self.rows[row_index][3] == Email:
                    self.ShowStds.insertRow(count)
                    for col_index in range(len(self.rows[row_index])):
                        self.ShowStds.setItem(count, col_index, QTableWidgetItem(str(self.rows[row_index][col_index])))
                    count += 1
        elif (Name and ID):
            count = 0
            for row_index in range(len(self.rows)):
                if Name in (self.rows[row_index][1] + " " + self.rows[row_index][2]) and self.rows[row_index][0] == ID:
                    self.ShowStds.insertRow(count)
                    for col_index in range(len(self.rows[row_index])):
                        self.ShowStds.setItem(count, col_index, QTableWidgetItem(str(self.rows[row_index][col_index])))
                    count += 1
        elif (Name and Email):
            count = 0
            for row_index in range(len(self.rows)):
                if Name in (self.rows[row_index][1] + " " + self.rows[row_index][2]) and self.rows[row_index][3] == Email:
                    self.ShowStds.insertRow(count)
                    for col_index in range(len(self.rows[row_index])):
                        self.ShowStds.setItem(count, col_index, QTableWidgetItem(str(self.rows[row_index][col_index])))
                    count += 1
        elif (Email and ID):
            count = 0
            for row_index in range(len(self.rows)):
                if self.rows[row_index][0] == ID and self.rows[row_index][3] == Email:
                    self.ShowStds.insertRow(count)
                    for col_index in range(len(self.rows[row_index])):
                        self.ShowStds.setItem(count, col_index, QTableWidgetItem(str(self.rows[row_index][col_index])))
                    count += 1
        elif Name:
            count = 0
            for row_index in range(len(self.rows)):
                if Name in (self.rows[row_index][1] + " " + self.rows[row_index][2]):
                    self.ShowStds.insertRow(count)
                    for col_index in range(len(self.rows[row_index])):
                        self.ShowStds.setItem(count, col_index, QTableWidgetItem(str(self.rows[row_index][col_index])))
                    count += 1
        elif ID:
            count = 0
            for row_index in range(len(self.rows)):
                if self.rows[row_index][0] == ID:
                    self.ShowStds.insertRow(count)
                    for col_index in range(len(self.rows[row_index])):
                        self.ShowStds.setItem(count, col_index, QTableWidgetItem(str(self.rows[row_index][col_index])))
                    count += 1
        elif Email:
            count = 0
            for row_index in range(len(self.rows)):
                if self.rows[row_index][3] == Email:
                    self.ShowStds.insertRow(count)
                    for col_index in range(len(self.rows[row_index])):
                        self.ShowStds.setItem(count, col_index, QTableWidgetItem(str(self.rows[row_index][col_index])))
                    count += 1
        else:
            for row_index, row_data in enumerate(self.rows):
                self.ShowStds.insertRow(row_index)
                for col_index, value in enumerate(row_data):
                    self.ShowStds.setItem(row_index, col_index, QTableWidgetItem(str(value)))
        self.disableEdit()

class approved_students(QtWidgets.QMainWindow):
    def __init__(self,admin_main_screen):
    # Call the inherited classes __init__ method
        super(approved_students, self).__init__()
        self.adminScreen = admin_main_screen
        # Load the .ui file
        uic.loadUi('Screens\\approved_students.ui', self)
        # Show the GUI
        self.show()
        self.populate()
        self.Back.clicked.connect(self.back)
        self.MakeAdmin.clicked.connect(self.MakeAd)
        self.Ban.clicked.connect(self.MakeByeBye)
        self.Search.clicked.connect(self.search)

    def back(self):
        self.close()
        self.adminScreen.show()

    def populate(self):
        
        rows = fetchStudents()
        self.rows = rows
        
        self.ShowStds.setRowCount(len(rows))
        self.ShowStds.setColumnCount(5)
        for row_index, row_data in enumerate(rows):
                for col_index, value in enumerate(row_data):
                    self.ShowStds.setItem(row_index, col_index, QTableWidgetItem(str(value)))
        self.disableEdit()

    def disableEdit(self):
        for row in range(self.ShowStds.rowCount()):
            for col in range(self.ShowStds.columnCount()):
                item = self.ShowStds.item(row, col)
                if item:
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)

    def button_clicked (self,s) :
        dlg = QtWidgets.QMessageBox(self)
        dlg.setWindowTitle ("Error")
        dlg.setText (s)
        dlg.setStandardButtons (QtWidgets.QMessageBox.StandardButton.Ok)
        dlg.setIcon (QtWidgets.QMessageBox.Icon.Question)
        dlg.exec()
    
    def MakeAd(self):
        selected_row = self.ShowStds.currentRow()
        if selected_row != -1:
            data = self.getRowData(selected_row)
            ID = data[0]
            Role = 'A'
            updateUserRole(ID,Role)
        else:
            self.button_clicked("Please select an entry first")

    def MakeByeBye(self):
        selected_row = self.ShowStds.currentRow()
        if selected_row != -1:
            data = self.getRowData(selected_row)
            ID = data[0]
            Role = 'B'
            updateUserRole(ID,Role)
        else:
            self.button_clicked("Please select an entry first")
    
    def getRowData(self,selected_row):
        row_data = []
        for col in range(self.ShowStds.columnCount()):
            item = self.ShowStds.item(selected_row, col)
            if item:
                row_data.append(item.text())  # Append the text from each cell in the row

        return row_data

    def search(self):
        Name = self.StdName.text()
        ID = self.StdId.text()
        Email = self.Email.text()

        self.ShowStds.clearContents()
        self.ShowStds.setRowCount(0)

        if (Name and ID and Email):
            count = 0
            for row_index in range(len(self.rows)):
                if Name in (self.rows[row_index][1] + " " + self.rows[row_index][2]) and self.rows[row_index][0] == ID and self.rows[row_index][3] == Email:
                    self.ShowStds.insertRow(count)
                    for col_index in range(len(self.rows[row_index])):
                        self.ShowStds.setItem(count, col_index, QTableWidgetItem(str(self.rows[row_index][col_index])))
                    count += 1
        elif (Name and ID):
            count = 0
            for row_index in range(len(self.rows)):
                if Name in (self.rows[row_index][1] + " " + self.rows[row_index][2]) and self.rows[row_index][0] == ID:
                    self.ShowStds.insertRow(count)
                    for col_index in range(len(self.rows[row_index])):
                        self.ShowStds.setItem(count, col_index, QTableWidgetItem(str(self.rows[row_index][col_index])))
                    count += 1
        elif (Name and Email):
            count = 0
            for row_index in range(len(self.rows)):
                if Name in (self.rows[row_index][1] + " " + self.rows[row_index][2]) and self.rows[row_index][3] == Email:
                    self.ShowStds.insertRow(count)
                    for col_index in range(len(self.rows[row_index])):
                        self.ShowStds.setItem(count, col_index, QTableWidgetItem(str(self.rows[row_index][col_index])))
                    count += 1
        elif (Email and ID):
            count = 0
            for row_index in range(len(self.rows)):
                if self.rows[row_index][0] == ID and self.rows[row_index][3] == Email:
                    self.ShowStds.insertRow(count)
                    for col_index in range(len(self.rows[row_index])):
                        self.ShowStds.setItem(count, col_index, QTableWidgetItem(str(self.rows[row_index][col_index])))
                    count += 1
        elif Name:
            count = 0
            for row_index in range(len(self.rows)):
                if Name in (self.rows[row_index][1] + " " + self.rows[row_index][2]):
                    self.ShowStds.insertRow(count)
                    for col_index in range(len(self.rows[row_index])):
                        self.ShowStds.setItem(count, col_index, QTableWidgetItem(str(self.rows[row_index][col_index])))
                    count += 1
        elif ID:
            count = 0
            for row_index in range(len(self.rows)):
                if self.rows[row_index][0] == ID:
                    self.ShowStds.insertRow(count)
                    for col_index in range(len(self.rows[row_index])):
                        self.ShowStds.setItem(count, col_index, QTableWidgetItem(str(self.rows[row_index][col_index])))
                    count += 1
        elif Email:
            count = 0
            for row_index in range(len(self.rows)):
                if self.rows[row_index][3] == Email:
                    self.ShowStds.insertRow(count)
                    for col_index in range(len(self.rows[row_index])):
                        self.ShowStds.setItem(count, col_index, QTableWidgetItem(str(self.rows[row_index][col_index])))
                    count += 1
        else:
            for row_index, row_data in enumerate(self.rows):
                self.ShowStds.insertRow(row_index)
                for col_index, value in enumerate(row_data):
                    self.ShowStds.setItem(row_index, col_index, QTableWidgetItem(str(value)))
        self.disableEdit()

class add_betting_events(QtWidgets.QMainWindow):
    def __init__(self,admin_main_screen):
    # Call the inherited classes __init__ method
        super(add_betting_events, self).__init__()
        self.adminScreen = admin_main_screen
        # Load the .ui file
        uic.loadUi('Screens\\add_betting_events.ui', self)
        # Show the GUI
        self.show()
        self.Back.clicked.connect(self.back)
        self.AddEvent.clicked.connect(self.addEvent)

    def back(self):
        self.close()
        self.adminScreen.show()
    def addEvent(self):
        EventName = self.EventName.text()
        Details = self.Details.text()
        StartDate = self.StartDate.date()
        EndDate = self.EndDate.date()
        AddEvent(EventName, Details, StartDate, EndDate)
        pass


class approve_task_list(QtWidgets.QMainWindow):
    def __init__(self,admin_main_screen):
    # Call the inherited classes __init__ method
        super(approve_task_list, self).__init__()
        self.adminScreen = admin_main_screen
        # Load the .ui file
        uic.loadUi('Screens\\approve_task_list.ui', self)
        # Show the GUI
        self.show()
        self.populate()
        self.Back.clicked.connect(self.back)
        self.View.clicked.connect(self.weew)
        self.Search.clicked.connect(self.search)

    def back(self):
        self.close()
        self.adminScreen.show()
    
    def weew(self):
        self.hide()
        self.weew = view_task_approval(self)
        self.weew.show()

    def populate(self):
        
        rows = fetchUnapprovedTasks()
        self.rows = rows

        self.ViewTasks.setRowCount(len(rows))
        self.ViewTasks.setColumnCount(4)
        for row_index, row_data in enumerate(rows):
                for col_index, value in enumerate(row_data):
                    self.ViewTasks.setItem(row_index, col_index, QTableWidgetItem(str(value)))
        self.disableEdit()

    def disableEdit(self):
        for row in range(self.ViewTasks.rowCount()):
            for col in range(self.ViewTasks.columnCount()):
                item = self.ViewTasks.item(row, col)
                if item:
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)

    def button_clicked (self,s) :
        dlg = QtWidgets.QMessageBox(self)
        dlg.setWindowTitle ("Error")
        dlg.setText (s)
        dlg.setStandardButtons (QtWidgets.QMessageBox.StandardButton.Ok)
        dlg.setIcon (QtWidgets.QMessageBox.Icon.Question)
        dlg.exec()

    def getRowData(self,selected_row):
        row_data = []
        for col in range(self.ViewTasks.columnCount()):
            item = self.ViewTasks.item(selected_row, col)
            if item:
                row_data.append(item.text())  # Append the text from each cell in the row

        return row_data

    def search(self):
        Name = self.TaskName.text()
        ID = self.StdID.text()

        self.ViewTasks.clearContents()
        self.ViewTasks.setRowCount(0)

        if (Name and ID):
            count = 0
            for row_index in range(len(self.rows)):
                if Name in (self.rows[row_index][1]) and self.rows[row_index][2] == ID:
                    self.ViewTasks.insertRow(count)
                    for col_index in range(len(self.rows[row_index])):
                        self.ViewTasks.setItem(count, col_index, QTableWidgetItem(str(self.rows[row_index][col_index])))
                    count += 1
        elif (Name):
            count = 0
            for row_index in range(len(self.rows)):
                if Name in (self.rows[row_index][1]):
                    self.ViewTasks.insertRow(count)
                    for col_index in range(len(self.rows[row_index])):
                        self.ViewTasks.setItem(count, col_index, QTableWidgetItem(str(self.rows[row_index][col_index])))
                    count += 1
        elif (ID):
            count = 0
            for row_index in range(len(self.rows)):
                if self.rows[row_index][2] == ID:
                    self.ViewTasks.insertRow(count)
                    for col_index in range(len(self.rows[row_index])):
                        self.ViewTasks.setItem(count, col_index, QTableWidgetItem(str(self.rows[row_index][col_index])))
                    count += 1
        else:
            for row_index, row_data in enumerate(self.rows):
                self.ViewTasks.insertRow(row_index)
                for col_index, value in enumerate(row_data):
                    self.ViewTasks.setItem(row_index, col_index, QTableWidgetItem(str(value)))
        self.disableEdit()

class view_task_approval(QtWidgets.QMainWindow):
    def __init__(self,approve_task_list):
    # Call the inherited classes __init__ method
        super(view_task_approval, self).__init__()
        # Load the .ui file
        self.tasklist = approve_task_list
        uic.loadUi('Screens\\view_task_approval.ui', self)
        # Show the GUI
        self.show()
        self.Back.clicked.connect(self.back)

    def back(self):
        self.close()
        self.tasklist.show()

class modify_shops(QtWidgets.QMainWindow):
    def __init__(self,admin_main_screen):
    # Call the inherited classes __init__ method
        super(modify_shops, self).__init__()
        self.adminScreen = admin_main_screen
        # Load the .ui file
        uic.loadUi('Screens\\modify_shops.ui', self)
        # Show the GUI
        self.show()
        self.populate()
        self.Back.clicked.connect(self.back)
        self.Search.clicked.connect(self.search)
        self.Update.clicked.connect(self.update)
        self.NewItem.clicked.connect(self.new)

    def populate(self):
        rows = fetchShopItems()

        self.ViewItems.setRowCount(len(rows))
        self.ViewItems.setColumnCount(3)
        for row_index, row_data in enumerate(rows):
                for col_index, value in enumerate(row_data):
                    self.ViewItems.setItem(row_index, col_index, QTableWidgetItem(str(value)))

    def back(self):
        self.close()
        self.adminScreen.show()

    def update(self):
        self.hide()
        selected_row = self.ViewItems.currentRow()
        Item_ID = self.ViewItems.item(selected_row, 0).text()
        ItemName = self.ViewItems.item(selected_row, 1).text()

        self.Item_ID = Item_ID
        self.ItemName = ItemName
        self.weew = update_item(self, self.Item_ID, self.ItemName)
        self.weew.show()

    def new(self):
        self.hide()
        self.weew = new_item(self)
        self.weew.show()
    
    def search(self):
        Name = self.ItemName.text()
        Min = self.MinPrice.text()
        Max = self.MaxPrice.text()
        rows = fetchShopsearch(Name, Min, Max)
        self.ViewItems.setRowCount(len(rows))
        self.ViewItems.setColumnCount(3)
        for row_index, row_data in enumerate(rows):
                for col_index, value in enumerate(row_data):
                    self.ViewItems.setItem(row_index, col_index, QTableWidgetItem(str(value)))
    
class update_item(QtWidgets.QMainWindow):
    def __init__(self,modify_shops, Item_ID, ItemName):
    # Call the inherited classes __init__ method
        super(update_item, self).__init__()
        # Load the .ui file
        uic.loadUi('Screens\\update_item.ui', self)
        # Show the GUI
        self.show()
        self.modify_shops = modify_shops
        self.Back.clicked.connect(self.back)
        self.ItemID.setText(Item_ID)
        self.ItemID.setDisabled(True)
        self.ItemName.setText(ItemName)
        self.ItemName.setDisabled(True)
        self.Create.clicked.connect(self.update)

        

    def back(self):
        self.close()
        self.modify_shops.show()
    def update(self):
        Item_ID = self.ItemID.text()
        Name = self.ItemName.text()
        Price = self.MinPrice.text()
        Stock = self.Stock.text()
        if Price != '' and Stock != '':
            Update_Shop(Item_ID, Name, Price, Stock)
        else:
            print("Input all feilds")
        

    
class new_item(QtWidgets.QMainWindow):
    def __init__(self,modify_shops):
    # Call the inherited classes __init__ method
        super(new_item, self).__init__()
        # Load the .ui file
        uic.loadUi('Screens\\new_item.ui', self)
        # Show the GUI
        self.show()
        self.modify_shops = modify_shops
        self.Create.clicked.connect(self.Add_Item)
        self.Back.clicked.connect(self.back)

    def back(self):
        self.close()
        self.modify_shops.show()
    def Add_Item(self):
        Item_Name = self.ItemName.text()
        Price = self.MinPrice.text()
        Stock = self.Stock.text()
        if Item_Name != '' and Price != '' and Stock != '':
            Add_shop(Item_Name, int(Price), int(Stock))
        else:
            print("Input all feilds")
    

class task_history(QtWidgets.QMainWindow):
    def __init__(self,admin_main_screen):
    # Call the inherited classes __init__ method
        super(task_history, self).__init__()
        self.adminScreen = admin_main_screen
        # Load the .ui file
        uic.loadUi('Screens\\task_history.ui', self)
        # Show the GUI
        self.show()
        self.populate()
        self.Back.clicked.connect(self.back)
        self.View.clicked.connect(self.view)
        self.Search.clicked.connect(self.search)

    def back(self):
        self.close()
        self.adminScreen.show()

    def view(self):
        selected_row = self.ViewTasks.currentRow()
        if selected_row != -1:
            data = self.getRowData(selected_row)
            TaskEventId = data[0]
            StudentId = data[2]
        else:
            self.button_clicked("Please select an entry first")
            return
        self.hide()
        self.view = view_task_history(self,TaskEventId,StudentId)
        self.view.show()

    def populate(self):
        rows = fetchFinishedTasks()
        self.rows = rows

        self.ViewTasks.setRowCount(len(rows))
        self.ViewTasks.setColumnCount(6)
        self.ViewTasks.setHorizontalHeaderItem(5, QTableWidgetItem("Approved/Denied"))

        for row_index, row_data in enumerate(rows):
                for col_index, value in enumerate(row_data):
                    self.ViewTasks.setItem(row_index, col_index, QTableWidgetItem(str(value)))

        self.disableEdit()

    def disableEdit(self):
        for row in range(self.ViewTasks.rowCount()):
            for col in range(self.ViewTasks.columnCount()):
                item = self.ViewTasks.item(row, col)
                if item:
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)

    def button_clicked (self,s) :
        dlg = QtWidgets.QMessageBox(self)
        dlg.setWindowTitle ("Error")
        dlg.setText (s)
        dlg.setStandardButtons (QtWidgets.QMessageBox.StandardButton.Ok)
        dlg.setIcon (QtWidgets.QMessageBox.Icon.Question)
        dlg.exec()

    def getRowData(self,selected_row):
        row_data = []
        for col in range(self.ViewTasks.columnCount()):
            item = self.ViewTasks.item(selected_row, col)
            if item:
                row_data.append(item.text())  # Append the text from each cell in the row

        return row_data

    def search(self):
        Name = self.TaskName.text()
        ID = self.StdID.text()
        Approved = self.Approved.isChecked()

        self.ViewTasks.clearContents()
        self.ViewTasks.setRowCount(0)

        if (Name and ID and Approved):
            count = 0
            for row_index in range(len(self.rows)):
                if Name in (self.rows[row_index][1]) and self.rows[row_index][2] == ID and self.rows[row_index][5] == "Approved":
                    self.ViewTasks.insertRow(count)
                    for col_index in range(len(self.rows[row_index])):
                        self.ViewTasks.setItem(count, col_index, QTableWidgetItem(str(self.rows[row_index][col_index])))
                    count += 1
        elif (Name and ID):
            count = 0
            for row_index in range(len(self.rows)):
                if Name in (self.rows[row_index][1]) and self.rows[row_index][2] == ID:
                    self.ViewTasks.insertRow(count)
                    for col_index in range(len(self.rows[row_index])):
                        self.ViewTasks.setItem(count, col_index, QTableWidgetItem(str(self.rows[row_index][col_index])))
                    count += 1
        elif (ID and Approved):
            count = 0
            for row_index in range(len(self.rows)):
                if self.rows[row_index][2] == ID and self.rows[row_index][5] == "Approved":
                    self.ViewTasks.insertRow(count)
                    for col_index in range(len(self.rows[row_index])):
                        self.ViewTasks.setItem(count, col_index, QTableWidgetItem(str(self.rows[row_index][col_index])))
                    count += 1
        elif Name and Approved:
            count = 0
            for row_index in range(len(self.rows)):
                if Name in (self.rows[row_index][1]) and self.rows[row_index][5] == "Approved":
                    self.ViewTasks.insertRow(count)
                    for col_index in range(len(self.rows[row_index])):
                        self.ViewTasks.setItem(count, col_index, QTableWidgetItem(str(self.rows[row_index][col_index])))
                    count += 1
        elif (Name):
            count = 0
            for row_index in range(len(self.rows)):
                if Name in (self.rows[row_index][1]):
                    self.ViewTasks.insertRow(count)
                    for col_index in range(len(self.rows[row_index])):
                        self.ViewTasks.setItem(count, col_index, QTableWidgetItem(str(self.rows[row_index][col_index])))
                    count += 1
        elif (ID):
            count = 0
            for row_index in range(len(self.rows)):
                if self.rows[row_index][2] == ID:
                    self.ViewTasks.insertRow(count)
                    for col_index in range(len(self.rows[row_index])):
                        self.ViewTasks.setItem(count, col_index, QTableWidgetItem(str(self.rows[row_index][col_index])))
                    count += 1
        elif Approved:
            count = 0
            for row_index in range(len(self.rows)):
                if self.rows[row_index][5] == "Approved":
                    self.ViewTasks.insertRow(count)
                    for col_index in range(len(self.rows[row_index])):
                        self.ViewTasks.setItem(count, col_index, QTableWidgetItem(str(self.rows[row_index][col_index])))
                    count += 1
        else:
            for row_index, row_data in enumerate(self.rows):
                self.ViewTasks.insertRow(row_index)
                for col_index, value in enumerate(row_data):
                    self.ViewTasks.setItem(row_index, col_index, QTableWidgetItem(str(value)))
        self.disableEdit()


class view_task_history(QtWidgets.QMainWindow):
    def __init__(self,task_history,TaskEventId,StudentId):
    # Call the inherited classes __init__ method
        super(view_task_history, self).__init__()
        # Load the .ui file
        uic.loadUi('Screens\\view_task_history.ui', self)
        # Show the GUI
        self.show()
        self.taskHistory = task_history
        self.taskEventId = TaskEventId
        self.studentId = StudentId
        self.setView()
        self.Back.clicked.connect(self.back)

    def back(self):
        self.close()
        self.taskHistory.show()

    def setView(self):
        self.TaskEventID.setText(self.taskEventId)
        self.TaskEventID.setEnabled(False)
        self.StdID.setText(self.studentId)
        self.StdID.setEnabled(False)
        data = fetchFinishedTask(self.taskEventId)
        print(data)

class add_task_event(QtWidgets.QMainWindow):
    def __init__(self,admin_main_screen):
    # Call the inherited classes __init__ method
        super(add_task_event, self).__init__()
        self.adminScreen = admin_main_screen
        # Load the .ui file
        uic.loadUi('Screens\\add_task_event.ui', self)
        # Show the GUI
        self.show()
        self.Back.clicked.connect(self.back)
        self.AddTask.clicked.connect(self.addTask)

    def back(self):
        self.close()
        self.adminScreen.show()

    def addTask(self):
        TName = self.TaskName.text()
        reward = self.Reward.text()
        startDate = self.StartDate.date()
        endDate = self.EndDate.date()

        startDate = startDate.toPyDate()  # Converts QDate to Python date
        endDate = endDate.toPyDate()      # Converts QDate to Python date

        if startDate >= endDate or startDate < QDate.currentDate():
            self.button_clicked("Dates mess up kardi hai bro")
            return
        
        if not TName:
            self.button_clicked("Event Needs a name bud")
            return
        
        if not reward:
            self.button_clicked("Event Needs a reward bud")
            return
        
        try:
            int(reward)
        except:
            self.button_clicked("Reward should be an integer value bruv")
            return
        
        insertTaskEvent(TName,startDate,endDate,reward)
        self.successful("Values Inserted Successfully")

    def button_clicked (self,s) :
        dlg = QtWidgets.QMessageBox(self)
        dlg.setWindowTitle ("Error")
        dlg.setText (s)
        dlg.setStandardButtons (QtWidgets.QMessageBox.StandardButton.Ok)
        dlg.setIcon (QtWidgets.QMessageBox.Icon.Question)
        dlg.exec()

    def successful(self,s):
        dlg = QtWidgets.QMessageBox(self)
        dlg.setWindowTitle ("Done")
        dlg.setText (s)
        dlg.setStandardButtons (QtWidgets.QMessageBox.StandardButton.Ok)
        dlg.setIcon (QtWidgets.QMessageBox.Icon.Question)
        dlg.exec()

class end_betting_event(QtWidgets.QMainWindow):
    def __init__(self,admin_main_screen):
    # Call the inherited classes __init__ method
        super(end_betting_event, self).__init__()
        self.adminScreen = admin_main_screen
        # Load the .ui file
        uic.loadUi('Screens\\end_betting_event.ui', self)
        rows = fetchBetEvents()
        for row in rows:
                self.SelectEvent.addItem(row[0])
        # Show the GUI
        self.show()
        self.EndEvent.clicked.connect(self.endEvent)
        self.Back.clicked.connect(self.back)

    def back(self):
        self.close()
        self.adminScreen.show()
    def endEvent(self):
        Event = self.SelectEvent.currentText()
        if (self.For.isChecked() and self.Agaisnt.isChecked()):
            self.button_clicked("Choose Only One For or Agaisnt")
        elif(not self.For.isChecked() and not self.Agaisnt.isChecked()):
            self.button_clicked("Choose One For or Agaisnt")
        elif(self.For.isChecked()):
            betEnded(Event, 'F')
        else:
            betEnded(Event, 'A')


    def button_clicked (self,s) :
        dlg = QtWidgets.QMessageBox(self)
        dlg.setWindowTitle ("Error")
        dlg.setText (s)
        dlg.setStandardButtons (QtWidgets.QMessageBox.StandardButton.Ok)
        dlg.setIcon (QtWidgets.QMessageBox.Icon.Question)
        dlg.exec()


    


# Create an instance of QtWidgets . QApplication
app = QtWidgets.QApplication(sys.argv)
window = login_screen() # Create an instance of our class
app.exec() # Start the application
