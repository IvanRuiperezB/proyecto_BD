#Iván Ruipérez Benítez
from funciones import menu,Oracle_opciones,Oracle_AbreBD,Oracle_CierraBD

db=Oracle_AbreBD()

num=0
while num != 7:
    num=menu()
    Oracle_opciones(num,db)

Oracle_CierraBD(db)