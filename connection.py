import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="tiket_pertandingan"
)

mycursor = mydb.cursor()