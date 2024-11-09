CREATE TABLE AccountBalance (
    UserID INT PRIMARY KEY,
    Balance DECIMAL(10, 2),
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

