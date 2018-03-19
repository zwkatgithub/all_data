from databaseconn import DatabaseConnector
from log import Log
from useragent import UserAgent

class Spider(UserAgent):

    def __init__(self):
        self.url = None
        self.params = None
        try:
            self.conn = DatabaseConnector()
            #self.conn.connect()
        except:
            Log.log(__file__,'__init__')
            raise Exception