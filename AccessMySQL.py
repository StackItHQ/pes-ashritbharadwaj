import mysql.

db_config = {
        "host":"localhost",
        "user":"root",
        "password":"arb12345",
        "database":"processors"
}

def connection():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except Exception as e:
        print(e)
        return None
    
def create_table():
    conn = connection()
    cursor = conn.cursor()

    try:
        cursor.execute("CREATE TABLE IF NOT EXISTS processors (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), manufacturer VARCHAR(255), price FLOAT)")
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        if conn:
            cursor.close()
            conn.close()

