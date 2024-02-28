#Iván Ruipérez Benítez
from funciones import menu,opciones,MariaDB_AbreBD,CierraBD

db=MariaDB_AbreBD()
cursor=db.cursor()
num=0
while num != 7:
    num=menu()
    opciones(num,cursor,db)
cursor.close()
db.close()
