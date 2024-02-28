#Iván Ruipérez Benítez
import psycopg2
from tabulate import tabulate
import sys
import MySQLdb

def MariaDB_AbreBD():
    try:
        db = MySQLdb.connect("localhost","ivan_proyecto","1234","Proyecto" )
    except MySQLdb.Error as e:
        print("No puedo conectar a la base de datos:",e)
        sys.exit(1)
    return db

def MariaDB_CierraBD(db):
    db.close()

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

def MariaDB_opciones(num,db):
    if int(num) == 1:
        MariaDB_ListaAlumnos(db)
    elif int(num) == 2:
        MariaDB_AyudaIngresos(db)
    elif int(num) == 3:
        MariaDB_AlumnoTareas(db)
    elif int(num) == 4:
        MariaDB_InsertarAlumno(db)
    elif int(num) == 5:
        MariaDB_BorraAlumno(db)
    elif int(num) == 6:
        MariaDB_ActualizaDireccion(db)

def MariaDB_ListaAlumnos(db):
    sql="SELECT Alumnos.Nombre,Apellido1,Apellido2,COUNT(Practicas.ID) FROM Alumnos,Practicas WHERE Alumnos.DNI = Practicas.DNIAlumno GROUP BY Nombre,Apellido1,Apellido2;"
    cursor = db.cursor()
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
        
def MariaDB_AyudaIngresos(db):
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
    cursor=db.cursor()
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

def MariaDB_AlumnoTareas(db):
    dni=input("DNI del Alumno: ")
    sql=f"SELECT * FROM Tareas WHERE Terminada='1' AND IDPractica IN (SELECT ID FROM Practicas WHERE DNIAlumno = '{dni}')"
    cursor=db.cursor()
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
        
def MariaDB_InsertarAlumno(db):
    dni=input("DNI del alumno: ")
    direccion=input("Dirección del alumno: ")
    municipio=input("Municipio del alumno: ")
    nombre=input("Nombre del alumno: ")
    apellido1=input("Primer apellido del alumno: ")
    apellido2=input("Segundo apellido del alumno: ")
    sql=f"INSERT INTO Alumnos (DNI,Direccion,Municipio,Nombre,Apellido1,Apellido2) VALUES('{dni}','{direccion}','{municipio}','{nombre}','{apellido1}','{apellido2}')"
    cursor=db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
        print()
        print("Inserción realizada con éxito.")
    except:
        db.rollback()
        print()
        print("Inserción fallida.")
        
def MariaDB_BorraAlumno(db):
    nombre=input("Nombre del alumno: ")
    apellido1=input("Primer apellido del alumno: ")
    apellido2=input("Segundo apellido del alumno: ")
    sql=f"DELETE FROM Alumnos WHERE Nombre='{nombre}' AND Apellido1='{apellido1}' AND Apellido2='{apellido2}'"
    cursor=db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
        print()
        print("Borrado realizado con éxito.")
    except:
        db.rollback()
        print()
        print("Borrado fallido.")

def MariaDB_ActualizaDireccion(db):
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
    cursor=db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
        print()
        print("Actualización realizada con éxito.")
    except:
        db.rollback()
        print()
        print("Actualización fallida.")

def PostgreSQL_AbreBD():
    try:
        db=psycopg2.connect(host="localhost",database="proyecto",user="ivan_proyecto",password="1234",)
    except psycopg2.OperationalError as e:
        print("No puedo conectar a la base de datos:",e)
    return db
        
def PostgreSQL_CierraBD(db):
    db.close()

def PostgreSQL_opciones(num,db):
    if int(num) == 1:
        PostgreSQL_ListaAlumnos(db)
    elif int(num) == 2:
        PostgreSQL_AyudaIngresos(db)
    elif int(num) == 3:
        PostgreSQL_AlumnoTareas(db)
    elif int(num) == 4:
        PostgreSQL_InsertarAlumno(db)
    elif int(num) == 5:
        PostgreSQL_BorraAlumno(db)
    elif int(num) == 6:
        PostgreSQL_ActualizaDireccion(db)

def PostgreSQL_ListaAlumnos(db):
    sql="SELECT Alumnos.Nombre,Apellido1,Apellido2,COUNT(Practicas.ID) FROM Alumnos,Practicas WHERE Alumnos.DNI = Practicas.DNIAlumno GROUP BY Nombre,Apellido1,Apellido2;"
    cursor=db.cursor()
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
    cursor.close()

def PostgreSQL_AyudaIngresos(db):
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
    cursor=db.cursor()
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
        print("Consulta fallida.")
    cursor.close()

def PostgreSQL_AlumnoTareas(db):
    dni=input("DNI del Alumno: ")
    sql=f"SELECT * FROM Tareas WHERE Terminada='1' AND IDPractica IN (SELECT ID FROM Practicas WHERE DNIAlumno = '{dni}')"
    cursor=db.cursor()
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
        print("Consulta fallida.")
    cursor.close()

def PostgreSQL_InsertarAlumno(db):
    dni=input("DNI del alumno: ")
    direccion=input("Dirección del alumno: ")
    municipio=input("Municipio del alumno: ")
    nombre=input("Nombre del alumno: ")
    apellido1=input("Primer apellido del alumno: ")
    apellido2=input("Segundo apellido del alumno: ")
    sql=f"INSERT INTO Alumnos (DNI,Direccion,Municipio,Nombre,Apellido1,Apellido2) VALUES('{dni}','{direccion}','{municipio}','{nombre}','{apellido1}','{apellido2}')"
    cursor=db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
        print("Inserción realizada con éxito.")
    except:
        db.rollback()
        print("Inserción fallida.")
    cursor.close()

def PostgreSQL_BorraAlumno(db):
    nombre=input("Nombre del alumno: ")
    apellido1=input("Primer apellido del alumno: ")
    apellido2=input("Segundo apellido del alumno: ")
    sql=f"DELETE FROM Alumnos WHERE Nombre='{nombre}' AND Apellido1='{apellido1}' AND Apellido2='{apellido2}'"
    cursor=db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
        print()
        print("Borrado realizado con éxito.")
    except:
        db.rollback()
        print()
        print("Borrado fallido.")
    cursor.close()

def PostgreSQL_ActualizaDireccion(db):
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
    cursor=db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
        print()
        print("Actualización realizada con éxito.")
    except:
        db.rollback()
        print()
        print("Actualización fallida.")
    cursor.close()