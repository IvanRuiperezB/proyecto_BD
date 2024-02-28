#Iván Ruipérez Benítez
import MySQLdb
import sys
from funciones import menu,opciones

try:
    db = MySQLdb.connect("localhost","ivan_proyecto","1234","Proyecto" )
except MySQLdb.Error as e:
    print("No puedo conectar a la base de datos:",e)
    sys.exit(1)
cursor=db.cursor()
num=0
while num != 7:
    num=menu()
    opciones(num,cursor,db)
    
cursor.close()
db.close()
