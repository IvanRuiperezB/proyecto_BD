#Iván Ruipérez Benítez
import cx_Oracle
from funciones import menu,opciones

try:
    db=cx_Oracle.connect(user="ivan_proyecto", password="1234",dsn="localhost/XE",encoding='UTF-8')
except cx_Oracle.DatabaseError as e:
    print("No puedo conectar a la base de datos:",e)
    exit()
cursor=db.cursor()

num=0
while num != 7:
    num=menu()
    opciones(num,cursor,db)

cursor.close()
db.close()