import mysql.connector
from mysql.connector import errorcode
from database import cursor, db
import os

url = os.environ['DATABASE_URL']
database = url.split('/')[-1].split('?')[0]
DB_NAME = database

# Empty dictionary for tables
TABLES = {}

TABLES['PROFILE'] = (
    "CREATE TABLE `PROFILE` ("
    " `User` varchar(19) NOT NULL,"
    " `Name` varchar(20) NOT NULL,"
    " `Introduction` varchar(30) NOT NULL,"
    " `Hobby` varchar(20) NOT NULL,"
    " `Colour` varchar(10) NOT NULL,"
    " `Food` varchar(30) NOT NULL,"
    " `Movie` varchar(30) NOT NULL,"
    " `Song` varchar(20) NOT NULL,"
    " PRIMARY KEY (`User`)"
    ") ENGINE=InnoDB"
)

def create_database():
    cursor.execute(
        f"CREATE DATABASE IF NOT EXISTS {DB_NAME} DEFAULT CHARACTER SET 'utf8'"
    )
    print(f"Database {DB_NAME} created!")

# Create tables 

def create_tables():
    cursor.execute(f"USE {DB_NAME}")

    for tbl_name in TABLES:

        tbl_desc = TABLES[tbl_name]

        try:
            print(f"Making table: {tbl_name} ", end="")
            cursor.execute(tbl_desc)
        except mysql.connector.Error as err:
            # if the error is that the table already exists
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("Table already exists!")
            else:
                # if the error is something else, print the error msg
                print(err.msg)


# Create Profile
def create_profile(user_id, name, introduction, favouritehobby, favouritecolour, favouritefood, favouritemovie, favouritesong):
    
    sql = ("INSERT INTO PROFILE(User, Name, Introduction, Hobby, Colour, Food, Movie, Song) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)")
    cursor.execute(sql, (user_id, name, introduction, favouritehobby, favouritecolour, favouritefood, favouritemovie, favouritesong))
    db.commit()

    '''
    # If the profile does not already exist, we can make one
    if not check_profile_existence(user_id):
        # Add to database
        sql = ("INSERT INTO PROFILE(User, Name, Introduction, Hobby, Colour, Food, Movie, Song) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)")
        cursor.execute(sql, (user_id, name, introduction, favouritehobby, favouritecolour, favouritefood, favouritemovie, favouritesong))
        db.commit()
        #print(f"added profile for {user_id}")
        return True
    else:
        #print("A profile has already been created for this user id.")
        return False
    '''
        
# Get Info from Profile
def get_profile_info(user_id):
    
    sql = ("SELECT * FROM PROFILE WHERE User = %s")
    cursor.execute(sql, (user_id,))
    info = cursor.fetchone()
    return info

    ''''
    # Check if the user exists before getting the info
    if check_profile_existence(user_id):
        # Add to database
        sql = ("SELECT * FROM PROFILE WHERE User = %s")
        cursor.execute(sql, (user_id,))
        info = cursor.fetchone()

        return info

    else:
        #print("A profile does not exist for this user id.")
        return False
    '''

# Edit Profile
def edit_profile(user_id, field, edit):
    
    # Check whether a profile exists for the user ID
    #if check_profile_existence(user_id):

    if field == "NAME":
        
        sql = ("UPDATE PROFILE SET Name = %s WHERE User= %s")
        cursor.execute(sql, (edit, user_id))
        db.commit()
        print("NAME: Success!")
        
    elif field == "INTRODUCTION":
    
        sql = ("UPDATE PROFILE SET Introduction = %s WHERE User= %s") 
        cursor.execute(sql, (edit, user_id))
        db.commit()
        print("INTRO: Success!")
        
    elif field == "FAVOURITE HOBBY":
        
        sql = ("UPDATE PROFILE SET Hobby = %s WHERE User= %s")
        cursor.execute(sql, (edit, user_id))
        db.commit()
        print("HOBBY: Success!")
        
    elif field == "FAVOURITE COLOUR":

        sql = ("UPDATE PROFILE SET Colour = %s WHERE User= %s") 
        cursor.execute(sql, (edit, user_id))
        db.commit()
        print("COLOUR: Success!")
        
    elif field == "FAVOURITE FOOD":

        sql = ("UPDATE PROFILE SET Food = %s WHERE User= %s") 
        cursor.execute(sql, (edit, user_id))
        db.commit()
        print("FOOD: Success!")

    elif field == "FAVOURITE MOVIE":
        
        sql = ("UPDATE PROFILE SET Movie = %s WHERE User= %s")
        cursor.execute(sql, (edit, user_id))
        db.commit()
        print("MOVIE: Success!")
        
    elif field == "FAVOURITE SONG":
        
        sql = ("UPDATE PROFILE SET Song = %s WHERE User= %s")
        cursor.execute(sql, (edit, user_id))
        db.commit()
        print("SONG: Success!")
        
    # print(f"Edited profile for {user_id}")


# Delete Profile
def delete_profile(user_id):

    sql = ("DELETE FROM PROFILE WHERE User = %s")
    cursor.execute(sql, (user_id,))
    db.commit()


    '''
    # Delete if the profile already exists
    if check_profile_existence(user_id):
        # Add to database
        sql = ("DELETE FROM PROFILE WHERE User = %s")
        cursor.execute(sql, (user_id,))
        db.commit()
        # print("Profile deleted.")
        return True
    else:
        #print("A profile does not exist for this user id.")
        return False
    '''

# Check if the given user exists in the PROFILE table
def check_profile_existence(user_id):
    
    sql = ("SELECT Hobby FROM PROFILE WHERE EXISTS(SELECT * FROM PROFILE WHERE User = %s)")
    cursor.execute(sql, (user_id,))
    rows = cursor.fetchall()
    data = []
    for row in rows:
        data.append(row)

    if len(data) != 0:
        return True #("T") #True
    else:
        return False 
        #print("F") #False
    

   
    # select {COLUMN} FROM {TABLE} WHERE EXISTS(SELECT * FROM {TABLE} WHERE )
    #sql = ("SELECT Hobby FROM PROFILE WHERE EXISTS(SELECT * FROM PROFILE WHERE User=%s)")

    # sql = ("SELECT EXISTS(SELECT * from PROFILE WHERE User = %s)")
    # existence = cursor.execute(sql, (user_id,))

    # # Check if it returns 1 or 0
    # if existence == 1:
    #     # table exists
    #     return True
    # else:
    #     # table does not exist
    #     return False

#create_profile("755819001136807957", "Victoria", "Interesting", "eating", "blue", "bubbletea", "The Fault in our Stars", "Say My Name")
#create_profile("350325723304558592", "van", "hi there", "eating", "green", "potatoes", "tangled", "thomas the tank engine")
#delete_profile("755819001136807957")
#edit_profile("755819001136807957", "NAME", "Victoria Zhao")
#get_profile_info("350325723304558592")
#check_profile_existence("350325723304558592")
#check_profile_existence('350325723304558592')


#sql = ("UPDATE PROFILE SET Name = %s WHERE User= %s")
#cursor.execute(sql, ("Victoria", "755819001136807957"))
#db.commit()

#check_profile_existence("755819001136807957")


# Show Profile Table
#cursor.execute("SELECT * FROM PROFILE")
#for x in cursor:
#    print(x)

