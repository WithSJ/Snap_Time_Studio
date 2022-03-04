import sqlite3,os
DBPATH = "app//static//Database//"
def create_database():
    con = sqlite3.connect(DBPATH+'database.db')
    cur = con.cursor()
    # Create tables
    cur.execute('''CREATE TABLE PhotosLib
                (Id text,Title text, DateTime text, ImageName text, ImageTag text)''')
    
    cur.execute('''CREATE TABLE VideosLib
                (Id text,Title text, VideoUrl text, VideoTag text)''')
    
    cur.execute('''CREATE TABLE Accounts
                (   Id text,
                    FullName text, 
                    Email text, 
                    Password256 text,
                    PasswordHash text, 
                    LocalId text, 
                    IdToken text,
                    AdminRoll boolean)''')



    # Save (commit) the changes
    con.commit()

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    con.close()

    os.mkdir(DBPATH+"Photos")

def post_new_photo(id,title,dateTime,image,imgaeTag=None):
    con = sqlite3.connect(DBPATH+'database.db')
    cur = con.cursor()

    imageName = str(title).replace(" ","") + str(id)
    if image != None:
        image.save(DBPATH+"Photos/"+imageName)
    
    cur.execute('''INSERT INTO PhotosLib(Id,Title, DateTime, ImageName, ImageTag)
                    VALUES (:id,:title, :dateTime, :imageName, :imageTag)''',
                    {"id":id,"title":title,"dateTime":dateTime,
                        "imageName":imageName, "imageTag":imgaeTag})
    
    con.commit()
    con.close()



def get_all_photos():
    con = sqlite3.connect(DBPATH+'database.db')
    cur = con.cursor()
    
    cur.execute("SELECT * FROM PhotosLib ORDER BY DateTime DESC")
    allPhotos = cur.fetchall()
    con.commit()
    con.close()

    return allPhotos

    
if __name__ == "__main__":
    create_database()




