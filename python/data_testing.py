import pandas as pd
import mysql.connector
import glob

#  MySQL connection
conn = mysql.connector.connect(
    host="localhost",
    user="keerthi",
    password="1234",   # put password if you set one
    database="telecom_db"
)
