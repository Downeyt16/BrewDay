import mysql.connector
def connectDB():
    cnx = mysql.connector.connect(user='root', password='Pa$$w0rd',
                    host ='104.196.12.188', database = 'BrewDayDB')
    cursor = cnx.cursor(buffered=True)
    return cnx, cursor
def closeConnection(cnx, cursor):
    cursor.close()
    cnx.close()
    return
