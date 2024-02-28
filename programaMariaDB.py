#Iván Ruipérez Benítez
from funciones import menu,MariaDB_opciones,MariaDB_AbreBD,MariaDB_CierraBD

db=MariaDB_AbreBD()

num=0
while num != 7:
    num=menu()
    MariaDB_opciones(num,db)

MariaDB_CierraBD(db)
