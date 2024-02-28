#Iván Ruipérez Benítez
from funciones import MariaDB_menu,MariaDB_opciones,MariaDB_AbreBD,MariaDB_CierraBD

db=MariaDB_AbreBD()

num=0
while num != 7:
    num=MariaDB_menu()
    MariaDB_opciones(num,db)

MariaDB_CierraBD(db)
