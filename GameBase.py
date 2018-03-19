from Spider import Spider
from sql import Sql
from log import Log
from utils import change

class GameBase(Spider):
    colNames = [
            'min','pts','fgm',
            'fga','fg_pct','fg3m',
            'fg3a','fg3_pct','ftm',
            'fta','ft_pct','oreb',
            'dreb','reb','ast','tov',
            'stl','blk','pf','plus_minus'
        ]

    @staticmethod
    def insertSql(data):
        #print(data)
        value = ','.join([change(d) for d in data])
        #print(value)
        sql = Sql.insertValue.format(
            table='game_base_data',
            colNames=','.join(GameBase.colNames),
            value = value
        )
        return sql



