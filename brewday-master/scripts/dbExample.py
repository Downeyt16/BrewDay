import mysql.connector

print("conecting")

cnx = mysql.connector.connect(user='root', password='Pa$$w0rd',
                              host = '104.196.12.188', database = 'BrewDayDB')
cursor = cnx.cursor(buffered=True)

##insert = ("INSERT INTO BrewDayDB.user " "(name, password)" 
  ##        "VALUES (%s, %s)")
##testUser = ('Trevor', 'password')

##cursor.execute(insert, testUser)
##cnx.commit()

cursor.execute('SELECT * from BrewDayDB.user WHERE name = "Trevor"')
user = cursor.fetchone()
print(user)
cursor.close()
cnx.close()

print("done")
