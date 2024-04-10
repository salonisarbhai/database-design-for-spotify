DROP TABLE IF EXISTS SONG_PLAYLIST_ASSOCIATION_TABLE CASCADE;

-- Drop the album_table if it exists
DROP TABLE IF EXISTS playlist_table CASCADE;

-- Drop the album_table if it exists
DROP TABLE IF EXISTS song_details_table CASCADE;

-- Drop the album_table if it exists
DROP TABLE IF EXISTS album_table CASCADE;

-- Drop the artist table if it exists
DROP TABLE IF EXISTS artist CASCADE;

-- Drop the account_details table if it exists
DROP TABLE IF EXISTS account_details CASCADE;

-- Drop the user_details table if it exists
DROP TABLE IF EXISTS user_details CASCADE;
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Create the user_details table
CREATE TABLE user_details (
    UserID INT PRIMARY KEY,
	Age INT,  
	Gender VARCHAR(255),
    Device VARCHAR(225)
    -- Add any additional columns here
);

-- Import data into the user_details table from the CSV file
COPY user_details FROM 'D:/DMQL/DMQL_Project/FINAL_CSV/USER_TABLE.csv' DELIMITER ',' CSV HEADER;

-- Select the first 10 entries from the user_details table to verify the import
--SELECT * FROM user_details LIMIT 10;
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
--ACCOUNT TABLE
-- Create the account_details table
CREATE TABLE account_details (
    UserID INT,
    Subscription_Type VARCHAR(255),
    Payment_Date DATE,
    Country VARCHAR(255),
    Plan_Duration VARCHAR(50),
    Joined_Date DATE,
    Last_Payment DATE,
    PRIMARY KEY (UserID),
    FOREIGN KEY (UserID) REFERENCES user_details(UserID)
);

-- Import data into the account_details table from the CSV file
COPY account_details FROM 'D:/DMQL/DMQL_Project/FINAL_CSV/ACCOUNT_TABLE.csv' DELIMITER ',' CSV HEADER;

-- Retrieve the first 10 rows from the account_details table to verify the import
--SELECT * FROM account_details LIMIT 10;

---------------------------------------------------------------------------------------
-- ARTIST_TABLE
CREATE TABLE artist (
	Artist_Name VARCHAR(255),
    Artist_ID SERIAL PRIMARY KEY
    
);

-- Import data into the song_association_table from the CSV file
COPY artist FROM 'D:/DMQL/DMQL_Project/FINAL_CSV/artist_table.csv' DELIMITER ',' CSV HEADER;

--Retrieve the first 10 rows from the playlist_table to verify the import
--SELECT * FROM artist LIMIT 10;

----------------------------------------------------------------------------------------------------------------------------------------------

-- ALBUM_TABLE
CREATE TABLE album_table (
    Album_ID VARCHAR(255) PRIMARY KEY,
    Album_Name VARCHAR(255),
    Release_Date DATE,
    Artist_ID INT,
    FOREIGN KEY (Artist_ID) REFERENCES artist(Artist_ID)
);

-- Import data into the song_association_table from the CSV file
COPY album_table FROM 'D:/DMQL/DMQL_Project/FINAL_CSV/filtered_album_table.csv' DELIMITER ',' CSV HEADER;

--Retrieve the first 10 rows from the playlist_table to verify the import
--SELECT * FROM album_table LIMIT 10;

--------------------------------------------------------------------------------------------------------------------------------------------------------------
-- SONG_DETAILS_TABLE
CREATE TABLE song_details_table (
    Track_ID VARCHAR(255) PRIMARY KEY,
    Track_Name VARCHAR(255),
    Track_Album_ID VARCHAR(255),
    TRACK_POP INT,
    Duration_ms INT,
    Release_Year INT,
    Danceability FLOAT,
    FOREIGN KEY (Track_Album_ID) REFERENCES ALBUM_TABLE(Album_ID)
);

-- Import data into the song_association_table from the CSV file
COPY song_details_table FROM 'D:/DMQL/DMQL_Project/FINAL_CSV/filtered_song_details_cleaned.csv' DELIMITER ',' CSV HEADER;

--Retrieve the first 10 rows from the playlist_table to verify the import
--SELECT * FROM song_details_table LIMIT 10;
----------------------------------------------------------------------------------------------------------------------------------------------------------------
-- PLAYLIST_TABLE
CREATE TABLE playlist_table (
    Playlist_ID VARCHAR(255) PRIMARY KEY,
	Playlist_Name VARCHAR(255),
    Playlist_Genre VARCHAR(50),
    USER_ID INT,
    FOREIGN KEY (USER_ID) REFERENCES user_details(UserID)
);

-- Import data into the song_association_table from the CSV file
COPY playlist_table FROM 'D:/DMQL/DMQL_Project/FINAL_CSV/PLAYLIST_TABLE.csv' DELIMITER ',' CSV HEADER;

--Retrieve the first 10 rows from the playlist_table to verify the import
--SELECT * FROM playlist_table LIMIT 10;

----------------------------------------------------------------------------------------------------------------------
-- SONG_PLAYLIST_ASSOCIATION_TABLE
CREATE TABLE SONG_PLAYLIST_ASSOCIATION_TABLE (
    Track_ID VARCHAR(50),
    Playlist_ID VARCHAR(50),
    PRIMARY KEY (Track_ID, Playlist_ID),
    FOREIGN KEY (Track_ID) REFERENCES SONG_DETAILS_TABLE(Track_ID),
    FOREIGN KEY (Playlist_ID) REFERENCES PLAYLIST_TABLE(Playlist_ID)
);

-- Import data into the song_association_table from the CSV file
COPY SONG_PLAYLIST_ASSOCIATION_TABLE FROM 'D:/DMQL/DMQL_Project/FINAL_CSV/filtered_song_playlist_association_cleaned.csv' DELIMITER ',' CSV HEADER;

--Retrieve the first 10 rows from the playlist_table to verify the import
SELECT * FROM SONG_PLAYLIST_ASSOCIATION_TABLE LIMIT 10;

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
INSERT INTO user_details (UserID, Age, Gender, Device) VALUES (224, 30, 'Female', 'Smartphone');
SELECT * FROM user_details WHERE UserID = 224;
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
INSERT INTO album_table (Album_ID, Album_Name, Release_Date, Artist_ID) VALUES ('album101', 'New Album', '2023-01-01', 1);
SELECT * FROM album_table WHERE Artist_ID = 1;
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
UPDATE account_details SET Subscription_Type = 'Premium' WHERE UserID = 50
UPDATE album_table SET Album_Name = 'Husn' WHERE Album_ID = "ty783e"
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- DELETE QUERY 

DELETE FROM SONG_PLAYLIST_ASSOCIATION_TABLE
WHERE Playlist_ID IN (SELECT Playlist_ID FROM playlist_table WHERE USER_ID = 50);
DELETE FROM playlist_table WHERE USER_ID = 50;
DELETE FROM account_details WHERE UserID = 50;
DELETE FROM user_details WHERE UserID = 50;


SELECT * FROM user_details WHERE UserID = 50;
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
--Query 1: Playlists by User
SELECT * FROM song_details_table ORDER BY TRACK_POP DESC LIMIT 5;

-- # Query 2: Total Songs in Playlists
    SELECT p.Playlist_ID, p.Playlist_Name, COUNT(sp.Track_ID) as Total_Songs
    FROM playlist_table p
    JOIN SONG_PLAYLIST_ASSOCIATION_TABLE sp ON p.Playlist_ID = sp.Playlist_ID
    GROUP BY p.Playlist_ID;

-- # Query 3: Top 5 Popular Songs
SELECT * FROM song_details_table ORDER BY TRACK_POP DESC LIMIT 6;

-- # Query 4: Average Age by Subscription
 SELECT a.Subscription_Type, AVG(u.Age) as Average_Age
    FROM account_details a
    JOIN user_details u ON a.UserID = u.UserID
    GROUP BY a.Subscription_Type;

-- # Query 5: Artists with Recent Albums
SELECT ar.Artist_Name, al.Album_ID, COUNT(sd.Track_ID) as Total_Songs
FROM artist ar
JOIN album_table al ON ar.Artist_ID = al.Artist_ID
JOIN song_details_table sd ON al.Album_ID = sd.Track_Album_ID
WHERE al.Release_Date >= CURRENT_DATE - INTERVAL '5 year'
GROUP BY ar.Artist_Name, al.Album_ID;

-- # Query 6: Users and Subscription Status

SELECT u.UserID, u.Gender, u.Age, a.Subscription_Type
    FROM user_details u
    JOIN account_details a ON u.UserID = a.UserID;

-- # Query 7: Artists with Most Albums

SELECT ar.Artist_Name, COUNT(al.Album_ID) as Total_Albums
FROM artist ar
JOIN album_table al ON ar.Artist_ID = al.Artist_ID
GROUP BY ar.Artist_Name
ORDER BY Total_Albums DESC;

-- # Query 8: Most Subscribed Country

SELECT Country, COUNT(*) as Total_Subscriptions
FROM account_details
GROUP BY Country
ORDER BY Total_Subscriptions DESC
LIMIT 1;

-- # Query 9 Latest Joined User Without Subscription

SELECT u.UserID, u.Age, u.Gender
FROM user_details u
LEFT JOIN account_details a ON u.UserID = a.UserID
WHERE a.UserID IS NULL
ORDER BY a.Joined_Date DESC;

-- # Query 10: Users and Favorite Genre

SELECT u.UserID, MAX(p.Playlist_Genre) as Favorite_Genre
FROM user_details u
JOIN playlist_table p ON u.UserID = p.USER_ID
JOIN SONG_PLAYLIST_ASSOCIATION_TABLE s ON p.Playlist_ID = s.Playlist_ID
GROUP BY u.UserID;


-- Explain 
-- Query 2
EXPLAIN SELECT p.Playlist_ID, p.Playlist_Name, COUNT(sp.Track_ID) as Total_Songs
FROM playlist_table p
JOIN SONG_PLAYLIST_ASSOCIATION_TABLE sp ON p.Playlist_ID = sp.Playlist_ID
GROUP BY p.Playlist_ID;

-- Query 5
EXPLAIN SELECT ar.Artist_Name, al.Album_ID, COUNT(sd.Track_ID) as Total_Songs
    FROM artist ar
    JOIN album_table al ON ar.Artist_ID = al.Artist_ID
    JOIN song_details_table sd ON al.Album_ID = sd.Track_Album_ID
    WHERE al.Release_Date >= CURRENT_DATE - INTERVAL '5 year'
    GROUP BY ar.Artist_Name, al.Album_ID;

-- Query 10
EXPLAIN SELECT u.UserID, MAX(p.Playlist_Genre) as Favorite_Genre
    FROM user_details u
    JOIN playlist_table p ON u.UserID = p.USER_ID
    JOIN SONG_PLAYLIST_ASSOCIATION_TABLE s ON p.Playlist_ID = s.Playlist_ID
    GROUP BY u.UserID;




































