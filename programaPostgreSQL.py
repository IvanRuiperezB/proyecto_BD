#Iván Ruipérez Benítez
import psycopg2
from funciones import menu,opciones

try:
    db=psycopg2.connect(host="localhost",database="proyecto",user="ivan_proyecto",password="1234",)
except psycopg2.OperationalError as e:
    print("No puedo conectar a la base de datos:",e)
    exit()

cursor=db.cursor()

num=0
while num != 7:
    num=menu()
    opciones(num,cursor,db)

cursor.close()
db.close()