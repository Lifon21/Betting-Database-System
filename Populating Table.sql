INSERT INTO Users (User_ID, First_Name, Last_Name, Email, Password, Balance, Role, DOB) VALUES
('nk08703', 'Nofil', 'Khalid', 'nk08703@st.habib.edu.pk', '2004', 50000, 'A', '2004-12-20'),
('mh09027', 'Mustafa', 'Hussain', 'mh09027@st.habib.edu.pk', 'password123', 30000, 'A', '2004-12-16'),
('ms08702', 'Umer', 'Siddiqui', 'ms08702@st.habib.edu.pk', 'password321', 2500, 'S', '2005-02-10'),
('yz09054', 'Yusra', 'Zulfiqar', 'yz09054@st.habib.edu.pk', '0212', 1000, 'S', '2004-12-02'),
('zh08968', 'Zainab', '.', 'zh08968@st.habib.edu.pk', 'dot', 4000, 'U', '2004-07-07');

set IDENTITY_INSERT Events ON
INSERT INTO Events (Event_ID, Name, Details, Start_Date, End_Date, Odds, Ended, Pool) VALUES
('1', 'Chuttti before exams', 'Habib will give us off for finals', '2024-11-20', '2024-12-01', '2-1','F', 2000),
('2', 'HUSO', 'HUSO will happen', '2024-11-19', '2024-12-20', '1-4','F',3000),
('3', 'Database breakfast', 'Miss maria gets us breakfast', '2024-11-18', '2024-11-25', '2-3','F',6000),
('4', 'Deans list for Nofil', 'Nofil gets deans list for Fall', '2024-11-15', '2024-12-19', '4-2','F',3000),
('5', 'Mustafa survives', 'Mustafa survives the semester', '2024-11-02', '2024-12-19', '2-1','F',2500);
set IDENTITY_INSERT Events OFF


set IDENTITY_INSERT Bets ON
INSERT INTO Bets (Bet_ID, Total_Amount, [For/Against]) VALUES
('1', 500, 'For'),
('2', 300, 'Against'),
('3', 700, 'For'),
('4', 250, 'Against'),
('5', 1000, 'For');
set IDENTITY_INSERT Bets OFF

set IDENTITY_INSERT Task_Events ON
INSERT INTO Task_Events (Task_Event_ID, Name, Start_Date, End_Date, Reward) VALUES
('1', 'Daily Login', '2024-11-20', '2024-11-27', 100),
('2', 'Get Nofil sweet corn', '2024-11-20', '2024-11-27', 2000),
('3', 'Place a Bet', '2024-11-20', '2024-11-27', 150),
('4', 'Pour water on mustafa', '2024-11-20', '2024-11-27', 3000),
('5', 'Complete 3 Tasks', '2024-11-20', '2024-11-27', 500);
set IDENTITY_INSERT Task_Events OFF

set IDENTITY_INSERT Task_Done ON
INSERT INTO Task_Done (Task_ID, Name, Description, Complete_Date) VALUES
('1', 'Get Nofil sweet corn', 'Gave Nofil Sweet Corn', '2024-11-20'),
('2', 'Daily Login', 'Logged in', '2024-11-20'),
('3', 'Place a bet', 'check your records', '2024-11-19'),
('4', 'Pour water on mustafa', 'Dont let mustafa find me', '2024-11-19'),
('5', 'Daily login', 'Logged in', '2024-11-19');
set IDENTITY_INSERT Task_Done OFF

set IDENTITY_INSERT Shop ON
INSERT INTO Shop (Item_ID, Item_Name, Price, Quantity) VALUES
('1', 'A round on Nofils cycle', 300, 99),
('2', 'A lost pen', 100, 1),
('3', 'APS worksheets', 250, 25),
('4', 'Dld Cheatsheet', 350, 5),
('5', 'Pamsa Notes', 400, 8);
set IDENTITY_INSERT Shop OFF

set IDENTITY_INSERT [Order] ON
INSERT INTO [Order] (Order_ID, Quantity, Total_Cost) VALUES
('1', 1, 300),
('2', 1, 300),
('3', 5, 1250),
('4', 3, 1050),
('5', 1, 400);

set IDENTITY_INSERT [Order] OFF

INSERT INTO Shop_Order (Order_ID, Item_ID) VALUES
('1', '1'),
('2', '1'),
('3', '3'),
('4', '4'),
('5', '5');



INSERT INTO Shop_Users (Item_ID, User_ID) VALUES
('1', 'nk08703'),
('2', 'nk08703'),
('3', 'nk08703'),
('4', 'mh09027'),
('5', 'mh09027');


INSERT INTO Users_Order (Order_ID, User_ID) VALUES
('1', 'ms08702'),
('2', 'yz09054'),
('3', 'ms08702'),
('4', 'zh08968'),
('5', 'zh08968');


INSERT INTO Users_Events (Event_ID, User_ID) VALUES
('1', 'nk08703'),
('2', 'nk08703'),
('3', 'nk08703'),
('4', 'nk08703'),
('5', 'mh09027');


INSERT INTO Users_Task_Done (Task_ID, User_ID,Admin_ID ,[Approved/Denied], Comments) VALUES
('1', 'ms08702','nk08703', 'Approved', 'Nice'),
('2', 'ms08702','nk08703', 'Approved', 'Nice'),
('3', 'yz09054','nk08703', 'Approved', 'Nice'),
('4', 'zh08968','nk08703', 'Denied', 'Not Nice'),
('5', 'zh08968','nk08703', 'Approved', 'Nice');


INSERT INTO Task_Context (Task_ID, Task_Event_ID) VALUES
('1', '2'),
('2', '1'),
('3', '3'),
('4', '4'),
('5', '1');


INSERT INTO Users_Task_Events (Task_Event_ID, User_ID) VALUES
('1', 'nk08703'),
('2', 'nk08703'),
('3', 'nk08703'),
('4', 'mh09027'),
('5', 'mh09027');


INSERT INTO Users_Bets (Bet_ID, User_ID) VALUES
('1', 'yz09054'),
('2', 'yz09054'),
('3', 'ms08702'),
('4', 'ms08702'),
('5', 'ms08702');


INSERT INTO Events_Bets (Bet_ID, Event_ID) VALUES
('1', '1'),
('2', '2'), 
('3', '3'),
('4', '4'),
('5', '5');


