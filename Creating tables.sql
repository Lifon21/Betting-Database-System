Create table Users (
	User_ID VARCHAR(30) PRIMARY KEY,
	First_Name VARCHAR(30) NOT NULL,
	Last_Name VARCHAR(30) NOT NULL,
	Email VARCHAR(30) NOT NULL,
	[Password] VARCHAR(30) NOT NULL,
	Balance INT,
	[Role] CHAR,
	DOB Date
)

Create table [Events](
	Event_ID int IDENTITY(1,1) PRIMARY KEY,
	[Name] VARCHAR(30),
	Details VARCHAR(200),
	[Start_Date] Date,
	End_Date Date, 
	Odds VARCHAR(30),
	Ended CHAR,
	Pool int 
)

Create table Bets (
	Bet_ID int IDENTITY(1,1) PRIMARY KEY,
	Total_Amount int,
	[For/Against] VARCHAR(20)
)

CREATE TABLE Task_Events (
    Task_Event_ID INT IDENTITY(1,1) PRIMARY KEY,
    [Name] VARCHAR(30),
    [Start_Date] DATE,
    End_Date DATE, 
    Reward INT
);

Create table Task_Done(
	Task_ID int IDENTITY(1,1) PRIMARY KEY,
	Name VARCHAR(30),
	[Description] VARCHAR(200),
	Complete_Date Date
)

Create table Shop (
	Item_ID int IDENTITY(1,1) PRIMARY KEY,
	Item_Name VARCHAR(30),
	Price int,
	Quantity int
)

Create table [Order](
	Order_ID int IDENTITY(1,1) PRIMARY KEY,
	Quantity INT,
	Total_Cost INT
)

Create table [Shop_Order](
	Order_ID int,
	Item_ID int,
	Primary key(Order_ID, Item_ID),
	Foreign key (Order_ID) References [Order](Order_ID),
	Foreign key (Item_ID) References Shop(Item_ID)
)

Create table [Shop_Users](
	Item_ID int,
	User_ID VARCHAR(30),
	Primary key(User_ID, Item_ID),
	Foreign key (User_ID) References Users(User_ID),
	Foreign key (Item_ID) References Shop(Item_ID)
)

Create table [Users_Order](
	Order_ID int,
	User_ID VARCHAR(30),
	Primary key(Order_ID, User_ID),
	Foreign key (Order_ID) References [Order](Order_ID),
	Foreign key (User_ID) References Users(User_ID)
)

Create table [Users_Events](
	Event_ID int,
	User_ID VARCHAR(30),
	Primary key(Event_ID, User_ID),
	Foreign key (Event_ID) References [Events](Event_ID),
	Foreign key (User_ID) References Users(User_ID)
)

Create table [Users_Task_Done](
	Task_ID int,
	User_ID VARCHAR(30),
	Admin_ID VARCHAR(30),
	[Approved/Denied] VARCHAR(30),
	Comments VARCHAR(300),
	Primary key(Task_ID, User_ID),
	Foreign key (Task_ID) References [Task_Done](Task_ID),
	Foreign key (User_ID) References Users(User_ID)
)

Create table [Task_Context](
	Task_ID int,
	Task_Event_ID int,
	Primary key(Task_ID, Task_Event_ID),
	Foreign key (Task_ID) References [Task_Done](Task_ID),
	Foreign key (Task_Event_ID) References Task_Events(Task_Event_ID)
)

Create table [Users_Task_Events](
	Task_Event_ID int,
	User_ID VARCHAR(30),
	Primary key(Task_Event_ID, User_ID),
	Foreign key (Task_Event_ID) References [Task_Events](Task_Event_ID),
	Foreign key (User_ID) References Users(User_ID)
)

Create table [Users_Bets](
	Bet_ID int,
	User_ID VARCHAR(30),
	Primary key(Bet_ID, User_ID),
	Foreign key (Bet_ID) References [Bets](Bet_ID),
	Foreign key (User_ID) References Users(User_ID)
)


Create table [Events_Bets](
	Bet_ID int,
	Event_ID int,
	Primary key(Bet_ID, Event_ID),
	Foreign key (Bet_ID) References [Bets](Bet_ID),
	Foreign key (Event_ID) References [Events](Event_ID)
)

