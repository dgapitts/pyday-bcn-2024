CREATE TABLE Visits (
    VisitID INT PRIMARY KEY,
    UserID INT,
    ServiceUsed VARCHAR(50),
    Date DATE,
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

