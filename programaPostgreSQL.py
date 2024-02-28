#Iván Ruipérez Benítez
from funciones import PostgreSQL_AbreBD,menu,PostgreSQL_opciones,PostgreSQL_CierraBD

db=PostgreSQL_AbreBD()

num=0
while num != 7:
    num=menu()
    PostgreSQL_opciones(num,db)

PostgreSQL_CierraBD(db)

