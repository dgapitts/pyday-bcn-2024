CREATE TABLE Orders (
    OrderID INT PRIMARY KEY,
    UserID INT,
    OrderTotal DECIMAL(10, 2),
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

