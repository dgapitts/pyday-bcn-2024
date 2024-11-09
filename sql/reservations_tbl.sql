CREATE TABLE Reservations (
    ReservationID INT PRIMARY KEY,
    UserID INT,
    SeatID VARCHAR(10),
    ReservationDate DATE,
    UNIQUE (SeatID),
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

