#Iván Ruipérez Benítez
from funciones import menu,opciones,Oracle_AbreBD,CierraBD

db=Oracle_AbreBD()

num=0
while num != 7:
    num=menu()
    opciones(num,db)

CierraBD(db)