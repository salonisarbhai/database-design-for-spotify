# Database_Design_For_Spotify ER - ![image](https://github.com/Sree-lekshmi99/Database_Design_For_Spotify/assets/72271005/f319acb6-7d68-4dce-9d7b-8ae08f42bda9)
In a world where technology and music are inseparably connected, our initiative intends to combine user information with Spotify playlists, providing a unique insight into their music choices, subscriptions, and more. This approach is intended to transform music suggestions and curated playlists by adapting them to users' preferences in genres, artists, albums, and more. I have used streamlit for UI.

Relational Schema:
User (USERID, Gender, Age, Device)
Account (USERID, Subscription_Type, Plan_Duration,
Country, Joined_Date, Last_Payment_Date)
Playlist (USERID, playlist_id, playlist_name,
playlist_genre)
Songs Association (track_id, playlist_id)
Song (track_id, track_name, track_album,
track_popularity, duration_ms, release_year, danceability)
5
Album (album_id, album_name, release_date, artist_id)
Artist (artist_id, artist_name)
