import pymysql

class SQLDB:
    def __init__ (self, host, port, user, password, db_name):
        self.host = host
        self.user = user
        self.db_name = db_name
        self.port = port
        self.db = pymysql.connect(host=self.host,
                                user=self.user,
                                password=password,  #"ntC1234#31#",
                                database=self.db_name, 
                                port=self.port)
    
    def sql_commit (self):
        self.db.commit()
    
    def sql_read_table (self, table_name):
        try:
            db = self.db
            cursor = db.cursor()
            cursor.execute(f"SELECT * FROM {table_name}")

            result = cursor.fetchall()

            for x in result:
                print(x)
        except Exception as e:
            print(e)

    def sql_update_table (self, table_name, colums, row_data):
        try:
            db = self.db

            cursor = db.cursor()
            
            # 插入資料 (column)
            sql = f"INSERT INTO {table_name}({colums}) VALUES {row_data}"
            cursor.execute(sql)

            db.commit()

            print(cursor.rowcount, "OK !")

            for x in cursor:
                print(x)
        except Exception as e:
            print(e)

    








def sql_delete_table (db_name, table_name):
    try:
        db = pymysql.connect(host="localhost",
                            user="root",
                            password="123456",  #"ntC1234#31#",
                            database=db_name)

        cursor = db.cursor()

        # 刪除
        sql = f"DELETE FROM sites WHERE name = '{table_name}'"
        cursor.execute(sql)
        db.commit()


        # 查詢
        cursor.execute(f"SELECT * FROM {table_name}")
        result = cursor.fetchall()

        for x in result:
            print(x)
    except Exception as e:
        print(e)

def sql_read_table (db_name, table_name):
    try:
        db = pymysql.connect(host="localhost",
                            user="root",
                            password="123456",  #"ntC1234#31#",
                            database=db_name)

        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")

        result = cursor.fetchall()

        for x in result:
            print(x)
    except Exception as e:
        print(e)

def sql_update_table (db_name, table_name, colums, row_data):
    try:
        db = pymysql.connect(host="localhost",
                        user="root",
                        password="123456",  #"ntC1234#31#",
                        database=db_name)

        cursor = db.cursor()
        
        # 插入資料 (column)
        sql = f"INSERT INTO {table_name}({colums}) VALUES {row_data}"
        cursor.execute(sql)
        # sql = f"INSERT INTO {table_name}({colums}) VALUES (%s, %s)"
        # val = f"{row_data}"
        # cursor.execute(sql, val)

        db.commit()

        print(cursor.rowcount, "OK !")

        for x in cursor:
            print(x)
    except Exception as e:
        print(e)
    


def sql_create_table (db_name, table_name, columns_setup):
    try:
        db = pymysql.connect(host="localhost", 
                            user="root", 
                            password="123456",  #"ntC1234#31#",
                            database=db_name)
        
        cursor = db.cursor()

        cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
        result = cursor.fetchone()

        if result is not None:
            print("Table exists!")
        else:
            print("Create table")
            cursor.execute(f"CREATE TABLE {table_name} ({columns_setup})")
        cursor.execute("SHOW TABLES")

        for x in cursor:
            print(x)
    except Exception as e:
        print(e)

def sql_create_db (db_name):
    try:
        db = pymysql.connect(host="localhost", 
                            user="root", 
                            password="123456",  #"ntC1234#31#",
                            )

        cursor = db.cursor()

        cursor.execute(f"SHOW DATABASES LIKE '{db_name}'")
        result = cursor.fetchone()

        if result is not None:
            print("Database exists!")
        else:
            print("Create Database.")
            cursor.execute("SHOW DATABASES")
            cursor.execute(f"CREATE DATABASE {db_name}")
            cursor.execute("SHOW DATABASES")

        for x in cursor:
            print(x)
    except Exception as e:
        print(e)

def get_sql_version () -> str:
    try:
        db = pymysql.connect(host="localhost", 
                            user="root", 
                            password="ntC1234#31#")

        cursor = db.cursor()
        cursor.execute("SELECT VERSION()")
        data = cursor.fetchone()

        print("Database version: " + str(data))

        db.close()

        return str(data)
    except Exception as e:
        print(e)

def sql_delete_table_data (db_name, table_name, condition):
    try:
        db = pymysql.connect(host="localhost",
                        user="root",
                        password="123456",  #"ntC1234#31#",
                        database=db_name)

        cursor = db.cursor()

        # 插入資料 (column)
        sql = f"DELETE FROM {table_name} WHERE {condition}"

        cursor.execute(sql)
        db.commit()

        print(cursor.rowcount, "OK !")

        for x in cursor:
            print(x)
    except Exception as e:
        print(e)


def sql_delete_table_data_all (db_name, table_name):
    try:
        db = pymysql.connect(host="localhost",
                        user="root",
                        password="123456",  #"ntC1234#31#",
                        database=db_name)

        cursor = db.cursor()

        # 插入資料 (column)
        sql = f"DELETE FROM {table_name}"

        cursor.execute(sql)
        db.commit()

        print(cursor.rowcount, "OK !")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    sql_create_db("NTC")
    sql_create_table("NTC", "score", "name VARCHAR(255), value VARCHAR(255)")
    sql_update_table("NTC", "score", "name, value", """("1","40"),("2", "60"),("3", "70"),("4", "90")""")
    sql_delete_table_data("NTC", "score", "value < 60")
    sql_read_table("NTC", "score")
