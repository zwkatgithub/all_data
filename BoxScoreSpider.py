import requests
from useragent import UserAgent
from log import Log
from utils import genDict, change, genGameID, genSeason
from databaseconn import DatabaseConnector
from sql import Sql
from Spider import Spider
from GameBase import GameBase
import argparse

class BoxScoreSpider(Spider):

    def __init__(self, seasons,
        url = 'http://stats.nba.com/stats/boxscoretraditionalv2',
        params = {
        'EndPeriod': '10',
        'EndRange': '28800',
        'GameID': None,
        'RangeType': '0',
        'Season': None,
        'SeasonType': 'Regular Season',
        'StartPeriod': '1',
        'StartRange': '0'       
        }):

        super(BoxScoreSpider,self).__init__()
        self.url = url
        self.params = params
        self.startSeason, self.endSeason = [int(s) for s in seasons.split('-')]
        #self.startGame, self.endGame = [int(g) for g in games.split('-')]
        self.data = None
        self.colNames = [
            'game_id','team_id','player_id','game_base_data_id','start_pos'
        ]
        self.playerIds = self.getPlayerIds()
    def __del__(self):
        self.conn.close()
    def getPlayerIds(self):
        self.conn.connect()
        self.conn.cursor.execute('SELECT player_id FROM player;')
        res = self.conn.cursor.fetchall()
        result = []
        for r in res:
            result.append(r[0])
        self.conn.close()
        return result
    def writePlayer(self,data):
        if data[0] not in self.playerIds:
            self.conn.cursor.execute(
                Sql.insertIgnoreValue.format(
                    table='player',colNames="player_id, name",
                    value= ','.join([change(d) for d in data])
                )
            )
            self.playerIds.append(data[0])

    def getPlayerIdName(self,row):
          return [
              row[self.dict['PLAYER_ID']],
              row[self.dict['PLAYER_NAME']].replace("\'","\\\'")
          ]
    def getGameID(self,season):
        self.conn.cursor.execute('SELECT game_id from game where season = \'{0}\' '.format(season))
        res = self.conn.cursor.fetchall()
        result = (r[0] for r in res)
        return result

    def getGameBase(self,row):
        res = []
        for col in GameBase.colNames:
            res.append(row[self.dict[col.upper() if col != 'tov' else 'TO']])
        return res

    def writeGameBase(self,row):
        rd = self.getGameBase(row)
        baseSql = GameBase.insertSql(rd)
        self.conn.cursor.execute(baseSql)
        self.conn.commit()
        self.conn.cursor.execute('select MAX(game_base_data_id) from game_base_data;')
        gameBaseID = self.conn.cursor.fetchone()[0]
        return gameBaseID
    def writeBoxScore(self,values):
        q = Sql.insertValues.format(table='box_score',
                        colNames = ','.join(self.colNames),
                        values= ','.join(values)
        )
        #print(q)
        self.conn.cursor.execute(q)
        self.conn.commit()
    def run(self):
        self.conn.connect()
        for season in range(self.startSeason, self.endSeason+1):
            gameIDs = self.getGameID(season)
            
            for gameID in gameIDs:
                #self.conn.cursor.execute("SELECT COUNT(*) FROM box_score WHERE game_id = \'{0}\';".format(gameID))
                #if self.conn.cursor.fetchone()[0] == 0:
                #    continue
                print("processing "+str(gameID))
                self.params['GameID'] = str(gameID)
                self.params['Season'] = genSeason(season)
                try:
                    self.data = requests.get(self.url,params=self.params, headers={'User-Agent':self.userAgent}).json()
                except Exception:
                    Log.log(__file__, "run",gameID)
                    continue
                self.dict = genDict(self.data['resultSets'][0]['headers'])
                for row in self.data['resultSets'][0]['rowSet']:
                    values = []
                    #gameBaseID= 0
                    gameBaseID = self.writeGameBase(row)
                    self.writePlayer(self.getPlayerIdName(row))
                    values.append("("+
                        ','.join([
                            change(row[self.dict['GAME_ID']]),
                            change(row[self.dict['TEAM_ID']]),
                            change(row[self.dict['PLAYER_ID']]),
                            change(gameBaseID),
                            change(row[self.dict['START_POSITION']])
                        ])+")"
                    )
                    #print(values)
                    self.writeBoxScore(values)




if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('-s','--season')

    args = p.parse_args()

    bxSpider = BoxScoreSpider(args.season)
    bxSpider.run()

                


                
        
                    

                
                
                
                
                

        
