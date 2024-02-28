#Iván Ruipérez Benítez
from funciones import PostgreSQL_AbreBD,menu,opciones

db=PostgreSQL_AbreBD()
cursor=db.cursor()

num=0
while num != 7:
    num=menu()
    opciones(num,cursor,db)

cursor.close()
db.close()