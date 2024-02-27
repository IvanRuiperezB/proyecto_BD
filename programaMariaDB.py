#Iván Ruipérez Benítez
import sys,MySQLdb
try:
	db = MySQLdb.connect("localhost","ivan_proyecto","1234","Proyecto" )
except MySQLdb.Error as e:
	print("No puedo conectar a la base de datos:",e)
	sys.exit(1)

