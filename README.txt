The project consists 7 csv. User.csv, Account.csv, Playlist.csv, Song.csv, SongAssociation.cs, Album.csv, Artist.csv. 
The code structure is:
    create.sql: This file consists of the queries regarding creation, deletion and updation of the tables. Besides this it also consists of the 10 Select queries. The loading of the databse is also done inside this file. This is why we do not have a separate load.sql file. 

    dmql_app.py: It consists of the code and the queries for the UI. The host, the address and the port needs to be changed in this file according to the system used and postgresql version. 

How to run? 

streamlit run dmql_app.py 