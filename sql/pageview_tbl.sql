CREATE TABLE PageViews (
    PageID INT PRIMARY KEY,
    UserID INT,
    ViewCount INT,
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

