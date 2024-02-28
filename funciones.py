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

def MariaDB_menu():
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
    sql="SELECT Alumnos.Nombre,Apellido1,Apellido2,COUNT(Tareas.ID) FROM Alumnos,Practicas,Tareas WHERE Alumnos.DNI = Practicas.DNIAlumno AND Practicas.ID = Tareas.IDPractica GROUP BY Nombre,Apellido1,Apellido2;"
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        registros = cursor.fetchall()
        for registro in registros:
            print(registro[0],registro[1],registro[2],registro[3])
    except:
        print("Error en la consulta")
        
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
    try:
        cursor.execute(sql)
        registros = cursor.fetchall()
        for registro in registros:
            print(registro[0],registro[1],registro[2],registro[3],registro[4],registro[5])
    except:
        print("Error en la consulta")
    
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
    try:
        cursor.execute(sql)
        registros = cursor.fetchall()
        for registro in registros:
            print(registro[0],registro[1],registro[2],registro[3],registro[4],registro[5])
    except:
        print("Error en la consulta")
        
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
    except:
        db.rollback()
        
def MariaDB_BorraAlumno(db):
    nombre=input("Nombre del alumno: ")
    apellido1=input("Primer apellido del alumno: ")
    apellido2=input("Segundo apellido del alumno: ")
    sql=f"DELETE FROM Alumnos WHERE Nombre='{nombre}' AND Apellido1='{apellido1}' AND Apellido2='{apellido2}'"
    cursor=db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()

def MariaDB_ActualizaDireccion(db):
    print()