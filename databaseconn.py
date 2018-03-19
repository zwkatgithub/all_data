import pymysql
from log import Log
class DatabaseConnector:
    
    def __init__(self):
        self.__conn = None
        self.__cur = None

    
    def connect(self):
        try:
            self.__conn = pymysql.connect("192.168.0.251","team1","12345qwert",'zwk')
            print("Connected")
        except Exception:
            Log.log('databaseconn.py','connect')
            return None
        self.__cur = self.__conn.cursor()
    
    @property
    def cursor(self):
        return self.__cur

    def close(self):
        self.__conn.close()

    def commit(self):
        self.__conn.commit()

    def rollback(self):
        self.__conn.rollback()

        
if __name__ == '__main__':

    conn = DatabaseConnector()
    conn.connect()
    #conn.close()