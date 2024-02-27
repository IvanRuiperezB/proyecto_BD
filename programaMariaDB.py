#Iván Ruipérez Benítez
from funcionesMariaDB import ListaAlumnos,AbreBD,CierraBD

db=AbreBD()

ListaAlumnos(db)

CierraBD(db)
