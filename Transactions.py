import sys
from PyQt6 import QtWidgets
from PyQt6 import uic
from PyQt6.QtWidgets import (QMainWindow , QApplication ,
QLabel , QCheckBox , QComboBox , QListWidget , QLineEdit ,
QLineEdit , QSpinBox , QDoubleSpinBox , QSlider)
from PyQt6.QtCore import Qt,QDate
from connections import *
import pyodbc

connection_string = connection_string()

def Add_shop(Item_Name, Price, Quantity):
    sql_query = """
            INSERT INTO Shop
            (Item_Name, Price, Quantity)
            VALUES ( ?, ?, ?)
        """
    connection = pyodbc.connect(connection_string)    
    cursor = connection.cursor()
    cursor.execute(sql_query, (Item_Name, Price, Quantity))
    connection.commit()
    print("Item Added")
    pass

def Update_Shop(Item_ID, Name, Price, Stock):
    sql_query = """
            Update Shop
            set Price = ?, Quantity = ?
            where Item_ID = ?
        """
    connection = pyodbc.connect(connection_string)    
    cursor = connection.cursor()
    cursor.execute(sql_query, (Price, Stock, Item_ID))
    connection.commit()
    print("Item Updated")


def Order_placed(User_ID, Item_Name, Quantity, Total_Cost, Balance):
    connection = pyodbc.connect(connection_string)    
    cursor = connection.cursor()

    sql_query = """
            INSERT INTO [Order]
            ( Quantity, Total_Cost)
            OUTPUT INSERTED.Order_ID
            VALUES ( ?, ?)
            
        """
    cursor.execute(sql_query, (Quantity, Total_Cost))

    # sql_query = "SELECT SCOPE_IDENTITY() AS LastOrderID;"

    result = cursor.fetchone()
    Order_ID = result[0] 

    sql_query = """
            UPDATE Users
            SET Balance = Balance - ?
            WHERE User_ID = ? AND Balance >= ?;
        """

    cursor.execute(sql_query, (Total_Cost, User_ID, Balance))

    sql_query = """
            Select Item_ID from Shop
            where Item_Name = ?
        """
    cursor.execute(sql_query, (Item_Name))
    result = cursor.fetchone()
    Item_ID = result[0] 
    
    sql_query = """
            Update Shop
            set Quantity = Quantity-1
            where Item_ID = ?
        """
    cursor.execute(sql_query, (Item_ID))

    sql_query = """
            INSERT INTO Shop_Order
            (Order_ID, Item_ID)
            VALUES (?, ?)
            
        """
    cursor.execute(sql_query, (Order_ID, Item_ID))

    sql_query = """
            INSERT INTO Users_Order
            (Order_ID, User_ID)
            VALUES (?, ?)
        """
    cursor.execute(sql_query, (Order_ID, User_ID))


    connection.commit()
    print("bought")

def insertTaskEvent(TName,startDate,endDate,reward):
    #inserts user data into the User table
    connection = pyodbc.connect(connection_string)    
    cursor = connection.cursor()

    sql_query = """
            INSERT INTO Task_Events
            ([Name],[Start_Date],End_Date,Reward)
            VALUES ( ?, ?, ?,?)
        """

    cursor.execute(sql_query, (TName,startDate,endDate,reward))

    connection.commit()

def insertUser(F_Name,L_Name,ID,Email,Password,qdate,Balance,Role):
    #inserts user data into the User table
    connection = pyodbc.connect(connection_string)    
    cursor = connection.cursor()

    sql_query = """
            INSERT INTO Users
            (User_ID, First_Name, Last_Name,Email,[Password],Balance,[Role],DOB)
            VALUES ( ?, ?, ?,?, ?, ?,?, ?)
        """

    cursor.execute(sql_query, (ID,F_Name,L_Name,Email,Password,Balance,Role,qdate))

    connection.commit()

def updateUserRole(ID,Role):
    connection = pyodbc.connect(connection_string)    
    cursor = connection.cursor()

    sql_query = """
            UPDATE Users
            SET Role = ?
            WHERE User_ID = ?
            
        """
    cursor.execute(sql_query, (Role,ID))

    connection.commit()
    cursor.close()
    connection.close()


def fetchUserData(HU_ID):
    #fetches a list containing the users data
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()
    query = "SELECT User_ID, First_Name, Last_Name, Email, [Password], Balance, [Role], DOB FROM Users WHERE User_ID = ?"
    cursor.execute(query, (HU_ID,))
    user_data = cursor.fetchone()

    cursor.close()
    connection.close()

    return user_data

def fetchUnapprovedUsers():
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()
    query = "select [User_ID], First_Name, Last_Name, Email, Password, DOB from Users where [Role] = 'U' "
    cursor.execute(query)

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return rows

def fetchStudents():
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()
    query = "select [User_ID], First_Name, Last_Name, Email, Password from Users where [Role] = 'S' "
    cursor.execute(query)

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return rows

def betPlaced(ID, betAmt,EventID, for_against):
    connection = pyodbc.connect(connection_string)    
    cursor = connection.cursor()

    sql_query = """
            INSERT INTO Bets
            (Total_Amount, [For/Against])
            VALUES ( ?, ?)
        """

    cursor.execute(sql_query, (betAmt, for_against))
    sql_query = """
            INSERT INTO Bets
            (Total_Amount, [For/Against])
            OUTPUT INSERTED.Bet_ID
            VALUES ( ?, ?)
        """

    cursor.execute(sql_query, (betAmt, for_against))
    result = cursor.fetchone()
    Bet_ID = result[0] 

    sql_query = """
            INSERT INTO Events_Bets
            (Bet_ID, Event_ID)
            OUTPUT INSERTED.Bet_ID
            VALUES ( ?, ?)
        """

    cursor.execute(sql_query, (Bet_ID, EventID))

    sql_query = """
            INSERT INTO Users_Bets
            (Bet_ID, User_ID)
            OUTPUT INSERTED.Bet_ID
            VALUES ( ?, ?)
        """

    cursor.execute(sql_query, (Bet_ID, ID))

    sql_query = """
            Update Users
            set Balance = Balance - ?
        """

    cursor.execute(sql_query, (betAmt))

    connection.commit()

def updateUserBal(ID,Amt):
    pass #updates the users bal by adding amt into it

def fetchEvents():
    pass #returns a list containing all the event names happening rn, and their odds
    #It should be a 2D list in the following format
    #[[EventName1,Odds1],[EventName1,Odds1]]

def fetchEventDetails(EventName):
    pass #returns a list containing all the event details for the specific event
    #can find by checking EventName and the dates it fits into

def updateEventDetials(EventID,betAmt):
    pass #updates event detail to update prize pool and change odds accordingly

def generateBetEntry(EventID,ID,Amt,For):
    pass #creates a entry in the Bet table with the details mentioned above (might need more params)

def fetchUserBets(ID): #fetches the data about all the bets user has made
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()
    query = """
        SELECT Events.Event_ID, Name, Bets.Bet_ID, Total_Amount, [For/Against], Odds, End_Date, Start_Date, Events.Ended
        FROM Events_Bets
        INNER JOIN Events ON Events.Event_ID = Events_Bets.Event_ID
        INNER JOIN Bets ON Bets.Bet_ID = Events_Bets.Bet_ID
        INNER JOIN Users_Bets ON Bets.Bet_ID = Users_Bets.Bet_ID
        WHERE Users_Bets.User_ID = ?
    """
    cursor.execute(query, (ID,))
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return rows
    
def fetchTaskEvents():
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()
    query = "select Name, Start_Date, End_Date, Reward from Task_Events;"

    cursor.execute(query)
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return rows

def fetchUserTasks(ID):
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()
    query = """SELECT Task_Events.Name, Users_Task_Done.[Approved/Denied], Task_Events.Reward
            FROM Task_Events
            JOIN Task_Context ON Task_Events.Task_Event_ID = Task_Context.Task_Event_ID
            JOIN Users_Task_Done ON Task_Context.Task_ID = Users_Task_Done.Task_ID
            where Users_Task_Done.User_ID = ?;
            """
    cursor.execute(query, (ID, ))
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return rows

def fetchUnapprovedTasks():
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()
    query = """SELECT Task_Events.Task_Event_ID, Task_Events.Name, Users_Task_Done.User_ID,(select First_Name+' '+Last_Name from Users where Users.User_ID = Users_Task_Done.User_ID)
            FROM Task_Events
            JOIN Task_Context ON Task_Events.Task_Event_ID = Task_Context.Task_Event_ID
            JOIN Users_Task_Done ON Task_Context.Task_ID = Users_Task_Done.Task_ID; """
    cursor.execute(query)
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return rows

def fetchFinishedTasks():
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()
    query = """SELECT Task_Events.Task_Event_ID, Task_Events.Name, Users_Task_Done.User_ID, (select First_Name+' '+Last_Name from Users where Users.User_ID = Users_Task_Done.User_ID), Task_Done.Complete_Date, Users_Task_Done.[Approved/Denied]
            FROM Task_Events
            JOIN Task_Context ON Task_Events.Task_Event_ID = Task_Context.Task_Event_ID
            JOIN Users_Task_Done ON Task_Context.Task_ID = Users_Task_Done.Task_ID
            JOIN Task_Done ON Users_Task_Done.Task_ID = Task_Done.Task_ID
            ;"""
    cursor.execute(query)
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return rows

def fetchFinishedTask(TaskEventID):
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()
    query = """SELECT Task_Events.Task_Event_ID, Task_Done.Complete_Date, Users_Task_Done.[Approved/Denied], Task_Done.[Description], Users_Task_Done.User_ID
            FROM Task_Events
            JOIN Task_Context ON Task_Events.Task_Event_ID = Task_Context.Task_Event_ID
            JOIN Users_Task_Done ON Task_Context.Task_ID = Users_Task_Done.Task_ID
            JOIN Task_Done ON Users_Task_Done.Task_ID = Task_Done.Task_ID
            JOIN Users ON Users_Task_Done.User_ID = Users.User_ID
            WHERE Task_Events.Task_Event_ID = ?
            ;"""
    cursor.execute(query, (TaskEventID))
    row = cursor.fetchall()

    cursor.close()
    connection.close()

    return row

    
def fetchShopItems():
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()
    query = "select Item_ID, Item_Name, Price, Quantity from Shop"
    cursor.execute(query)
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return rows

def fetchShopsearch(Name, Min, Max):
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()
    query = "select Item_Name, Price, Quantity from Shop where 1=1"
    param = []
    if Name:
        query += " and Item_Name LIKE ?"
        param.append(f"%{Name}%")
    if Min:
        query += " and Price >= ?"
        param.append(int(Min))
    if Max:
        query += " and Price <= ?"
        param.append(int(Max))
    cursor.execute(query, param)
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows

def fetchTasksearch(EventName, MinReward):
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()
    query = "select Name, Start_Date, End_Date, Reward from Task_Events where 1=1"
    param = []
    if EventName:
        query += " and Name LIKE ?"
        param.append(f"%{EventName}%")
    if MinReward:
        query += " and Reward >= ?"
        param.append(int(MinReward))
    cursor.execute(query, param)
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows

def UploadTask(TaskEventID, Name, Description, Complete_Date, UserID):
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()
    completed_on_str = Complete_Date.toString("yyyy-MM-dd")
    query = """INSERT INTO Task_Done
            (Name, Description, Complete_Date)
            OUTPUT INSERTED.Task_ID
            VALUES ( ?, ?, ?)"""
    cursor.execute(query, ( Name, Description, completed_on_str))
    result = cursor.fetchone()
    TaskID = result[0]
    query = """INSERT INTO Task_Context
            (Task_ID, Task_Event_ID)
            VALUES ( ?, ?)"""
    cursor.execute(query, ( TaskID, TaskEventID))
    query = """INSERT INTO Users_Task_Done
            (Task_ID, User_ID, [Approved/Denied])
            VALUES ( ?, ?, ?)"""
    cursor.execute(query, ( TaskID, UserID, "Pending"))

    cursor.close()
    connection.commit()
    connection.close()
    print("Sent for Approval")

def geteventID(EventName):
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()
    query = "select Task_Event_ID from Task_Events where Name=?"
    cursor.execute(query, EventName)
    rows = cursor.fetchall()
    eventID = rows[0][0]
    cursor.close()
    connection.close()
    return eventID

def fetchBetEvents():
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()
    query = "select Name from Events"
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows

def getBetOdds(eventName):
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()
    query = "select Odds from Events where Name = ?"
    cursor.execute(query, eventName)
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows

def getbeteventID(betName):
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()
    query = "select Event_ID from Events where Name = ?"
    cursor.execute(query, betName)
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows

def AddEvent(EventName,Details, StartDate, EndDate):
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()
    start = StartDate.toString("yyyy-MM-dd")
    end = EndDate.toString("yyyy-MM-dd")
    query = """INSERT INTO Events
            (Name, Details, Start_Date,End_Date,Odds,Ended)
            VALUES ( ?, ?, ?,?,?,?)"""
    cursor.execute(query, ( EventName, Details, start, end, "1-1", "F"))
    cursor.close()
    connection.commit()
    connection.close()
    print("Added")


def betEnded(Name, For_Against):
    ID = getbeteventID(Name)[0][0]
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()
    query = """UPDATE Events
            set Ended = ?
            where Event_ID = ?
            """
    cursor.execute(query, (For_Against,ID))

    query = """UPDATE Users
                SET Balance = Balance + 
                    CASE 
                        WHEN e.Ended = 'F' THEN b.Total_Amount * CAST(LEFT(e.Odds, CHARINDEX('-', e.Odds) - 1) AS FLOAT) / CAST(RIGHT(e.Odds, CHARINDEX('-', REVERSE(e.Odds)) - 1) AS FLOAT)
                        WHEN e.Ended = 'A' THEN b.Total_Amount * CAST(RIGHT(e.Odds, CHARINDEX('-', REVERSE(e.Odds)) - 1) AS FLOAT) / CAST(LEFT(e.Odds, CHARINDEX('-', e.Odds) - 1) AS FLOAT)
                        ELSE 0
                    END
                FROM Users u
                JOIN Users_Bets ub ON u.User_ID = ub.User_ID
                JOIN Bets b ON ub.Bet_ID = b.Bet_ID
                JOIN Events_Bets eb ON b.Bet_ID = eb.Bet_ID
                JOIN Events e ON eb.Event_ID = e.Event_ID
                WHERE e.Event_ID = ?;
            """
    cursor.execute(query, (ID))

    print("Bet Ended")
    cursor.close()
    connection.commit()
