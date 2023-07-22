import mysql.connector 
#mysql://root:your-password@localhost/nexus
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "your-password"
)

cursor = mydb.cursor()

cursor.execute("select * from nexus.student_profile;")
for thing in cursor:
  print(thing)

cursor.close()
mydb.close()