#Iván Ruipérez Benítez
import cx_Oracle
import psycopg2
from tabulate import tabulate
import sys
import MySQLdb


def menu():
    print()
    print('''Menú
    1. Lista los alumnos y el número de prácticas de cada uno.
    2. Mostrar ayudas de desplazamiento según un rango de IngresosAnoAnterior.
    3. Pide un alumno y muestra las tareas que ha terminado.
    4. Insertar nuevo alumno.
    5. Eliminar alumno.
    6. Actualizar dirección de alumno.
    7. Salir.''')
    num=input("Elija una opción: ")
    print()
    while num.isnumeric() == False or int(num) > 7 or int(num) < 1:
        print("Esa opción no existe.")
        num=input("Elija una opción: ")
    return int(num)

def opciones(num,cursor,db):
    if int(num) == 1:
        ListaAlumnos(cursor)
    elif int(num) == 2:
        AyudaIngresos(cursor)
    elif int(num) == 3:
        AlumnoTareas(cursor)
    elif int(num) == 4:
        InsertarAlumno(cursor,db)
    elif int(num) == 5:
        BorraAlumno(cursor,db)
    elif int(num) == 6:
        ActualizaDireccion(cursor,db)

def ListaAlumnos(cursor):
    sql="SELECT Alumnos.Nombre,Apellido1,Apellido2,COUNT(Practicas.ID) FROM Alumnos,Practicas WHERE Alumnos.DNI = Practicas.DNIAlumno GROUP BY Nombre,Apellido1,Apellido2"
    datos=[]
    datos.append(["Nombre","Apellido1","Apellido2","NumPracticas"])
    try:
        cursor.execute(sql)
        registros = cursor.fetchall()
        for registro in registros:
            datos.append(registro)
        tabla= tabulate(datos, headers="firstrow", tablefmt="fancy_grid")
        print(tabla)
    except:
        print("Consulta fallida.")
        
def AyudaIngresos(cursor):
    print("Ponga dos valores para ver las ayudas de desplazamiento que tengan unos ingresos del año anterior dentro del rango introducido.")
    print()
    valor1=CompruebaValor1()
    valor2=CompruebaValor2()
    while valor1 > valor2:
        print("Valor 1 es el mínimo y valor 2 es el máximo.")
        valor1=CompruebaValor1()
        valor2=CompruebaValor2()
    print()
    sql=f"SELECT * FROM AyudasDespl WHERE (IngresosAnoAnterior BETWEEN {int(valor1)} AND {int(valor2)})"
    datos=[]
    datos.append(["FechaAyuda", "DNIAlumno", "NumUnidadFamiliar","IngresosAnoAnterior","Concedida","IDPractica"])
    try:
        cursor.execute(sql)
        registros = cursor.fetchall()
        for registro in registros:
            datos.append(registro)
        tabla= tabulate(datos, headers="firstrow", tablefmt="fancy_grid")
        print(tabla)
    except:
        print()
        print("Consulta fallida.")
    
def CompruebaValor1():
    while True:
        valor1=input("Valor 1: ")
        try:
            valor1=int(valor1)
            return valor1
        except ValueError:
            print("Error: Ingresa un valor numérico")

def CompruebaValor2():
    while True:
        valor2=input("Valor 2: ")
        try:
            valor2=int(valor2)
            return valor2
        except ValueError:
            print("Error: Ingresa un valor numérico")

def AlumnoTareas(cursor):
    dni=input("DNI del Alumno: ")
    sql=f"SELECT * FROM Tareas WHERE Terminada='1' AND IDPractica IN (SELECT ID FROM Practicas WHERE DNIAlumno = '{dni}')"
    datos=[]
    datos.append(["ID", "Nombre","Descripción","Fecha","Duración","Terminada","IDPractica"])
    try:
        cursor.execute(sql)
        registros = cursor.fetchall()
        for registro in registros:
            datos.append(registro)
        tabla= tabulate(datos, headers="firstrow", tablefmt="fancy_grid")
        print(tabla)
    except:
        print()
        print("Consulta fallida.")
        
def InsertarAlumno(cursor,db):
    dni=input("DNI del alumno: ")
    direccion=input("Dirección del alumno: ")
    municipio=input("Municipio del alumno: ")
    nombre=input("Nombre del alumno: ")
    apellido1=input("Primer apellido del alumno: ")
    apellido2=input("Segundo apellido del alumno: ")
    sql=f"INSERT INTO Alumnos (DNI,Direccion,Municipio,Nombre,Apellido1,Apellido2) VALUES('{dni}','{direccion}','{municipio}','{nombre}','{apellido1}','{apellido2}')"
    try:
        cursor.execute(sql)
        db.commit()
        print()
        print("Inserción realizada con éxito.")
    except:
        db.rollback()
        print()
        print("Inserción fallida.")
        
def BorraAlumno(cursor,db):
    nombre=input("Nombre del alumno: ")
    apellido1=input("Primer apellido del alumno: ")
    apellido2=input("Segundo apellido del alumno: ")
    sql=f"DELETE FROM Alumnos WHERE Nombre='{nombre}' AND Apellido1='{apellido1}' AND Apellido2='{apellido2}'"
    try:
        cursor.execute(sql)
        db.commit()
        print()
        print("Borrado realizado con éxito.")
    except:
        db.rollback()
        print()
        print("Borrado fallido.")

def ActualizaDireccion(cursor,db):
    print('''¿Cómo quiere seleccionar el alumno?
          1) Por DNI
          2) Por Nombre completo''')
    num=input("Elija una opción: ")
    print()
    while num.isnumeric() == False or int(num) > 2 or int(num) < 1:
        print("Esa opción no existe.")
        num=input("Elija una opción: ")
    if int(num) == 1:
        dni=input("DNI del alumno: ")
        direccion=input("Nueva dirección: ")
        sql=f"UPDATE Alumnos SET Direccion='{direccion}' WHERE DNI='{dni}'"
    elif int(num) ==2 :
        nombre=input("Nombre del alumno: ")
        apellido1=input("Primer apellido del alumno: ")
        apellido2=input("Segundo apellido del alumno: ")
        direccion=input("Nueva dirección: ")
        sql=f"UPDATE Alumnos SET Direccion='{direccion}' WHERE Nombre='{nombre}' AND Apellido1='{apellido1}' AND Apellido2='{apellido2}'"
    try:
        cursor.execute(sql)
        db.commit()
        print()
        print("Actualización realizada con éxito.")
    except:
        db.rollback()
        print()
        print("Actualización fallida.")

def MariaDB_AbreBD():
    try:
        db = MySQLdb.connect("localhost","ivan_proyecto","1234","Proyecto" )
    except MySQLdb.Error as e:
        print("No puedo conectar a la base de datos:",e)
        sys.exit(1)
    return db

def PostgreSQL_AbreBD():
    try:
        db=psycopg2.connect(host="localhost",database="proyecto",user="ivan_proyecto",password="1234",)
    except psycopg2.OperationalError as e:
        print("No puedo conectar a la base de datos:",e)
        exit()
    return db

def Oracle_AbreBD():
    try:
        db=cx_Oracle.connect(user="ivan_proyecto", password="1234",dsn="localhost/XE",encoding='UTF-8')
    except cx_Oracle.DatabaseError as e:
        print("No puedo conectar a la base de datos:",e)
        exit()
    return db