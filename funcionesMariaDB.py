import sys
import MySQLdb

def AbreBD():
    try:
        db = MySQLdb.connect("localhost","ivan_proyecto","1234","Proyecto" )
    except MySQLdb.Error as e:
        print("No puedo conectar a la base de datos:",e)
        sys.exit(1)
    return db

def ListaAlumnos(db):
    sql="SELECT Alumnos.Nombre,Apellido1,Apellido2,COUNT(Tareas.ID) FROM Alumnos,Practicas,Tareas Where Alumnos.DNI = Practicas.DNIAlumno AND Practicas.ID = Tareas.IDPractica GROUP BY Nombre,Apellido1,Apellido2;"
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        registros = cursor.fetchall()
        for registro in registros:
            print(registro[0],registro[1],registro[2],registro[3])
    except:
        print("Error en la consulta")

def CierraBD(db):
    db.close()