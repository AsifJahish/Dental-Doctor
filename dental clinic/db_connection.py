import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname="dental_clinic",
        user="admin_user",
        password="admin123",
        host="localhost",
        port="5432"
    )
