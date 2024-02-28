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

def menu():
    print()
    print('''Menú
    1. Lista los alumnos y el número de prácticas de cada uno.
    2. Mostrar ayudas de desplazamiento según un rango de IngresosAnoAnterior.
    3. Pide un alumno y muestra las tareas que ha terminado.
    4. Insertar nuevos alumnos.
    5. Eliminar alumnos.
    6. Actualizar dirección de alumnos.
    7. Salir.''')
    num=input("Elija una opción: ")
    print()
    while num.isnumeric() == False or int(num) > 6 or int(num) < 1:
        print("Esa opción no existe.")
        num=input("Elija una opción: ")
    return int(num)

def opciones(num,db):
    if int(num) == 1:
        ListaAlumnos(db)
    elif int(num) == 2:
        ListaAlumnos(db)
    elif int(num) == 3:
        ListaAlumnos(db)
    elif int(num) == 4:
        ListaAlumnos(db)
    elif int(num) == 5:
        ListaAlumnos(db)
    elif int(num) == 6:
        ListaAlumnos(db)