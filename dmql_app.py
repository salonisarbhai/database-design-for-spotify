import streamlit as st
import psycopg2
import pandas as pd

st.set_page_config(layout="wide")

custom_css = """
<style>
    /* Main content background color */
    .stApp {
        background-color: #93B1A6;  /* Light greenish background */
    }

    /* Text input fields styling */
    .stTextInput input, .stDateInput input {
        color: #040D12;  /* Very dark bluish color for text */
        background-color: #F5F5F5;  /* Dark greenish background */
    }

    /* Button colors */
    .stButton>button {
        color: #040D12;  /* Very dark bluish color for button text */
        background-color: #5C8374;  /* Medium greenish background */
    }

    /*  text of widgets */
    .css-145kmo2, .stTextInput .st-bx, .stTextInput .st-bw, .stTextInput .st-cj, .stTextInput .st-bv, .stTextInput .st-bt, .stTextInput .st-bs, .stTextInput .st-br, .stTextInput .st-bz, .stTextInput .st-bn {
        color: #040D12;  /* Very dark bluish color for widget text */
    }

    /*  text input */
    .css-1gkcyyc, .stTextInput .st-cj {
        color: #93B1A6;  /* Light greenish color for placeholder text */
    }
    
    /* modifying the label of the widgets */
    .css-1n6g4vv label {
        color: #5C8374;  /* Medium greenish color for labels */
    }

    /* Background color for the selected date */
    .CalendarDay__selected, .CalendarDay__selected:active, .CalendarDay__selected:hover {
        background-color: #5C8374 !important;
        color: #f0f2f6 !important;
    }

    /* Background color for the current date */
    .CalendarDay__today {
        background-color: #5C8374 !important;
        color: #f0f2f6 !important;
    }

    /* Hover states for calendar days */
    .CalendarDay:hover, .CalendarDay__hovered:hover, .CalendarDay__hovered_span:hover, .CalendarDay__selected_span:hover, .CalendarDay__last_in_range:hover {
        background-color: #93B1A6 !important;
        color: #040D12 !important;
        border-color: #5C8374 !important;
    }

    /* Adjusting the color of the date input to ensure visibility */
    .stDateInput .DateInput_input {
        color: #040D12 !important;
        background-color: #93B1A6 !important;
    }

    /* Calendar widget styles for better visibility */
    .SingleDatePicker, .SingleDatePickerInput, .DateInput, .DateInput_input {
        background-color: #93B1A6 !important;
        color: #040D12 !important;
    }

    /* Date picker dropdown (the calendar itself) */
    .SingleDatePicker_picker .DayPicker, .SingleDatePicker_picker .DayPicker__withBorder {
        background-color: #93B1A6 !important;
        color: #040D12 !important;
    }

    /* Calendar days */
    .CalendarMonth_table {
        background-color: #93B1A6 !important;
        color: #040D12 !important;
    }

    /* Navigational buttons in the calendar */
    .DayPickerNavigation_button {
        color: #040D12 !important;
    }
</style>
"""


st.markdown(custom_css, unsafe_allow_html=True)


def connect_to_db():
    return psycopg2.connect(
        dbname="spotify_db", 
        user="postgres", 
        password="Jaarvis@1999", 
        host="localhost",  
        port="5432"  
    )

st.title('DATABSE DESIGN FOR SPOTIFY')

#*********************USER DETAILS*********************************
def get_user_details():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_details LIMIT 10")
    records = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()
    return pd.DataFrame(records, columns=columns)  # Convert to DataFrame

def style_df(df):
    return df.style.set_properties(**{
        'background-color': '#f0f2f6', 
        'color': '#333',
        'border-color': 'black',
        'border-width': '1px',
        'border-style': 'solid'
    })
def insert_user_details(user_id, age, gender, device):
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "INSERT INTO user_details (UserID, Age, Gender, Device) VALUES (%s, %s, %s,%s)"
    cursor.execute(query, (user_id, age, gender, device))
    conn.commit()
    cursor.close()
    conn.close()


def update_user_age(user_id, new_age):
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "UPDATE user_details SET Age = %s WHERE UserID = %s"
    cursor.execute(query, (new_age, user_id))
    conn.commit()
    cursor.close()
    conn.close()

# Function to display the form for inserting data
def display_insert_form():
    with st.form("Insert Form"):
        user_id = st.text_input("User ID")
        age = st.text_input("Age")
        gender = st.selectbox("Gender", ['Male', 'Female', 'Other'])  # Using selectbox for gender selection
        device = st.text_input("Device")
        submitted = st.form_submit_button("Submit")
        if submitted:
            insert_user_details(user_id, age, gender, device)
            st.success("Record inserted successfully!")
            st.write("The following row has been added to the User Details:")
            # Retrieve the last inserted row by user_id assuming it's unique
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user_details WHERE UserID = %s", (user_id,))
            inserted_record = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            cursor.close()
            conn.close()
            # Convert to DataFrame and display
            inserted_df = pd.DataFrame(inserted_record, columns=columns)
            st.dataframe(style_df(inserted_df))

# Function to display the form for updating data
def display_update_form():
    with st.form("Update Form"):
        user_id = st.text_input("User ID")
        new_age = st.text_input("New Age")  # Input for new age
        submitted = st.form_submit_button("Submit")
        if submitted:
            update_user_age(user_id, new_age)  # Update the age
            st.success("User age updated successfully!")
            # Fetch the updated details to display
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user_details WHERE UserID = %s", (user_id,))
            updated_record = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            cursor.close()
            conn.close()
            if updated_record:
                updated_df = pd.DataFrame(updated_record, columns=columns)
                st.write("The updated user details are as follows:")
                st.dataframe(style_df(updated_df))
            else:
                st.error("No record found with the given User ID.")


#***********************************************ACCOUNT DETAILS**********************************************************************

def get_account_details():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM account_details LIMIT 10")
    records = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()
    return pd.DataFrame(records, columns=columns)


def insert_account_details(user_id, subscription_type, payment_date, country, plan_duration, joined_date, last_payment):
    conn = connect_to_db()
    cursor = conn.cursor()
    query = """
    INSERT INTO account_details 
    (UserID, Subscription_Type, Payment_Date, Country, Plan_Duration, Joined_Date, Last_Payment) 
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (user_id, subscription_type, payment_date, country, plan_duration, joined_date, last_payment))
    conn.commit()
    cursor.close()
    conn.close()

def update_account_details(user_id, new_subscription_type):
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "UPDATE account_details SET Subscription_Type = %s WHERE UserID = %s"
    cursor.execute(query, (new_subscription_type, user_id))
    conn.commit()
    cursor.close()
    conn.close()


# Function to display the form for inserting account data
def display_insert_account_form():
    with st.form("Insert Account Form"):
        user_id = st.text_input("User ID")
        subscription_type = st.text_input("Subscription Type")
        payment_date = st.date_input("Payment Date")
        country = st.text_input("Country")
        plan_duration = st.text_input("Plan Duration")
        joined_date = st.date_input("Joined Date")
        last_payment = st.date_input("Last Payment")
        submitted = st.form_submit_button("Submit")
        if submitted:
            insert_account_details(user_id, subscription_type, payment_date, country, plan_duration, joined_date, last_payment)
            st.success("Account record inserted successfully!")

# Function to display the form for updating account data
def display_update_account_form():
    with st.form("Update Account Form"):
        user_id = st.text_input("User ID")
        new_subscription_type = st.text_input("New Subscription Type")
        submitted = st.form_submit_button("Submit")
        if submitted:
            update_account_details(user_id, new_subscription_type)
            st.success("Account subscription type updated successfully!")


#*****************************ARTIST TABLE**********************************************************************************
def get_artist_data():
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM artist LIMIT 10")
        records = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        cursor.close()
        conn.close()
        return pd.DataFrame(records, columns=columns)

def insert_artist_details(artist_name):
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "INSERT INTO artist (Artist_Name) VALUES (%s)"
    cursor.execute(query, (artist_name,))
    conn.commit()
    cursor.close()
    conn.close()

def update_artist_details(artist_id, new_artist_name):
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "UPDATE artist SET Artist_Name = %s WHERE Artist_ID = %s"
    cursor.execute(query, (new_artist_name, artist_id))
    conn.commit()
    cursor.close()
    conn.close()

# Function to display the form for inserting artist data
def display_insert_artist_form():
    with st.form("Insert Artist Form"):
        artist_name = st.text_input("Artist Name")
        submitted = st.form_submit_button("Submit")
        if submitted:
            insert_artist_details(artist_name)
            st.success("Artist record inserted successfully!")
            # Fetch and display the new artist record
            conn = connect_to_db()
            cursor = conn.cursor()
            # Assuming RETURNING is supported to get the id of inserted row
            cursor.execute("INSERT INTO artist (Artist_Name) VALUES (%s) RETURNING Artist_ID", (artist_name,))
            artist_id = cursor.fetchone()[0]
            conn.commit()
            cursor.execute("SELECT * FROM artist WHERE Artist_ID = %s", (artist_id,))
            new_artist_record = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            cursor.close()
            conn.close()
            new_artist_df = pd.DataFrame(new_artist_record, columns=columns)
            st.dataframe(style_df(new_artist_df))

# Function to display the form for updating artist data
def display_update_artist_form():
    with st.form("Update Artist Form"):
        artist_id = st.text_input("Artist ID")
        new_artist_name = st.text_input("New Artist Name")
        submitted = st.form_submit_button("Submit")
        if submitted:
            update_artist_details(artist_id, new_artist_name)
            st.success("Artist name updated successfully!")
            # Fetch and display the updated artist record
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM artist WHERE Artist_ID = %s", (artist_id,))
            updated_artist_record = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            cursor.close()
            conn.close()
            if updated_artist_record:
                updated_artist_df = pd.DataFrame(updated_artist_record, columns=columns)
                st.dataframe(style_df(updated_artist_df))
            else:
                st.error("No record found with the given Artist ID.")

#*****************************************ALBUM*********************
def get_album_data():
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM album_table LIMIT 10")
        records = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        cursor.close()
        conn.close()
        return pd.DataFrame(records, columns=columns)

def insert_album_details(album_id, album_name, release_date, artist_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    query = """
    INSERT INTO album_table (Album_ID, Album_Name, Release_Date, Artist_ID) 
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (album_id, album_name, release_date, artist_id))
    conn.commit()
    cursor.close()
    conn.close()

# Function to update album details
def update_album_details(album_id, new_album_name):
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "UPDATE album_table SET Album_Name = %s WHERE Album_ID = %s"
    cursor.execute(query, (new_album_name, album_id))
    conn.commit()
    cursor.close()
    conn.close()



# Function to display the form for inserting album data
def display_insert_album_form():
    with st.form("Insert Album Form"):
        album_id = st.text_input("Album ID")
        album_name = st.text_input("Album Name")
        release_date = st.date_input("Release Date")
        artist_id = st.text_input("Artist ID")
        submitted = st.form_submit_button("Submit")
        if submitted:
            insert_album_details(album_id, album_name, release_date, artist_id)
            st.success("Album record inserted successfully!")
            # Show the inserted record
            show_inserted_album(album_id)

# Function to display the form for updating album data
def display_update_album_form():
    with st.form("Update Album Form"):
        album_id = st.text_input("Album ID")
        new_album_name = st.text_input("New Album Name")
        submitted = st.form_submit_button("Submit")
        if submitted:
            update_album_details(album_id, new_album_name)
            st.success("Album name updated successfully!")
            # Show the updated record
            show_updated_album(album_id)



# Function to show the inserted album record
def show_inserted_album(album_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM album_table WHERE Album_ID = %s", (album_id,))
    inserted_record = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()
    if inserted_record:
        inserted_df = pd.DataFrame(inserted_record, columns=columns)
        st.dataframe(style_df(inserted_df))
    else:
        st.error("The record was not inserted successfully or doesn't exist.")

# Function to show the updated album record
def show_updated_album(album_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM album_table WHERE Album_ID = %s", (album_id,))
    updated_record = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()
    if updated_record:
        updated_df = pd.DataFrame(updated_record, columns=columns)
        st.dataframe(style_df(updated_df))
    else:
        st.error("No record found with the given Album ID.")



#************************Playlist******************************
def get_playlist_data():
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM playlist_table LIMIT 10")
        records = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        cursor.close()
        conn.close()
        return pd.DataFrame(records, columns=columns)

def insert_playlist_details(playlist_id, playlist_name, playlist_genre, user_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    query = """
    INSERT INTO playlist_table (Playlist_ID, Playlist_Name, Playlist_Genre, USER_ID) 
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (playlist_id, playlist_name, playlist_genre, user_id))
    conn.commit()
    cursor.close()
    conn.close()

# Function to update playlist details
def update_playlist_details(playlist_id, new_playlist_name):
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "UPDATE playlist_table SET Playlist_Name = %s WHERE Playlist_ID = %s"
    cursor.execute(query, (new_playlist_name, playlist_id))
    conn.commit()
    cursor.close()
    conn.close()


# Function to display the form for inserting playlist data
def display_insert_playlist_form():
    with st.form("Insert Playlist Form"):
        playlist_id = st.text_input("Playlist ID")
        playlist_name = st.text_input("Playlist Name")
        playlist_genre = st.text_input("Playlist Genre")
        user_id = st.text_input("User ID")  # Assuming the user will enter a valid user ID
        submitted = st.form_submit_button("Submit")
        if submitted:
            insert_playlist_details(playlist_id, playlist_name, playlist_genre, user_id)
            st.success("Playlist record inserted successfully!")
            # Fetch and display the new playlist record
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM playlist_table WHERE Playlist_ID = %s", (playlist_id,))
            new_playlist_record = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            cursor.close()
            conn.close()
            new_playlist_df = pd.DataFrame(new_playlist_record, columns=columns)
            st.dataframe(style_df(new_playlist_df))

# Function to display the form for updating playlist data
def display_update_playlist_form():
    with st.form("Update Playlist Form"):
        playlist_id = st.text_input("Playlist ID")
        new_playlist_name = st.text_input("New Playlist Name")
        submitted = st.form_submit_button("Submit")
        if submitted:
            update_playlist_details(playlist_id, new_playlist_name)
            st.success("Playlist name updated successfully!")
            # Fetch and display the updated playlist record
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM playlist_table WHERE Playlist_ID = %s", (playlist_id,))
            updated_playlist_record = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            cursor.close()
            conn.close()
            if updated_playlist_record:
                updated_playlist_df = pd.DataFrame(updated_playlist_record, columns=columns)
                st.dataframe(style_df(updated_playlist_df))
            else:
                st.error("No record found with the given Playlist ID.")

#*************************Song*****************************************************
def get_song_details():
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM song_details_table LIMIT 10")
        records = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        cursor.close()
        conn.close()
        return pd.DataFrame(records, columns=columns)

def insert_song_details(track_id, track_name, track_album_id, track_pop, duration_ms, release_year, danceability):
    conn = connect_to_db()
    cursor = conn.cursor()
    query = """
    INSERT INTO song_details_table (Track_ID, Track_Name, Track_Album_ID, TRACK_POP, Duration_ms, Release_Year, Danceability) 
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (track_id, track_name, track_album_id, track_pop, duration_ms, release_year, danceability))
    conn.commit()
    cursor.close()
    conn.close()


# Function to update song details
def update_song_details(track_id, new_track_name):
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "UPDATE song_details_table SET Track_Name = %s WHERE Track_ID = %s"
    cursor.execute(query, (new_track_name, track_id))
    conn.commit()
    cursor.close()
    conn.close()


# Function to display the form for inserting song data
def display_insert_song_form():
    with st.form("Insert Song Form"):
        track_id = st.text_input("Track ID")
        track_name = st.text_input("Track Name")
        track_album_id = st.text_input("Track Album ID")
        track_pop = st.number_input("Track Popularity", min_value=0)
        duration_ms = st.number_input("Duration (ms)", min_value=0)
        release_year = st.number_input("Release Year", min_value=1900, max_value=2023)
        danceability = st.slider("Danceability", 0.0, 1.0)
        
        submitted = st.form_submit_button("Submit")
        if submitted:
            insert_song_details(track_id, track_name, track_album_id, track_pop, duration_ms, release_year, danceability)
            st.success("Song record inserted successfully!")

            # Fetch and display the new song record
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM song_details_table WHERE Track_ID = %s", (track_id,))
            new_song_record = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            cursor.close()
            conn.close()
            new_song_df = pd.DataFrame(new_song_record, columns=columns)
            st.dataframe(style_df(new_song_df))

# Function to display the form for updating song data
def display_update_song_form():
    with st.form("Update Song Form"):
        track_id = st.text_input("Track ID")
        new_track_name = st.text_input("New Track Name")
        submitted = st.form_submit_button("Submit")
        if submitted:
            update_song_details(track_id, new_track_name)
            st.success("Song details updated successfully!")

            # Fetch and display the updated song record
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM song_details_table WHERE Track_ID = %s", (track_id,))
            updated_song_record = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            cursor.close()
            conn.close()
            if updated_song_record:
                updated_song_df = pd.DataFrame(updated_song_record, columns=columns)
                st.dataframe(style_df(updated_song_df))
            else:
                st.error("No record found with the given Track ID.")


#***********************10 queries************************************************************
def run_query(query, params=None):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute(query, params)
    columns = [desc[0] for desc in cursor.description]
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return pd.DataFrame(data, columns=columns)

# Query 1: Playlists by User
def run_playlist_by_user_query(user_id):
    query = "SELECT * FROM playlist_table WHERE USER_ID = %s;"
    return run_query(query, (user_id,))
# Query 2: Total Songs in Playlists
def run_total_songs_in_playlists_query():
    query = """
    SELECT p.Playlist_ID, p.Playlist_Name, COUNT(sp.Track_ID) as Total_Songs
    FROM playlist_table p
    JOIN SONG_PLAYLIST_ASSOCIATION_TABLE sp ON p.Playlist_ID = sp.Playlist_ID
    GROUP BY p.Playlist_ID;
    """
    return run_query(query)

# Query 3: Top 5 Popular Songs
def run_top_5_popular_songs_query():
    query = "SELECT * FROM song_details_table ORDER BY TRACK_POP DESC LIMIT 6;"
    return run_query(query)

# Query 4: Average Age by Subscription
def run_average_age_by_subscription_query():
    query = """
    SELECT a.Subscription_Type, AVG(u.Age) as Average_Age
    FROM account_details a
    JOIN user_details u ON a.UserID = u.UserID
    GROUP BY a.Subscription_Type;
    """
    return run_query(query)

# Query 5: Artists with Recent Albums
def run_artists_with_recent_albums_query():
    query = """
    SELECT ar.Artist_Name, al.Album_ID, COUNT(sd.Track_ID) as Total_Songs
    FROM artist ar
    JOIN album_table al ON ar.Artist_ID = al.Artist_ID
    JOIN song_details_table sd ON al.Album_ID = sd.Track_Album_ID
    WHERE al.Release_Date >= CURRENT_DATE - INTERVAL '5 year'
    GROUP BY ar.Artist_Name, al.Album_ID;
    """
    return run_query(query)

# Query 6: Users and Subscription Status
def run_users_and_subscription_status_query():
    query = """
    SELECT u.UserID, u.Gender, u.Age, a.Subscription_Type
    FROM user_details u
    JOIN account_details a ON u.UserID = a.UserID;
    """
    return run_query(query)

# Query 7: Artists with Most Albums
def run_artists_with_most_albums_query():
    query = """
    SELECT ar.Artist_Name, COUNT(al.Album_ID) as Total_Albums
    FROM artist ar
    JOIN album_table al ON ar.Artist_ID = al.Artist_ID
    GROUP BY ar.Artist_Name
    ORDER BY Total_Albums DESC;
    """
    return run_query(query)

# Query 8: Most Subscribed Country
def run_most_subscribed_country_query():
    query = """
    SELECT Country, COUNT(*) as Total_Subscriptions
    FROM account_details
    GROUP BY Country
    ORDER BY Total_Subscriptions DESC
    LIMIT 1;
    """
    return run_query(query)

# Query 9 Latest Joined User Without Subscription
def run_latest_joined_users_without_subscription_query():
    query = """
    SELECT u.UserID, u.Age, u.Gender
    FROM user_details u
    LEFT JOIN account_details a ON u.UserID = a.UserID
    WHERE a.UserID IS NULL
    ORDER BY a.Joined_Date DESC;
    """
    return run_query(query)
#*****************************Delete********************************
def manage_user_data(user_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        # Run the delete queries
        delete_queries = [
            f"DELETE FROM SONG_PLAYLIST_ASSOCIATION_TABLE WHERE Playlist_ID IN (SELECT Playlist_ID FROM playlist_table WHERE USER_ID = {user_id});",
            f"DELETE FROM playlist_table WHERE USER_ID = {user_id};",
            f"DELETE FROM account_details WHERE UserID = {user_id};",
            f"DELETE FROM user_details WHERE UserID = {user_id};"
        ]

        for query in delete_queries:
            cursor.execute(query)

        # Commit the changes
        conn.commit()

        # Run the select query to verify deletion
        select_query = f"SELECT * FROM user_details WHERE UserID = {user_id};"
        cursor.execute(select_query)
        records = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        # Convert to DataFrame
        result_df = pd.DataFrame(records, columns=columns)

    except Exception as e:
        conn.rollback()  # Rollback in case of error
        raise e
    finally:
        cursor.close()
        conn.close()

    return result_df

# Query 10: Users and Favorite Genre
def run_users_and_favorite_genre_query():
    query = """
    SELECT u.UserID, MAX(p.Playlist_Genre) as Favorite_Genre
    FROM user_details u
    JOIN playlist_table p ON u.UserID = p.USER_ID
    JOIN SONG_PLAYLIST_ASSOCIATION_TABLE s ON p.Playlist_ID = s.Playlist_ID
    GROUP BY u.UserID;
    """
    return run_query(query)
#**************************************UI*********************************************************************************

# Main categories in the sidebar
main_category = st.sidebar.radio(
    "Choose a category",
    ['Home', 'User Operations', 'Account Operations', 'Artist Operations', 'Album Operations', 'Playlist Operations', 'Song Operations', 'Top 10 Searched', 'Manage User Data']
)

# Conditional display of subcategories based on main category selection
if main_category == 'User Operations':
    user_operation = st.sidebar.radio(
        "Choose an operation",
        ['Show Table', 'Insert', 'Update'],
        key='user_operations'
    )

    # Display forms or tables based on the user operation selected
    if user_operation == 'Show Table':
        user_details_df = get_user_details()
        st.dataframe(style_df(user_details_df))
    elif user_operation == 'Insert':
        display_insert_form()
        
    elif user_operation == 'Update':
        display_update_form()
        
#************************Account************************************
if main_category == 'Account Operations':
    account_operation = st.sidebar.radio(
        "Choose an operation",
        ['Show Table', 'Insert', 'Update'],
        key='user_operations'
    )

    # Display forms or tables based on the user operation selected
    if account_operation == 'Show Table':
        get_account_details_df = get_account_details()
        st.dataframe(style_df(get_account_details_df))
    elif account_operation == 'Insert':
        display_insert_account_form()
    elif account_operation == 'Update':
        display_update_account_form()
#*************************Artist*************************************

if main_category == 'Artist Operations':
    artist_operation = st.sidebar.radio(
        "Choose an operation",
        ['Show Table', 'Insert', 'Update'],
        key='user_operations'
    )

    # Display forms or tables based on the user operation selected
    if artist_operation == 'Show Table':
        get_artist_details_df = get_artist_data()
        st.dataframe(style_df(get_artist_details_df))
    elif artist_operation == 'Insert':
        display_insert_artist_form()
    elif artist_operation == 'Update':
        display_update_artist_form()
#**************************************ALBUM ************************************
        
if main_category == 'Album Operations':
    album_operation = st.sidebar.radio(
        "Choose an operation",
        ['Show Table', 'Insert', 'Update'],
        key='user_operations'
    )

    # Display forms or tables based on the user operation selected
    if album_operation == 'Show Table':
        get_album_details_df = get_album_data()
        st.dataframe(style_df(get_album_details_df))
    elif album_operation == 'Insert':
        display_insert_album_form()
    elif album_operation == 'Update':
        display_update_album_form()
#******************************************PLAYLIST TABLE***********************************************************
if main_category == 'Playlist Operations':
    playlist_operation = st.sidebar.radio(
        "Choose an operation",
        ['Show Table', 'Insert', 'Update'],
        key='user_operations'
    )

    # Display forms or tables based on the user operation selected
    if playlist_operation == 'Show Table':
        get_playlist_details_df = get_playlist_data()
        st.dataframe(style_df(get_playlist_details_df))
    elif playlist_operation == 'Insert':
        display_insert_playlist_form()
    elif playlist_operation == 'Update':
        display_update_playlist_form()
#******************************************SONG TABLE***********************************************************
if main_category == 'Song Operations':
    song_operation = st.sidebar.radio(
        "Choose an operation",
        ['Show Table', 'Insert', 'Update'],
        key='user_operations'
    )

    # Display forms or tables based on the user operation selected
    if song_operation == 'Show Table':
        get_song_details_df = get_song_details()
        st.dataframe(style_df(get_song_details_df))
    elif song_operation == 'Insert':
        display_insert_playlist_form()
    elif song_operation == 'Update':
        display_update_playlist_form()
            
#***********************************************************************************
if main_category == 'Top 10 Searched':
    top_10_query = st.sidebar.selectbox(
        'Choose a query:',
        ('Playlists by User', 'Total Songs in Playlists', 'Top 5 Popular Songs', 'Average Age by Subscription',
         'Artists with Recent Albums', 'Users and Subscription Status', 'Artists with Most Albums', 
         'Most Subscribed Country', 'Latest Joined Users Without Subscription', 'Users and Favorite Genre')
    )

    if top_10_query == 'Playlists by User':
        user_id = st.text_input('Enter User ID:')
        if st.button('Search Playlists'):
            df = run_playlist_by_user_query(user_id)
            st.dataframe(style_df(df))

    elif top_10_query == 'Total Songs in Playlists':
        if st.button('Show Total Songs in Playlists'):
            df = run_total_songs_in_playlists_query()
            st.dataframe(style_df(df))

    elif top_10_query == 'Top 5 Popular Songs':
        if st.button('Show Top 5 Popular Songs'):
            df = run_top_5_popular_songs_query()
            st.dataframe(style_df(df))

    elif top_10_query == 'Average Age by Subscription':
        if st.button('Show Average Age by Subscription'):
            df = run_average_age_by_subscription_query()
            st.dataframe(style_df(df))

    elif top_10_query == 'Artists with Recent Albums':
        if st.button('Show Artists with Recent Albums'):
            df = run_artists_with_recent_albums_query()
            st.dataframe(style_df(df))

    elif top_10_query == 'Users and Subscription Status':
        if st.button('Show Users and Subscription Status'):
            df = run_users_and_subscription_status_query()
            st.dataframe(style_df(df))

    elif top_10_query == 'Artists with Most Albums':
        if st.button('Show Artists with Most Albums'):
            df = run_artists_with_most_albums_query()
            st.dataframe(style_df(df))

    elif top_10_query == 'Most Subscribed Country':
        if st.button('Show Most Subscribed Country'):
            df = run_most_subscribed_country_query()
            st.dataframe(style_df(df))

    elif top_10_query == 'Latest Joined Users Without Subscription':
        if st.button('Show Latest Joined Users Without Subscription'):
            df = run_latest_joined_users_without_subscription_query()
            st.dataframe(style_df(df))

    elif top_10_query == 'Users and Favorite Genre':
        if st.button('Show Users and Favorite Genre'):
            df = run_users_and_favorite_genre_query()
            st.dataframe(style_df(df))

if main_category == 'Manage User Data':
    user_id = st.number_input("Enter User ID", min_value=0, step=1)
    if st.sidebar.button("Execute"):
        try:
            result_df = manage_user_data(user_id)
            st.write("User data managed successfully.")
            st.dataframe(result_df)
        except Exception as e:
            st.error(f"An error occurred: {e}")



    






































