import mysql.connector

def get_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",  
            database="ecommerce_db"        
        )
        return connection
    except mysql.connector.Error as err:
        print("❌ Error connecting to MySQL:", err)
        return None