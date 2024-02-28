#Iván Ruipérez Benítez
from funcionesMariaDB import menu,opciones,AbreBD,CierraBD

db=AbreBD()

num=0
while num != 7:
    num=menu()
    opciones(num,db)

CierraBD(db)
